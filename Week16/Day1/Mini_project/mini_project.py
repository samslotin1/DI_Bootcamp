"""Scrape dynamic hosting-plan data with Selenium and BeautifulSoup.

Target page:
    https://www.inmotionhosting.com/shared-hosting

The script opens the page in Chrome, waits for JavaScript-rendered content,
parses the final HTML with BeautifulSoup, and saves plan details to CSV.
"""

from __future__ import annotations

import argparse
import csv
import re
import time
from dataclasses import dataclass
from pathlib import Path

import chromedriver_autoinstaller
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_URL = "https://www.inmotionhosting.com/shared-hosting"
DEFAULT_OUTPUT = "hosting_plans.csv"
PLAN_NAMES = ("Launch", "Power", "Pro")


@dataclass
class HostingPlan:
    name: str
    price: str
    renewal_price: str
    savings: str
    features: list[str]


def build_driver(headless: bool = True) -> webdriver.Chrome:
    """Initialize Selenium WebDriver."""
    chromedriver_path = chromedriver_autoinstaller.install()

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1400")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=Service(chromedriver_path), options=options)


def load_page(driver: webdriver.Chrome, url: str, timeout: int = 25) -> str:
    """Load a dynamic webpage and return the fully rendered page source."""
    driver.get(url)

    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    try:
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                    "'abcdefghijklmnopqrstuvwxyz'), 'shared web hosting plans')]",
                )
            )
        )
    except TimeoutException:
        print("Pricing section was not found quickly; parsing whatever loaded.")

    # Trigger lazy-loaded content by scrolling down the page.
    for percent in (0.25, 0.5, 0.75, 1.0):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight * arguments[0]);",
            percent,
        )
        time.sleep(0.7)

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)
    return driver.page_source


def clean_text(value: str) -> str:
    """Normalize whitespace while keeping readable text."""
    return re.sub(r"\s+", " ", value).strip()


def nearest_card(heading: Tag) -> Tag:
    """Find the closest plan-card-like container around a plan heading."""
    for parent in heading.parents:
        if not isinstance(parent, Tag):
            continue

        text = clean_text(parent.get_text(" ", strip=True))
        has_price = bool(re.search(r"[$€£]\s*\d", text))
        has_feature_list = parent.find("li") is not None
        is_not_whole_page = parent.name not in {"body", "html"}

        if is_not_whole_page and has_price and has_feature_list:
            return parent

    return heading.parent if isinstance(heading.parent, Tag) else heading


def parse_plan_from_card(plan_name: str, card: Tag) -> HostingPlan:
    """Extract one hosting plan from a rendered pricing card."""
    text = clean_text(card.get_text(" ", strip=True))

    price_match = re.search(r"([$€£]\s*\d+(?:[.,]\d{2})?\s*/mo)", text)
    renewal_match = re.search(
        r"Renews?\s+at\s+([$€£]\s*\d+(?:[.,]\d{2})?\s*/mo)",
        text,
        flags=re.IGNORECASE,
    )
    savings_match = re.search(r"You\s+Save\s+\d+%", text, flags=re.IGNORECASE)

    features = []
    for item in card.find_all("li"):
        feature = clean_text(item.get_text(" ", strip=True))
        if feature and feature not in features:
            features.append(feature)

    return HostingPlan(
        name=plan_name,
        price=clean_text(price_match.group(1)) if price_match else "Not found",
        renewal_price=clean_text(renewal_match.group(1)) if renewal_match else "Not found",
        savings=clean_text(savings_match.group(0)) if savings_match else "Not found",
        features=features,
    )


def parse_hosting_plans(html: str) -> list[HostingPlan]:
    """Parse hosting plans from Selenium's rendered HTML."""
    soup = BeautifulSoup(html, "html.parser")
    plans: list[HostingPlan] = []
    seen_names: set[str] = set()

    heading_tags = soup.find_all(re.compile(r"^h[1-6]$"))
    for heading in heading_tags:
        heading_text = clean_text(heading.get_text(" ", strip=True))
        if heading_text not in PLAN_NAMES or heading_text in seen_names:
            continue

        card = nearest_card(heading)
        plan = parse_plan_from_card(heading_text, card)

        if plan.price != "Not found" or plan.features:
            plans.append(plan)
            seen_names.add(heading_text)

    return plans


def save_to_csv(plans: list[HostingPlan], output_path: Path) -> None:
    """Store and save the extracted data in CSV format."""
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["plan_name", "price", "renewal_price", "savings", "features"],
        )
        writer.writeheader()

        for plan in plans:
            writer.writerow(
                {
                    "plan_name": plan.name,
                    "price": plan.price,
                    "renewal_price": plan.renewal_price,
                    "savings": plan.savings,
                    "features": " | ".join(plan.features),
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape InMotion Hosting shared hosting plans into a CSV file."
    )
    parser.add_argument("--url", default=DEFAULT_URL, help="Dynamic webpage to scrape")
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="CSV output path, for example hosting_plans.csv",
    )
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Run Chrome visibly instead of headless mode",
    )
    args = parser.parse_args()

    driver = build_driver(headless=not args.show_browser)

    try:
        html = load_page(driver, args.url)
        plans = parse_hosting_plans(html)

        if not plans:
            raise RuntimeError("No hosting plans were found on the rendered page.")

        output_path = Path(args.output)
        save_to_csv(plans, output_path)

        print(f"Saved {len(plans)} hosting plans to {output_path.resolve()}")
        for plan in plans:
            print(f"- {plan.name}: {plan.price} ({len(plan.features)} features)")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
