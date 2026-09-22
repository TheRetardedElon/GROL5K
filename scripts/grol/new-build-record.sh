#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

target="${1:-ova}"
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
out="docs/build-records/DRAFT-${stamp}-${target}.md"

mkdir -p docs/build-records

grol_sha="$(git rev-parse HEAD)"
buildroot_sha="$(git submodule status buildroot 2>/dev/null | awk '{print $1}' | sed 's/^[+-]//' || true)"
docker_version="$(docker --version 2>/dev/null || echo 'not detected')"
host="$(uname -a 2>/dev/null || echo 'unknown')"

cat > "$out" <<EOF
# GROL5K Build Record — DRAFT

- Timestamp (UTC): $stamp
- Target: $target
- GROL5K commit: $grol_sha
- Buildroot submodule: ${buildroot_sha:-unknown}
- Host: $host
- Docker: $docker_version

## Build command

~~~text
TODO
~~~

## Result

- [ ] build started
- [ ] build completed
- [ ] artifacts hashed
- [ ] VM/target booted
- [ ] boot checklist completed

## Artifacts

| Artifact | SHA-256 | Notes |
|---|---|---|
| TODO | TODO | |

## Boot observations

TODO

## Relevant logs

TODO

## Failures / deviations

TODO

## Conclusion

TODO — this draft is not evidence that M0 passed until the checklist and real boot validation are complete.
EOF

echo "$out"
