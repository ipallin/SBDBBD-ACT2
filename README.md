# SBDBBD-ACT2

Actividad 2 para la asignatura de Seguridad en Bases de Datos, Blockchain y Big Data. El objetivo es comparar una arquitectura insegura frente a una versión endurecida que protege los motores PostgreSQL y MySQL con TLS, roles mínimos, cifrado de datos y rutinas de respaldo.

## Estructura del repositorio

```
SBDBBD-ACT2/
├── app/
│   ├── app.env                 # Credenciales y claves usadas por la app segura
│   ├── requiremewnts.txt       # Dependencias del cliente Python (psycopg2, PyMySQL, cryptography)
│   ├── seguro.py               # Cliente seguro: consultas parametrizadas y pgcrypto
│   └── vulnerable.py           # Cliente vulnerable usado en la versión insegura
├── backups/
│   ├── backup_mysql.sql        # Ejemplo de dump MySQL
│   └── backup_pg.dump          # Ejemplo de dump PostgreSQL
├── docker-compose.yaml         # Orquestación endurecida con TLS y volúmenes de backup
├── sql/
│   ├── init_mysql.sql          # Esquema inicial de productos
│   ├── init_mysql_audit.sql    # Usuario app con privilegios mínimos
│   ├── init_mysql_tls.sh       # Copia los certificados TLS al contenedor
│   ├── init_postgres.sql       # Esquema inicial de usuarios
│   ├── init_postgres_audit.sql # Roles, logging, pgcrypto y cifrado de emails
│   └── init_postgres_tls.sh    # Copia los certificados TLS al contenedor
├── tls/
│   ├── mysql_server.crt/key    # Certificado y clave del servidor MySQL
│   ├── pg_server.crt/key       # Certificado y clave del servidor PostgreSQL
│   └── mysql_ssl.cnf           # Configuración extra para habilitar SSL en mysqld
└── .inseguros-archivo/
    └── docker-compose.yaml     # Variante inicial e insegura (auth relajada, sin TLS)
```

## Servicios orquestados

| Servicio  | Puerto | Credenciales principales                              | Notas |
|-----------|--------|--------------------------------------------------------|-------|
| postgres  | 5432   | postgres / SuperPg#2025 (admin)                        | TLS con `server.crt`/`server.key`, rol `appuser` con pgcrypto |
| mysql     | 3306   | root / SuperMy#2025 (admin)                            | TLS configurado desde `tls/mysql_ssl.cnf`, rol `app` mínimo |
| app       | n/a    | Lee variables desde `app/app.env`                     | Instala dependencias y lanza `seguro.py` interactivo |

Todos los contenedores comparten la carpeta `./backups`, montada en `/backups` para realizar dumps o restauraciones.

## Puesta en marcha

1. **Requisitos previos**: Docker y Docker Compose v2 instalados en el host.
2. **Certificados**: coloca los ficheros TLS en `tls/` (`pg_server.crt`/`pg_server.key`, `mysql_server.crt`/`mysql_server.key`). El script de arranque los copiará dentro de cada motor con permisos `600`.
3. **Iniciar el entorno**:
   ```bash
   cd SBDBBD-ACT2
   sudo docker compose up -d
   ```
   La primera vez se inicializan esquemas, roles, logging y se cifran emails existentes con `pgcrypto`.
4. **Ver el cliente seguro**:
   ```bash
   sudo docker compose attach app
   ```
   El menú permite buscar usuarios (descifrando `email_enc`), insertar productos o listarlos usando consultas parametrizadas.

## Conexiones seguras

- PostgreSQL:
  ```bash
  PGPASSWORD=SuperPg#2025 psql \
    "host=localhost user=postgres dbname=postgres sslmode=require"
  ```
- MySQL:
  ```bash
  mysql --host=127.0.0.1 --protocol tcp -uroot -pSuperMy#2025 \
    --ssl-mode=REQUIRED --ssl-ca=tls/mysql_server.crt
  ```
  Dentro puedes comprobar `SHOW STATUS LIKE 'Ssl_cipher';`.

## Copias de seguridad

La carpeta `backups/` se monta dentro de ambos motores. Ejemplos:

- Dump PostgreSQL:
  ```bash
  sudo docker compose exec postgres \
    bash -lc "PGPASSWORD='$POSTGRES_PASSWORD' pg_dump \
      --format=c --dbname=\"postgresql://postgres:$POSTGRES_PASSWORD@localhost:5432/postgres?sslmode=require\" \
      --file=/backups/backup_pg.dump"
  ```
- Dump MySQL:
  ```bash
  sudo docker compose exec mysql \
    mysqldump -uroot -p$MYSQL_ROOT_PASSWORD --ssl-mode=REQUIRED \
      tienda > backups/backup_mysql.sql
  ```

Para restaurar, invierte los comandos empleando `pg_restore` o `mysql < backups/…` dentro del contenedor.

## Comparativa con la versión insegura

El directorio `.inseguros-archivo/` conserva el `docker-compose.yaml` original utilizado para demostrar malas prácticas: contraseñas vacías, `POSTGRES_HOST_AUTH_METHOD=trust`, sin TLS ni roles mínimos. Sirve como referencia directa de los vectores mitigados en la versión principal del repositorio.

## Personalización

- Ajusta usuarios/contraseñas en `app/app.env` y en `docker-compose.yaml` si deseas regenerar claves.
- Sustituye los certificados por otros emitidos por tu CA; los scripts de `sql/*tls.sh` copiarán los nuevos valores en el arranque.
- Extiende los scripts `sql/init_*.sql` para añadir más tablas o reglas de auditoría según tus necesidades.
