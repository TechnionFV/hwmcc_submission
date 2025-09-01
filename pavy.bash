#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <benchmark> <certificate.sat> <certificate.unsat>" >&2
  exit 64
}

[[ "${1-}" == "-h" || "${1-}" == "--help" ]] && usage
[[ $# -ne 3 ]] && usage

benchmark=$1
sat_cert=$2
unsat_cert=$3

# Resolve repository root (directory of this script) to find scripts/pavy.py
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
PAVY_PY="$SCRIPT_DIR/scripts/pavy.py"

exec python3 "$PAVY_PY" "$benchmark" --cex "$sat_cert" --certificate "$unsat_cert"

