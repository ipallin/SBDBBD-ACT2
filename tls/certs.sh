
#!/usr/bin/env bash
set -euo pipefail

# Genera certificados autofirmados para PostgreSQL y MySQL.
# Requiere openssl instalado en el sistema.

DIR=$(cd "$(dirname "$0")" && pwd)

POSTGRES_KEY="${DIR}/pg_server.key"
POSTGRES_CRT="${DIR}/pg_server.crt"
MYSQL_KEY="${DIR}/mysql_server.key"
MYSQL_CRT="${DIR}/mysql_server.crt"

if ! command -v openssl >/dev/null 2>&1; then
	echo "openssl no está instalado. Instálalo antes de ejecutar este script." >&2
	exit 1
fi

generate_cert() {
	local key_file="$1"
	local crt_file="$2"
	local cn="$3"

	if [[ -f "$key_file" || -f "$crt_file" ]];
	then
		echo "Saltando ${cn}: ya existen ${key_file} y/o ${crt_file}." >&2
		return
	fi

	openssl req -x509 -nodes -newkey rsa:4096 \
		-keyout "$key_file" \
		-out "$crt_file" \
		-days 365 \
		-subj "/CN=${cn}" \
		-addext "subjectAltName=DNS:${cn},DNS:localhost"

	chmod 600 "$key_file"
	chmod 644 "$crt_file"
	echo "Generado certificado para ${cn}."
}

generate_cert "$POSTGRES_KEY" "$POSTGRES_CRT" "postgres.local"
generate_cert "$MYSQL_KEY" "$MYSQL_CRT" "mysql.local"

echo "Certificados listos en ${DIR}."
