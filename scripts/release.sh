#!/usr/bin/env bash
set -euo pipefail

# Simple release helper for iacgen
#
# Usage:
#   ./scripts/release.sh 1.0.0
#
# This script:
#   - Validates the version is in X.Y.Z format (no dev/rc/etc.)
#   - Updates pyproject.toml, src/iacgen/__init__.py, and README.md version references
#   - Shows git status and suggests commit/tag/push commands
#

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Enforce simple semver X.Y.Z
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "ERROR: Version must be in X.Y.Z format (e.g. 1.0.0), got: $VERSION" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYPROJECT="$ROOT_DIR/pyproject.toml"
INIT_FILE="$ROOT_DIR/src/iacgen/__init__.py"
README_FILE="$ROOT_DIR/README.md"

if [[ ! -f "$PYPROJECT" ]]; then
  echo "ERROR: pyproject.toml not found at $PYPROJECT" >&2
  exit 1
fi

if [[ ! -f "$INIT_FILE" ]]; then
  echo "ERROR: src/iacgen/__init__.py not found at $INIT_FILE" >&2
  exit 1
fi

if [[ ! -f "$README_FILE" ]]; then
  echo "ERROR: README.md not found at $README_FILE" >&2
  exit 1
fi

echo "Releasing iacgen version $VERSION"

echo "Updating pyproject.toml..."
# Replace the version line under [project]
python - << PY
from pathlib import Path
pyproject = Path(r"$PYPROJECT")
text = pyproject.read_text()

import re
text_new = re.sub(
    r"^version\s*=\s*\"[^\"]*\"",
    f'version = "{"$VERSION"}"',
    text,
    count=1,
    flags=re.MULTILINE,
)
pyproject.write_text(text_new)
PY

echo "Updating src/iacgen/__init__.py..."
python - << PY
from pathlib import Path
init_file = Path(r"$INIT_FILE")
text = init_file.read_text()
import re
text_new = re.sub(
    r'^__version__\s*=\s*\"[^\"]*\"',
    f'__version__ = "{"$VERSION"}"',
    text,
    count=1,
    flags=re.MULTILINE,
)
init_file.write_text(text_new)
PY

echo "Updating README.md version references..."
python - << PY
from pathlib import Path
import re

readme = Path(r"$README_FILE")
text = readme.read_text()

# Replace any semantic-version-with-v prefix (e.g. v1.0.0) with the new version
text_new = re.sub(
    r"v[0-9]+\.[0-9]+\.[0-9]+",
    f'v{"$VERSION"}',
    text,
)

readme.write_text(text_new)
PY

cd "$ROOT_DIR"

echo
echo "Changes made for version $VERSION:" 
git diff

echo
echo "Next steps (run manually):"
echo "  git add pyproject.toml src/iacgen/__init__.py README.md"
echo "  git commit -m \"chore(release): v$VERSION\""
echo "  git tag -a v$VERSION -m \"Release v$VERSION\""
echo "  git push origin HEAD"
echo "  git push origin v$VERSION"
