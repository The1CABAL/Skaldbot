#!/bin/bash
sudo docker run -it -p 5478:5478 --name skaldbot -d skaldbot && \ 
sleep 5 && \
state = sudo docker inspect -f {{.State.Running}} skaldbot
if [$state == False] then
	exit 1
fi