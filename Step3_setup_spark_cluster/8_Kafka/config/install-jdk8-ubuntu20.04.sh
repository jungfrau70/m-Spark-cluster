#!/bin/bash
apt-get install -y wget

apt-get update -y && apt-get install -y software-properties-common
apt-get update -y && apt-get install -y openjdk-11-jre
java --version