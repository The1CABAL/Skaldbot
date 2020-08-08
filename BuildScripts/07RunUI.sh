#!/bin/bash
sudo docker run -it -p 8080:5480 --name skaldbotapi -d skaldbotapi && sleep 10 && sudo docker exec -t skaldbotapi echo "Api Container Is Running"