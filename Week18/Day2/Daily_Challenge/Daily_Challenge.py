"""Power analysis for Sweet Bytes' checkout A/B test.

This script calculates the sample size needed for a two-sided A/B test with
equal group sizes. It uses the noncentral t distribution, matching the logic
behind common tools such as statsmodels' TTestIndPower.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from scipy import optimize, stats


@dataclass(frozen=True)
class PowerSettings:
    alpha: float = 0.05
    desired_power: float = 0.80
    ratio: float = 1.0
    alternative: str = "two-sided"


def two_sample_ttest_power(
    sample_size_per_group: float,
    effect_size: float,
    settings: PowerSettings,
) -> float:
    """Return statistical power for an equal-sized two-sample t-test."""
    n_control = sample_size_per_group
    n_treatment = sample_size_per_group * settings.ratio
    degrees_of_freedom = n_control + n_treatment - 2
    noncentrality = abs(effect_size) * math.sqrt(
        (n_control * n_treatment) / (n_control + n_treatment)
    )

    if settings.alternative == "two-sided":
        critical_value = stats.t.ppf(1 - settings.alpha / 2, degrees_of_freedom)
        upper_tail = stats.nct.sf(critical_value, degrees_of_freedom, noncentrality)
        lower_tail = stats.nct.cdf(-critical_value, degrees_of_freedom, noncentrality)
        return upper_tail + lower_tail

    if settings.alternative == "larger":
        critical_value = stats.t.ppf(1 - settings.alpha, degrees_of_freedom)
        return stats.nct.sf(critical_value, degrees_of_freedom, noncentrality)

    raise ValueError("alternative must be 'two-sided' or 'larger'")


def required_sample_size(effect_size: float, settings: PowerSettings) -> int:
    """Solve for the minimum rounded-up sample size per group."""
    if effect_size <= 0:
        raise ValueError("effect_size must be positive")

    def objective(sample_size: float) -> float:
        return two_sample_ttest_power(sample_size, effect_size, settings) - settings.desired_power

    lower_bound = 2
    upper_bound = 4
    while objective(upper_bound) < 0:
        upper_bound *= 2

    sample_size = optimize.brentq(objective, lower_bound, upper_bound)
    return math.ceil(sample_size)


def cohens_h_for_conversion_rates(control_rate: float, treatment_rate: float) -> float:
    """Calculate Cohen's h, a common effect size for comparing proportions."""
    return 2 * math.asin(math.sqrt(treatment_rate)) - 2 * math.asin(math.sqrt(control_rate))


def main() -> None:
    settings = PowerSettings(alpha=0.05, desired_power=0.80)
    control_conversion_rate = 0.05
    new_checkout_conversion_rate = 0.07
    assigned_effect_size = 0.20
    effect_sizes = [0.10, 0.20, 0.30, 0.40]

    print("Sweet Bytes A/B Test Power Analysis")
    print("=" * 40)
    print(f"Current checkout conversion rate: {control_conversion_rate:.0%}")
    print(f"Expected new checkout conversion rate: {new_checkout_conversion_rate:.0%}")
    print(f"Significance level (alpha): {settings.alpha}")
    print(f"Desired power: {settings.desired_power}")
    print()

    main_required_n = required_sample_size(assigned_effect_size, settings)
    print("1. Required sample size for the assigned effect size")
    print(f"Effect size: {assigned_effect_size}")
    print(f"Required sample size per group: {main_required_n:,}")
    print(f"Total visitors needed: {main_required_n * 2:,}")
    print()

    print("2. Required sample size as effect size changes")
    print("Effect size | Sample size per group | Total sample size")
    print("------------|-----------------------|------------------")
    for effect_size in effect_sizes:
        needed = required_sample_size(effect_size, settings)
        print(f"{effect_size:>11.2f} | {needed:>21,} | {needed * 2:>17,}")
    print()

    observed_h = abs(
        cohens_h_for_conversion_rates(
            control_conversion_rate,
            new_checkout_conversion_rate,
        )
    )
    observed_required_n = required_sample_size(observed_h, settings)
    print("Conversion-rate context")
    print(
        "A move from 5% to 7% has Cohen's h of "
        f"{observed_h:.3f}, which is smaller than 0.20."
    )
    print(
        "Using that proportion-specific effect size would require about "
        f"{observed_required_n:,} visitors per group."
    )
    print()

    print("3. Bakery-friendly explanation")
    print(
        "Think of effect size as how obvious the new checkout's improvement is. "
        "If the new process is a giant cupcake display in the shop window, a few "
        "customers are enough to notice the difference. If it is only a tiny extra "
        "sprinkle, Sweet Bytes needs many more visitors before the team can be sure "
        "the lift is real and not just random shopping behavior."
    )
    print()
    print(
        "That is why smaller effect sizes require larger samples: subtle changes "
        "are harder to detect through normal day-to-day noise. Planning sample size "
        "up front helps the bakery avoid stopping too early, wasting traffic on a "
        "test that cannot detect the expected lift, or rolling out a checkout change "
        "without enough evidence. The balance gives the team a reliable test that "
        "protects time, marketing budget, and future sweet sales."
    )


if __name__ == "__main__":
    main()
