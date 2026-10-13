# Delivery and provenance

This repository is a consumer export of two selected Arxo corpus packages. It has fresh Git history; neither private corpus history nor unrelated packages are part of the delivery.

- `source-pin.json` captures the originating corpus commit and exact selected working-tree bytes. The file hashes, not an assumption about the originating branch, identify the delivered source snapshot.
- `packages/*/law.lock` pins each independent root to `law.core/0.2.11`. There are no imported package dependencies.
- `registry/` contains fresh CLI lowering of those exact package sources. Raw world SHA-256 and model artifact hashes are different identifiers and are recorded separately.
- `reports/formalization-depth.json` contains structural per-article measurement, its denominator and implementation hashes. The existing classifier is used; the applicability helper is a recorded captured implementation override, not acceptance of the unpublished corpus runtime.
- `toolchain.lock.json` pins the standalone CLI archives. The `0.2.3-japan.1` candidate contains the reference-valued-authority fix. Its core source branch has a separate review; that is not a claim that the change has already merged into every Arxo SDK or npm package.

The existing exact-allowlist `canon_publication.py` exporter creates the publication artifact. To reconstruct that artifact from this checkout, use a **new output directory**:

```sh
python3.12 tools/canon_publication.py export --source . \
  --config publication.toml --out /tmp/arxo-japan-artifact
python3.12 tools/canon_publication.py verify --artifact /tmp/arxo-japan-artifact
```

The verifier checks the exact inventory, byte hashes and lock resources without the private corpus. The reader-oriented `tools/check.py` additionally tests only Constitution and Kanpo, and compares complete example documents across repeated evaluation. It runs package tests in temporary directories to preserve the checkout.

The CLI is delivered as a GitHub Release asset, not checked into Git. Downloaded archives include its own license and third-party notices. The model release includes source texts, models, tests, reader cases, canonical answers and SVG visuals. Caches, node_modules, build targets and local machine paths are outside the allowlist.

Fresh addressed execution and historical execution are reported separately. The full corpus remains `not_checked`; `releaseVerified` remains `false`. No npm canon, browser SDK bundle, website, book revision or public central-catalog update is part of this release.

Reader revision 0.1.1 adds self-contained native `request.json` inputs and a hash-pinned POSIX-shell installer. Readers use `law eval`, `law inspect` and `law test`; Python remains an optional maintainer tool. The legal models and CLI archive pins are unchanged.
