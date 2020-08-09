@echo on
@echo Stopping Container
docker kill skaldbot-ui
docker rm skaldbot-ui
docker rmi skaldbotui