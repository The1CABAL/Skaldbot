#!/bin/bash
sudo docker run -it -p 5478:5478 --name skaldbotcore -d skaldbotcore && /sleep 10 && sudo docker exec -t skaldbotcore echo "Core Container Is Running"