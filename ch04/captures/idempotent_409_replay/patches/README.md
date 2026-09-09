# Patch artifact

`idempotent_409_replay.patch` is the machine-generated unified diff between the immutable reconstructed before fixture and the disposable after-state copy. It changes one production line so the fixed customer endpoint returns its existing result for exactly `409` in addition to status codes below `400`.

The capture runner applies this patch only inside `.work/`, regenerates the diff with `diff -u`, byte-compares it with the stored artifact, verifies the expected after-state SHA-256 checksum, and removes the working copy. The patch does not modify the package-local green importer.
