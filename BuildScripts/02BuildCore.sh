#!/bin/bash
cp ../../jsons/SkaldBotToken.json ./SkaldBotCore/
cp ../../jsons/config.ini ./SkaldBotCore/
cd ./SkaldBotCore/ && sudo docker build --tag skaldbotcore . && cd ~