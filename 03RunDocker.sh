#!/bin/bash
sudo docker run -it -p 5478:5478 --name skaldbot -d skaldbot && sudo docker inspect -f {{.State.Running}} skaldbot && echo "Container is running."