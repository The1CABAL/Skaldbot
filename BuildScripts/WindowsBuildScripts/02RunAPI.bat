@echo on
@echo Starting API
docker run -p 192.168.1.33:5555:5555 --name skaldbotapi -d skaldbotapi