# syntax=docker/dockerfile:1

ARG RUNTIME_IMAGE
FROM ${RUNTIME_IMAGE} AS reviewed-runtime

FROM scratch AS gateway
LABEL org.dotskills.evaluate.contract="provider-gateway-v0.4" \
      org.dotskills.evaluate.status="unverified"

COPY --from=reviewed-runtime /opt/evaluate/bin/python3 /opt/evaluate/bin/python3
COPY --chown=65532:65532 gateway-entrypoint.py /opt/evaluate/gateway-entrypoint.py

USER 65532:65532
WORKDIR /var/lib/evaluate-gateway
ENTRYPOINT ["/opt/evaluate/bin/python3", "/opt/evaluate/gateway-entrypoint.py"]
CMD ["serve", "--binding", "/run/evaluate/gateway-binding.json", "--replay-ledger", "/var/lib/evaluate-gateway/replay"]
