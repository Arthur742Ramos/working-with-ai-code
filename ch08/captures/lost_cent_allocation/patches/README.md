# Patch evidence

`allocation.patch` is the machine-generated unified diff from the byte-checked binary-float before fixture to the isolated exact-rational after-state. The patch changes one allocation path and adds no validation, new public API, feature flag, or second workflow.

The reviewed implementation converts each numeric weight with `Fraction(str(weight))`, then retains the named `ideal` list, `leftover` count, and sorted `order`. The conversion prevents binary-float residue from misordering mathematically equal decimal claims. The existing names keep conversion, proportional calculation, ranking, and mutation visible as separate review boundaries. This is the smallest reviewable change in the surrounding idiom, not the fewest-line form.
