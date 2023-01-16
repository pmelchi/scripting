#!/bin/bash

sudo apt update
sudo apt upgrade

sudo apt install ssh pdsh openjdk-8-jre -y

sudo mkdir /hadoop
sudo mkdir /hadoop/download
sudo chmod -R 777 /hadoop
wget -P /hadoop/download https://dlcdn.apache.org/hadoop/common/stable/hadoop-3.3.4.tar.gz
tar -xvzf /hadoop/download/hadoop-3.3.4.tar.gz -C /hadoop
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/" >> ~.profile

echo "Cleanin up other programs"
sudo apt autoremove