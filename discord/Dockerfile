FROM ubuntu:20.04
FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/discord

WORKDIR /discord

COPY . ./

RUN apt update

RUN apt install -y openjdk-11-jdk

RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

RUN pip3 install -r requirements.txt

# ENTRYPOINT [ "python3", "-u", "./main.py" ]

CMD tail -f /dev/null
