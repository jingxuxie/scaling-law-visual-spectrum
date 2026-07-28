#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/scaling-law-visual-spectrum" >&2
  exit 2
fi

repo="$(cd "$1" && pwd)"
root="$(cd "$(dirname "$0")" && pwd)"

cp "$root/paper/main.tex" "$repo/paper/main.tex"
cp "$root/paper/references.bib" "$repo/paper/references.bib"
cp "$root/experiments/damping_knee_sweep.py" \
   "$repo/experiments/damping_knee_sweep.py"
mkdir -p "$repo/experiments/results"
cp "$root/experiments/results/damping_knee_sweep.csv" \
   "$repo/experiments/results/damping_knee_sweep.csv"

echo "Applied expanded AAAI revision to $repo"
echo "Next: compile with the official aaai2027 author kit and inspect page count."
