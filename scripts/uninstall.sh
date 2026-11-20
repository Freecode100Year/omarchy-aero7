#!/bin/bash
# Omarchy Aero7: uninstall — wraps `aero7 uninstall`.
set -euo pipefail
exec "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/../bin/aero7" uninstall "$@"
