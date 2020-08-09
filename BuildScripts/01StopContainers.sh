#!/bin/bash
sudo docker stop skaldbotcore || \
sleep 3 && sudo docker rm skaldbotcore  || \
sleep 3 && sudo docker stop skaldbotapi  || \
sleep 3 && sudo docker rm skaldbotapi || \
sleep 3 && sudo docker stop skaldbotui || \
sleep 3 && sudo docker rm skaldbotui || \
sleep 3 && sudo docker start skaldbotoffline  || \
echo "All Containers stopped and maintenance page is active."