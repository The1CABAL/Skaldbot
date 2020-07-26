#!/bin/bash
sudo docker run -it -p 5479:5479 --name skaldbot-test -d skaldbot-test && \ 
sleep 5 && \
sudo docker inspect -f {{.State.Running}} skaldbot-test && \
echo "Container is running."