#!/bin/bash
cp ../../jsons/config.ini ./SkaldBotCore/
cd ./SkaldBotAPI/ && sudo docker build --tag skaldbotapi . && cd ~