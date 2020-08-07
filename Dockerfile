FROM alpine:3.10

COPY audit.sh /audit.sh

ENTRYPOINT ["/audit.sh"]
