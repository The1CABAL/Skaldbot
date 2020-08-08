#!/bin/bash
sudo docker run -it -p 5478:5478 --name skaldbotapi -d skaldbotapi && sleep 10 && sudo docker exec -t skaldbotapi echo "Api Container Is Running"