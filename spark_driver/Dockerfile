FROM ubuntu:20.04
FROM python:3.7-slim

WORKDIR /spark-driver

USER root

COPY . ./

RUN apt update

RUN apt install -y openjdk-11-jdk

RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

RUN echo 'export SPARK_HOME=/spark-driver/spark-3.1.3-bin-hadoop3.2' >> ~/.bashrc

RUN pip3 install -r requirements.txt --user

CMD tail -f /dev/null
