#!/bin/bash
cp ../../jsons/SkaldBotToken.json ./SkaldBotCore/
cd ./SkaldBotCore/ && sudo docker build --tag skaldbotcore . && cd ~