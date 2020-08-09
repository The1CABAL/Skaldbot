#!/bin/bash
cp ../../jsons/config.ini ./SkaldBotApi/
cd ./SkaldBotAPI/ && sudo docker build --tag skaldbotapi . && cd ~