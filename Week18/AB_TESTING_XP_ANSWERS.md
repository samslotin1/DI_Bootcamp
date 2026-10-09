# A/B Testing XP — Answers

Run the companion script with `python ab_testing_xp.py`. It requires `statsmodels`, `numpy`, and `scipy`.

## 1. Required sample size

Using `statsmodels.stats.power.TTestIndPower` with a two-sided alpha of 0.05, power of 0.80, equal group sizes, and the supplied standardized effect size of 0.30, the result is **175 users per group** (350 total after rounding up).

The calculation treats `0.30` as Cohen's *d*, as requested. An increase from 20% to 23% is a proportion comparison, not inherently a Cohen's-*d* effect size; for a live email experiment, use a two-proportion calculation with the actual baseline and minimum detectable lift.

## 2. Effect size and sample size

| Effect size | Required sample per group |
|---:|---:|
| 0.20 | 394 |
| 0.40 | 100 |
| 0.50 | 64 |

Larger effects are easier to distinguish from normal sampling noise, so fewer observations are needed. The relationship is roughly inverse-square: halving the effect size requires about four times as many observations.

## 3. Statistical power and sample size

For effect size 0.20 and alpha 0.05:

| Desired power | Required sample per group |
|---:|---:|
| 0.70 | 310 |
| 0.80 | 394 |
| 0.90 | 526 |

More power means a lower chance of missing a real effect (a false negative), which costs more traffic and time. Selecting power in advance makes this trade-off explicit and avoids an underpowered test that cannot answer the product question.

## 4. Sequential testing

Pre-register a maximum sample size and weekly looks, then use a group-sequential alpha-spending rule rather than applying `p < 0.05` every week. The script illustrates a conservative O'Brien–Fleming rule with four equally sized looks; it provides approximate two-sided p-value efficacy boundaries of 0.0001, 0.0056, 0.0236, and 0.0500.

Also predefine a practical lift threshold, a data-quality check, a harm guardrail, and a futility rule. With this preplanned schedule, the week-three result of `p = 0.02` crosses the approximate `0.0236` efficacy boundary, so stop for efficacy only after confirming the effect has the expected direction, meets the practical-lift rule, and passes the guardrails. If no sequential plan was agreed in advance, do **not** use the unadjusted `0.02` as a stop signal; continue to the planned end or analyse with an appropriate correction.

## 5. Bayesian A/B testing

For a binary engagement metric, assign both versions a neutral `Beta(1, 1)` prior. This encodes no preference for either underlying engagement rate; the initially stated 50% belief that the feature is better follows from symmetric priors. After data, each posterior is `Beta(1 + successes, 1 + failures)`. Compare draws from the two posterior distributions to estimate `P(B > A)`.

A 65% probability that B is better updates the belief toward B, but it normally is not enough to launch without a decision threshold and a minimum business benefit. Collect more data or retain the control. At 55%, evidence is especially weak: continue only if the experiment remains valuable, otherwise stop for futility. The script includes `probability_b_beats_a` to make this calculation from observed counts.

## 6. Adaptive experimentation

After the first week, use the three layouts' engagement data—not just the raw highest rate—to calculate uncertainty. Shift some traffic toward C, for example with Thompson sampling based on beta posteriors, while retaining a minimum allocation (such as 15%) for A and B. Recompute allocations after each planned batch, cap abrupt allocation changes, and stop when a predefined decision rule is met.





