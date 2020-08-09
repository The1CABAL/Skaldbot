#!/bin/bash
cp ../../jsons/config.ini ./SkaldBotAPI/
cd ./SkaldBotAPI/ && sudo docker build --tag skaldbotapi . && cd ~