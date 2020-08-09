@echo on
@echo Stopping Container
docker kill skaldbotui
docker kill skaldbotapi
docker rm skaldbotui
docker rm skaldbotapi
docker rmi skaldbotui
docker rmi skaldbotapi