#!/bin/bash
sudo docker run -it -p 192.168.1.11:5555:5555 --name skaldbotapi -d skaldbotapi && sleep 10 && sudo docker exec -t skaldbotapi echo "Api Container Is Running"