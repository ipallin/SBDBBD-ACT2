#!/bin/bash
set -euo pipefail

DATA_DIR="/var/lib/postgresql/data"
CERT_SRC="/tls/pg_server.crt"
KEY_SRC="/tls/pg_server.key"
CERT_DEST="${DATA_DIR}/server.crt"
KEY_DEST="${DATA_DIR}/server.key"

if [ -f "${CERT_SRC}" ] && [ -f "${KEY_SRC}" ]; then
    if [ ! -f "${CERT_DEST}" ] || [ ! -f "${KEY_DEST}" ]; then
        cp "${CERT_SRC}" "${CERT_DEST}"
        cp "${KEY_SRC}" "${KEY_DEST}"
        chown postgres:postgres "${CERT_DEST}" "${KEY_DEST}"
        chmod 600 "${KEY_DEST}"
        chmod 600 "${CERT_DEST}"
    fi
else
    echo "TLS certificates not found in /tls. Skipping Postgres TLS setup." >&2
fi
