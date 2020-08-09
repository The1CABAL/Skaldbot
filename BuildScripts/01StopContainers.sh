#!/bin/bash
sudo docker stop skaldbotcore
sudo docker rm skaldbotcore
sudo docker stop skaldbotapi
sudo docker rm skaldbotapi
sudo docker stop skaldbotui
sudo docker rm skaldbotui
sudo docker start skaldbotoffline