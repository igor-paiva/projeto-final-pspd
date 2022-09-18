# Projeto Final

Igor Batista Paiva - 18/0018728

## Sobre

Para executar será necessário ter instalado o `docker` e `docker-compose`.

## Configuração

Para instalar todas as dependências e criar todos os elementos necessários utilize o comando abaixo:

```
bash setup.sh
```

## Como executar

Após ter rodado o *setup* com sucesso para iniciar novamente só é necessário subir os containers e seguir os demais passos:

```
docker-compose up -d
```

Os containers sobem em modo *detach*, portanto caso queira ver os logs dos containers utilize:

```
docker-compose logs -f
```

### Iniciar o master

Será necessário iniciar o spark master:

```
docker exec -it spark-master bash spark-3.1.3-bin-hadoop3.2/sbin/start-master.sh
```

### Iniciar os workers

Para iniciar os *workers*:

```
docker exec -it spark-worker-1 bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh -m 1G -c 1 spark://spark-master:7077 && docker exec -it spark-worker-2 bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh -m 1G -c 1 spark://spark-master:7077
```

### Iniciar o publisher

O publisher envia eventos para o servidor Kafka a cada meio segundo (0,5 segundo) com um paragrafo de texto.

Em um novo terminal (a chamada é blocante):

```
docker exec -it kafka-publisher bash

# dentro do container
python3 -u main.py
```

Para encerrar: `CTRL + C`.

### Submeter o problema

Em um novo terminal entre no container do spark driver:

```
docker exec -it spark-driver bash
```

Para submeter o problema utilize um dos comandos abaixo, o arquivo txt no final é para onde os resultados serão salvos.

#### Local

Para o modo local não é necessário iniciar o spark master e workers.

```
./spark-3.1.3-bin-hadoop3.2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3 local.py > results.txt
```

#### Cluster

```
./spark-3.1.3-bin-hadoop3.2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3 cluster.py > results.txt
```

## Resultados

Os resultados serão listados como tabelas com nomes de colunas descritivos no arquivo texto fornecido como saída para o comando `spark-submit`.
