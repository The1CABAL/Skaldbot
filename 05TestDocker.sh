if sudo docker inspect -f {{.State.Running}} skaldbot
then
    exit 0
else
    exit 1
fi