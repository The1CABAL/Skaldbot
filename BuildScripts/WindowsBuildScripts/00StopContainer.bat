@echo on
@echo Stopping Container
docker kill skaldbotui
docker kill skaldbotapi
docker rm skaldbotui
docker rm skaldbotapi
docker rmi skaldbotui
docker rmi skaldbotapi
cd ../../SkaldBotUI/Offline
docker build --tag skaldbotoffline "./"
docker run --name skaldbotoffline -p 8080:8080 skaldbotoffline