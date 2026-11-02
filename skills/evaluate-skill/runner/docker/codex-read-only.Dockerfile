# syntax=docker/dockerfile:1

# RUNTIME_IMAGE has no default. The trusted host supplies one reviewed
# name@sha256:<digest> value from the verified image lock at build time.
ARG RUNTIME_IMAGE
FROM ${RUNTIME_IMAGE} AS reviewed-runtime

FROM scratch AS workload
LABEL org.dotskills.evaluate.contract="docker-only-v0.4" \
      org.dotskills.evaluate.provider="codex" \
      org.dotskills.evaluate.profile="read-only" \
      org.dotskills.evaluate.status="unverified"

COPY --from=reviewed-runtime /opt/evaluate/bin/python3 /opt/evaluate/bin/python3
COPY --from=reviewed-runtime /opt/evaluate/bin/node /opt/evaluate/bin/node
COPY --from=reviewed-runtime /opt/evaluate/bin/codex /opt/evaluate/bin/codex
COPY --from=reviewed-runtime /opt/evaluate/bin/promptfoo /opt/evaluate/bin/promptfoo
COPY --chown=65532:65532 codex-entrypoint.py /opt/evaluate/codex-entrypoint.py

USER 65532:65532
WORKDIR /workspace
ENTRYPOINT ["/opt/evaluate/bin/python3", "/opt/evaluate/codex-entrypoint.py"]
