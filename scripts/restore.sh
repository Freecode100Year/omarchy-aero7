#!/bin/bash
# Omarchy Aero7: restore — wraps `aero7 restore`.
set -euo pipefail
exec "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/../bin/aero7" restore "$@"
