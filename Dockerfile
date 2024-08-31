FROM rust:slim

RUN useradd -ms /bin/sh user

WORKDIR /app

COPY network/main /app/network
COPY threshold-encryption/keys /app/keys

COPY threshold-encryption/target/release/silent-threshold /app/silent-threshold
COPY threshold-encryption/transcript-512 /app/transcript-512

COPY start.sh /app/start.sh

RUN chown -R user /app && \
    chmod +x /app/network && \
    chmod +x /app/silent-threshold && \
    chmod +x /app/start.sh

USER user

ENTRYPOINT ["/app/start.sh"]
