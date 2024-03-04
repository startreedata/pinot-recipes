# Apache Pinot and Debezium Example for MySQL

```mermaid
flowchart LR

d[DVDRental Dump]-->pg

subgraph pg[PostgreSQL]
Postgres
c[Kafka Connect]
end

pg-->k[Kafka]
k-->p[Apache Pinot]

```

Spin up a Pinot cluster using the Makefile, which uses Docker compose:

```bash
make recipe
```

## Clean Up

```bash
make clean
```

## Trouble Shooting

```bsah
docker system prune
```