FROM jenkins/jenkins:lts

USER root


RUN jenkins-plugin-cli --plugins workflow-aggregator git docker-workflow


RUN apt-get update && apt-get install -y \
    qemu-system qemu-user-static wget unzip expect python3 python3-pip \
    && pip3 install selenium pytest locust \
    && rm -rf /var/lib/apt/lists/*

USER jenkins

EXPOSE 8080
EXPOSE 50000