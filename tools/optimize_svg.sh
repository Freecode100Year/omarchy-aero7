#!/bin/bash
# Optimise every SVG in the project with SVGO (tools/node/node_modules/svgo).
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH=/opt/node22/bin:$PATH
before=$(cat icons/aero7/*.svg assets/*.svg | wc -c)
node tools/node/node_modules/svgo/bin/svgo.js --config tools/svgo.config.mjs -q icons/aero7/*.svg assets/*.svg
after=$(cat icons/aero7/*.svg assets/*.svg | wc -c)
echo "SVGO: $before -> $after bytes"