"""Solutions and runnable examples for the A/B testing XP exercises.

Install dependencies once with:
    python -m pip install statsmodels numpy scipy

The sample-size calculations use Cohen's d because ``TTestIndPower`` expects
the standardized effect size supplied in the exercise.  For a conversion-rate
test in production, calculate an appropriate proportions effect size (such as
Cohen's h) and use a two-proportion power calculation instead.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.stats import norm
from statsmodels.stats.power import TTestIndPower


ALPHA = 0.05
POWER = 0.80


def required_per_group(effect_size: float, power: float = POWER) -> int:
    """Return the rounded-up equal allocation sample size for a two-sided test."""
    n = TTestIndPower().solve_power(
        effect_size=effect_size,
        alpha=ALPHA,
        power=power,
        ratio=1.0,
        alternative="two-sided",
    )
    return math.ceil(n)


def exercise_1_to_3() -> None:
    """Print the requested conventional power-analysis results."""
    print("Exercises 1–3: two-sided independent-groups power analysis")
    print(f"alpha = {ALPHA}, allocation ratio = 1:1\n")

    print(f"1. Effect size 0.30, power 0.80: {required_per_group(0.30):,} per group")

    print("\n2. Effect size | required n per group (power = 0.80)")
    for effect in (0.20, 0.40, 0.50):
        print(f"   {effect:>5.2f}     | {required_per_group(effect):,}")

    print("\n3. Power | required n per group (effect size = 0.20)")
    for power in (0.70, 0.80, 0.90):
        print(f"   {power:>4.2f} | {required_per_group(0.20, power):,}")


def obrien_fleming_boundary(information_fraction: float) -> tuple[float, float]:
    """Return an approximate two-sided O'Brien–Fleming z and p boundary.

    This is a simple alpha-spending illustration for preplanned interim looks.
    A production study should have its boundary schedule approved before data
    collection, ideally with a statistician or validated group-sequential tool.
    """
    if not 0 < information_fraction <= 1:
        raise ValueError("information_fraction must be in (0, 1]")
    fixed_z = norm.ppf(1 - ALPHA / 2)
    z_boundary = fixed_z / math.sqrt(information_fraction)
    return z_boundary, 2 * norm.sf(z_boundary)


def exercise_4() -> None:
    """Show a preplanned four-look sequential-testing decision rule."""
    print("\n4. Sequential testing: four equally sized weekly looks")
    print("Week | Information fraction | Stop for efficacy if two-sided p <=")
    for week in range(1, 5):
        _, p_boundary = obrien_fleming_boundary(week / 4)
        print(f"  {week}  |        {week / 4:.0%}         | {p_boundary:.4f}")

    _, week_three_boundary = obrien_fleming_boundary(0.75)
    decision = "stop and declare B superior" if 0.02 <= week_three_boundary else "continue"
    print(
        f"At week 3, p = 0.020; boundary = {week_three_boundary:.4f}: {decision}."
    )


def probability_b_beats_a(
    a_successes: int,
    a_trials: int,
    b_successes: int,
    b_trials: int,
    prior_alpha: float = 1,
    prior_beta: float = 1,
    draws: int = 200_000,
    seed: int = 42,
) -> float:
    """Estimate P(rate_B > rate_A | data) using beta-binomial posteriors."""
    if not 0 <= a_successes <= a_trials or not 0 <= b_successes <= b_trials:
        raise ValueError("successes must be between 0 and trials")
    rng = np.random.default_rng(seed)
    a_posterior = rng.beta(prior_alpha + a_successes, prior_beta + a_trials - a_successes, draws)
    b_posterior = rng.beta(prior_alpha + b_successes, prior_beta + b_trials - b_successes, draws)
    return float(np.mean(b_posterior > a_posterior))


def exercise_5() -> None:
    """Demonstrate Bayesian updating with a neutral beta prior."""
    print("\n5. Bayesian A/B testing")
    print("Use Beta(1, 1) for each engagement rate: a neutral, uniform prior.")
    print("After observing successes/trials, update to Beta(1 + successes, 1 + failures).")
    print("A posterior P(B > A) of 65% is evidence, but below a typical 90–95% launch threshold.")
    print("At 55%, keep collecting data (or stop for futility); do not roll out based on it.")


def thompson_allocation(alpha_params: np.ndarray, beta_params: np.ndarray, draws: int = 100_000) -> np.ndarray:
    """Allocate traffic by Thompson sampling: probability each layout is best."""
    rng = np.random.default_rng(7)
    sampled_rates = rng.beta(alpha_params, beta_params, size=(draws, len(alpha_params)))
    winners = np.argmax(sampled_rates, axis=1)
    return np.bincount(winners, minlength=len(alpha_params)) / draws


def exercise_6() -> None:
    """Show a guarded adaptive allocation after an initial week."""
    print("\n6. Adaptive experimentation")
    print("Start A/B/C at 33% each. After week 1, estimate each layout's posterior.")
    print("Use probability-of-being-best (e.g., Thompson sampling) for allocation, but keep")
    print("a floor such as 15% for every layout so the experiment can still learn.")
    print("Recompute after each preplanned batch; cap traffic moves and retain user-level logs.")


if __name__ == "__main__":
    exercise_1_to_3()
    exercise_4()
    exercise_5()
    exercise_6()

The main risks are noisy early winners, changing traffic mix over time, unfair exposure, harder inference, and operational complexity. Address them with exploration floors, randomized assignment, batch updates, logged allocation probabilities, segment/novelty checks, simulation before launch, and analysis designed for adaptive trials.
