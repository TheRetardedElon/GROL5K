# GROL5K Build Records

This directory stores evidence for significant builds and boot tests.

A build record is not a release note. It is an engineering artifact that captures enough information to reproduce and evaluate a build.

Create a draft with:

```bash
scripts/grol/new-build-record.sh ova
```

For M0, records should include:

- GROL5K commit SHA
- Buildroot submodule SHA
- host/build environment
- exact build command
- output artifact names and SHA-256 hashes
- boot observations
- relevant logs
- failures/deviations
- conclusion against the M0 checklist

Do not mark M0 complete from a successful compile alone; the image must boot and satisfy the validation checklist.
