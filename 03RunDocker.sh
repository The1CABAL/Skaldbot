#!/bin/bash
sudo docker run -it -p 5478:5478 --name skaldbot-test -d skaldbot-test && \ 
sleep 5 && \
sudo docker inspect -f {{.State.Running}} skaldbot-test && \
echo "Container is running."