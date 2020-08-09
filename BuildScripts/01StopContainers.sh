#!/bin/bash
sudo docker stop skaldbotcore && sleep 2|| \
sudo docker rm skaldbotcore && sleep 2 || \
sudo docker stop skaldbotapi && sleep 2 || \
sudo docker rm skaldbotapi && sleep 2|| \
sudo docker stop skaldbotui && sleep 2|| \
sudo docker rm skaldbotui && sleep 2|| \
sudo docker start skaldbotoffline || \
echo "All Containers stopped and maintenance page is active."