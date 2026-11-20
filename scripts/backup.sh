#!/bin/bash
# Omarchy Aero7: backup — wraps `aero7 backup`.
set -euo pipefail
exec "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/../bin/aero7" backup "$@"
