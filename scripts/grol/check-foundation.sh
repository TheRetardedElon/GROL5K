#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "GROL guardrail failed: $*" >&2
  exit 1
}

require_file() {
  [[ -f "$1" ]] || fail "missing required file: $1"
}

require_file GROL_VERSION
require_file GROL_UPSTREAM.md
require_file docs/development/STATUS.md
require_file docs/development/CODEBASE_MAP.md
require_file docs/development/M0_BASELINE_CHECKLIST.md
require_file docs/development/M1_IDENTITY_MAP.md
require_file docs/development/AI_COLLABORATION.md
require_file docs/development/GROK_ONBOARDING.md
require_file docs/architecture/COMPONENT_BOUNDARIES.md
require_file docs/decisions/0005-ha-is-ancestry.md
require_file grol/specs/ACTION_BROKER_V0.md
require_file grol/specs/action-request.schema.json

version="$(tr -d '[:space:]' < GROL_VERSION)"
[[ "$version" =~ ^[0-9]+.[0-9]+.[0-9]+(-[A-Za-z0-9.-]+)?$ ]]   || fail "GROL_VERSION is not semver-like: $version"

grep -qx 'HAOS_ID="haos"' buildroot-external/meta   || fail 'HAOS_ID changed; ADR-0002 requires explicit migration planning first'

grep -q 'BR2_PACKAGE_HASSIO_MACHINE="qemux86-64"'   buildroot-external/configs/ova_defconfig   || fail 'OVA Supervisor machine ID changed unexpectedly'

grep -q 'BR2_PACKAGE_OS_AGENT_BOARD="Ova"'   buildroot-external/configs/ova_defconfig   || fail 'OVA OS Agent board ID changed unexpectedly'

grep -q 'BR2_PACKAGE_HASSIO_MACHINE="generic-x86-64"'   buildroot-external/configs/generic_x86_64_defconfig   || fail 'generic x86-64 Supervisor machine ID changed unexpectedly'

grep -q 'BR2_PACKAGE_OS_AGENT_BOARD="GenericAmd64"'   buildroot-external/configs/generic_x86_64_defconfig   || fail 'generic x86-64 OS Agent board ID changed unexpectedly'

python3 - <<'PY'
import json
from pathlib import Path

for path in [
    Path("grol/specs/action-request.schema.json"),
    Path(".github/workflows/matrix.json"),
]:
    with path.open("r", encoding="utf-8") as f:
        json.load(f)
    print(f"JSON OK: {path}")
PY

echo "GROL foundation guardrails: PASS"
