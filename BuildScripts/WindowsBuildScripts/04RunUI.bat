@echo on
@echo Starting UI
docker kill skaldbotoffline
docker rm skaldbotoffline
docker rmi skaldbotoffline
docker run -p 8080:8080 --name skaldbotui --link skaldbotapi:skaldbotapi -d skaldbotui