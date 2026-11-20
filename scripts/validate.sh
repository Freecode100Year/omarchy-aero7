#!/bin/bash
# Omarchy Aero7: validate — wraps `aero7 validate`.
set -euo pipefail
exec "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/../bin/aero7" validate "$@"
