#!/bin/bash
sudo docker run -it -p 8080:8080 --name skaldbotui --link skaldbotapi:skaldbotapi -d skaldbotui && sleep 10 && sudo docker exec -t skaldbotui echo "Api Container Is Running"