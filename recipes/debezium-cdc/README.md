# Apache Pinot and Debezium Example for PostgreSQL

This recipe downloads a Postgres dump of change data capture (CDC) data about `dvdrentals` and stands up Kafka to connect with Debezium. CDC data is written to Kafka, which is then consumed by Apache Pinot.

This recipe executes all of the commands in a Makefile, which you can examine to understand the process. Examining the code will be the most useful part of this recipe.

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

Once that's completed, navigate to [localhost:9000/#/query](http://localhost:9000/#/query) to see the data in Apache Pinot.

## Clean Up

```bash
make clean
```

## Trouble Shooting

To clean up cruft from old Docker installations that may be interfering with your testing of this recipe, use this:

```bash
docker system prune
```
