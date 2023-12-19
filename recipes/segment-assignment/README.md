# Segment Assignment

> In this recipe we'll learn how to force commit segments.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>1.0.0</td>
  </tr>
  <tr>
    <td>Schema</td>
    <td><a href="config/pinot-events.yml">Schema and Table Config</a></td>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/segment-assignment

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/segment-assignment
```

Create Kubernetes cluster
```
kind create cluster
```

Spin up a Pinot cluster using Kubernetes

```bash
helm repo add pinot https://raw.githubusercontent.com/apache/pinot/master/kubernetes/helm
kubectl create ns pinot-quickstart
helm install pinot pinot/pinot \
    -n pinot-quickstart \
    --set cluster.name=pinot \
    --set server.replicaCount=4
```

Add tables and schema:

```bash
kubectl apply -f config/pinot-events.yml
```

Port Forward Pinot UI on port `9000`

```bash
kubectl port-forward service/pinot-controller 9000:9000 -n pinot-quickstart
```

Start Kafka cluster

```bash 
helm repo add kafka https://charts.bitnami.com/bitnami
helm install -n pinot-quickstart kafka kafka/kafka --set replicas=1,zookeeper.image.tag=latest
```

Port forward Kafka on port 9090

```bash
kubectl port-forward service/kafka-headless 9092:9092 -n pinot-quickstart
```

Add following line to `/etc/hosts`

```
127.0.0.1 kafka-0.kafka-headless.pinot-quickstart.svc.cluster.local
```

Ingest data into Kafka

```bash
python datagen.py --sleep 0.0001 2>/dev/null |
jq -cr --arg sep ø '[.uuid, tostring] | join($sep)' |
kcat -P -b localhost:9092 -t events -Kø
```

Install script dependencies + run script

```bash
pip install click ordered-set requests
python segments_to_server.py
```
