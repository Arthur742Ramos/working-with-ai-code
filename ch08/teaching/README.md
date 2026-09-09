# Chapter 8 teaching sequence

The September editorial rebase restores the visible missing-cent example before the independently captured exact-tie repair. It does not change the certified capture or the promoted allocator.

| Listing | Internal source | Purpose |
|---|---|---|
| 8.1 | `draft_allocation.py::allocate` in this directory | Deliberately rounds each share independently |
| 8.2 | `draft_allocation.py::conserves` and `smoke_test` | Rejects the missing cent using the original total |
| 8.3 | `../captures/lost_cent_allocation/before/allocation.py::allocate` | Same code with the ideal expression wrapped for print; conserves money but misorders the exact tie |
| 8.4 | Two named functions from `../test_allocation.py`, with their import | Even split and conserved-total regression |
| 8.5 | `../test_allocation.py::test_equal_exact_remainders_keep_input_order` | Stable order for equal mathematical remainders |
| 8.6 | `../captures/lost_cent_allocation/patches/allocation.patch` | Unmodified historical patch, including the original one-line expression |
| 8.7 | `../test_golden.py` | Six trusted rows and the same assertion loop; main runner omitted |

The reader evolves `allocation.py` through the three arithmetic stages. The small stage-2 and stage-3 calculation omits application validation explicitly. The maintained top-level implementation retains its existing validation and `split_charge` wrapper. Do not present either illustrative draft as the validated application.

The printed session now selects the focused red and focused/broader green from the preserved record. It omits the historical nine-test baseline run. The ten-test final-package result is labeled separately as post-session verification. The complete original exchange, raw evidence, checksums, and independent-review receipt remain unchanged.

From the book workspace, `python3 -m pytest code/tools/test_ch08_printed_examples.py -q` checks the printed stages against these sources, the demonstrated failures, and the exact captured patch. The package's original ten-test suite and isolated capture replay remain the final implementation checks.
