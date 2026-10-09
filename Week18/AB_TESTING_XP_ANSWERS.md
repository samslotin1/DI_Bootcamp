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

The main risks are noisy early winners, changing traffic mix over time, unfair exposure, harder inference, and operational complexity. Address them with exploration floors, randomized assignment, batch updates, logged allocation probabilities, segment/novelty checks, simulation before launch, and analysis designed for adaptive trials.
