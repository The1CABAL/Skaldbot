@echo on
@echo Starting UI
docker run -p 8080:8080 --name skaldbotui --link skaldbotapi:skaldbotapi -d skaldbotui