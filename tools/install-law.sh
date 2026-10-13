#!/bin/sh
# Pinned standalone law for this consumer kit. No Python runtime is required.
set -eu
repo_dir=$(cd "$(dirname "$0")/.." && pwd)
dest_dir=${1:-"$repo_dir/.toolchain"}
case "$(uname -s)/$(uname -m)" in
  Darwin/arm64)
    target=aarch64-apple-darwin
    archive_hash=8f145984f496b54dc1bbec79d6b7eec1c3115aaf8a2a8365d1eca9dc686d723b
    binary_hash=05ed4e45f15669bc0c2953effcadcf16e91800e3777e4022831280a061185d63 ;;
  Linux/x86_64)
    target=x86_64-unknown-linux-gnu
    archive_hash=31990a87cad5ff8f32384113ea8eccab1067b23e7cb92b0276fee7adabb00afd
    binary_hash=f3282131d5f1fee27fda9adb000da3ac326dc035ef3bd8eb8b202d8b6db1fb7e ;;
  *) printf '%s\n' 'Supported platforms: macOS arm64, Linux x86_64.' >&2; exit 1 ;;
esac
digest() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d ' ' -f 1
  else shasum -a 256 "$1" | cut -d ' ' -f 1; fi
}
if [ -e "$dest_dir" ]; then
  if [ -f "$dest_dir/law" ] && [ "$(digest "$dest_dir/law")" = "$binary_hash" ]; then
    "$dest_dir/law" version --json
    exit 0
  fi
  printf '%s\n' 'Destination exists with different files; choose a new directory.' >&2
  exit 1
fi
scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/arxo-japan-law.XXXXXX")
trap 'rm -rf "$scratch_dir"' 0
trap 'exit 1' HUP INT TERM
archive_name="law-0.2.3-japan.1-$target.tar.gz"
curl --fail --location --silent --show-error \
  "https://github.com/arxohq/arxo-japan/releases/download/cli-0.2.3-japan.1/$archive_name" \
  --output "$scratch_dir/cli.tar.gz"
[ "$(digest "$scratch_dir/cli.tar.gz")" = "$archive_hash" ] || { printf '%s\n' 'Archive SHA-256 mismatch.' >&2; exit 1; }
mkdir "$scratch_dir/install"
tar -xzf "$scratch_dir/cli.tar.gz" -C "$scratch_dir/install"
[ "$(digest "$scratch_dir/install/law")" = "$binary_hash" ] || { printf '%s\n' 'Binary SHA-256 mismatch.' >&2; exit 1; }
mkdir -p "$(dirname "$dest_dir")"
mv "$scratch_dir/install" "$dest_dir"
"$dest_dir/law" version --json
printf 'law installed in %s\n' "$dest_dir"
