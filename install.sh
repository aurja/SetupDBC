#!/usr/bin/env bash
# Install the SetupDBC skill into omp's user skill directory.
# Usage: ./install.sh [skills-dir]    (default: ~/.omp/agent/skills)
# Replaces any existing SetupDBC install there.
set -euo pipefail

src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/SetupDBC"
skills_dir="${1:-$HOME/.omp/agent/skills}"
dest="$skills_dir/SetupDBC"

mkdir -p "$skills_dir"
rm -rf "$dest"
cp -R "$src" "$dest"
find "$dest" \( -name __pycache__ -o -name .ruff_cache -o -name .pytest_cache \) -prune -exec rm -rf {} +

echo "Installed SetupDBC -> $dest"
