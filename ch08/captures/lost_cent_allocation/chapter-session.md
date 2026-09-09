# Captured Chapter 8 publication excerpt

You fix the missing cent with largest remainder and pin stable input order for ties. Then a plain integer case returns `[2, 1, 7]` where the policy requires `[2, 2, 6]`. The total is correct. The ranking is not.

*The exchange below comes from a real session with a coding agent (Claude Code 2.1.210) acting on `allocation.py` and its tests. The transcript is condensed from tool logs. Commands, output, exit statuses, and the diff come directly from the verified session evidence.*

The inspection contract is condensed from the retained author direction and the bounded session record. It is not presented as a verbatim prompt.

> [!prompt Keep an exact tie stable]
> Inspect `allocation.py` and the allocation tests. Run the exact-tie test before editing, and do not edit until you have observed the failure and stated a one-sentence plan. Fix binary-float misordering for ordinary numeric weights while preserving largest remainder and stable input-order ties. Add no validation, public interface, feature flag, or second allocation workflow. Then run the focused case, the broader suite, and the behavior plus golden tests.

> [!ai-response The total is right but the tie is wrong]
> I inspected the current implementation. It computes ideal shares and ranks their fractional parts as binary floats:
>
> ```python
> ideal = [total * weight / total_weight for weight in weights]
> shares = [int(value) for value in ideal]
> leftover = total - sum(shares)
> order = sorted(
>     range(len(weights)),
>     key=lambda index: ideal[index] - shares[index],
>     reverse=True,
> )
> ```
>
> I ran the focused check before editing:
>
> ```text
> python3 -m pytest -q -p no:cacheprovider test_lost_cent.py::test_equal_exact_remainders_keep_input_order
> F                                                                        [100%]
> =================================== FAILURES ===================================
> _________________ test_equal_exact_remainders_keep_input_order _________________
>
>     def test_equal_exact_remainders_keep_input_order():
> >       assert allocate(10, [1, 1, 4]) == [2, 2, 6]
> E       assert [2, 1, 7] == [2, 2, 6]
> E         
> E         At index 1 diff: 1 != 2
> E         Use -v to get more diff
>
> test_lost_cent.py:13: AssertionError
> =========================== short test summary info ============================
> FAILED test_lost_cent.py::test_equal_exact_remainders_keep_input_order - asse...
> 1 failed in 0.01s
> ```
>
> Exit status: `1`.
>
> All three mathematical remainders are two-thirds. Binary division stores the third residue slightly larger, so the stable sort never sees an equal key and assigns the second leftover cent to index 2.
>
> Plan: convert each stated numeric weight to an exact rational with `Fraction(str(weight))`, preserve the existing named largest-remainder stages and stable sort, and keep the exact-tie case beside the earlier conservation and shortcut-discriminating cases.

The direct author instruction authorized the bounded implementation without another approval checkpoint. The agent selected decimal-string rationalization because it preserves ordinary stated numeric weights instead of ranking their hidden binary approximations.

> [!ai-response Exact residues, the same allocation workflow]
> I changed the arithmetic representation before the existing largest-remainder stages:
>
> ```diff
> --- a/allocation.py
> +++ b/allocation.py
> @@ -1,9 +1,18 @@
>  """Proportional allocation with stable input-order ties."""
>  
> +from fractions import Fraction
>  
> +
>  def allocate(total, weights):
> -    total_weight = sum(weights)
> -    ideal = [total * weight / total_weight for weight in weights]
> +    exact_weights = [
> +        Fraction(str(weight))
> +        for weight in weights
> +    ]
> +    total_weight = sum(exact_weights)
> +    ideal = [
> +        total * weight / total_weight
> +        for weight in exact_weights
> +    ]
>      shares = [int(value) for value in ideal]
>      leftover = total - sum(shares)
>      order = sorted(
> ```
>
> I reran the focused check:
>
> ```text
> python3 -m pytest -q -p no:cacheprovider test_lost_cent.py::test_equal_exact_remainders_keep_input_order
> .                                                                        [100%]
> 1 passed in 0.00s
> ```
>
> Exit status: `0`.
>
> I then ran the broader staged suite:
>
> ```text
> python3 -m pytest -q -p no:cacheprovider
> ......                                                                   [100%]
> 6 passed in 0.01s
> ```
>
> Exit status: `0`.
>
> Finally, I verified the unchanged maintained behavior and golden baseline:
>
> ```text
> python3 -m pytest -q -p no:cacheprovider test_allocation.py test_golden.py
> .........                                                                [100%]
> 9 passed in 0.00s
> ```
>
> Exit status: `0`.
>
> The focused case proves the covered exact tie now keeps input order. The six staged cases retain the missing-cent, exact split, unequal remainder, and round-then-force-index-zero protections. The nine maintained tests confirm that the unchanged baseline was green. They did not run against the staged repair, so they do not prove its compatibility. These checks do not cover every numeric type, non-finite input, extreme magnitude, or fairness policy.

Inspect the boundary the patch moved. `Fraction(str(weight))` makes the stated numeric weights exact before `ideal` computes proportional claims. The familiar `leftover` and `order` stages remain visible, so the repair strengthens the original workflow instead of hiding a second one beside it. The new test also exposes why conservation is necessary but insufficient: `[2, 1, 7]` adds up correctly while violating the selected tie rule.

Look at what the loop bought you: one green invariant stopped masking a ranking defect, the diff stayed inside the chapter's largest-remainder slice, and the broader staged suite ran beside the focused proof. It also exposed the evidence still missing for release. The original maintained run did not exercise the staged repair. Decimal-string rationalization works for the covered ordinary numeric weights, but it does not define accepted numeric types or decide whether stable input order is fair. Domain owners set those policy boundaries; the unified final-package run supplies the missing engineering evidence.

## Final-package promotion note

After the captured session, the exact-rational implementation and exact-tie regression were promoted into one final package. Its separately labeled ten-test evidence runs the nine canonical-equivalent checks plus the promoted exact-tie test against the same implementation. This post-capture verification is not presented as part of the original agent response.
