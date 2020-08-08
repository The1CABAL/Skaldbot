#!/bin/bash
sudo docker run -it -p 8080:8080 --name skaldbotui -d skaldbotui --link skaldbotapi:skaldbotapi && sleep 10 && sudo docker exec -t skaldbotui echo "Api Container Is Running"