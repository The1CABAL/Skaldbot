@echo on
@echo Building API
copy ..\..\..\..\secretData\config.ini ..\..\SkaldBotAPI
cd ../../SkaldBotAPI
docker build --tag skaldbotapi "./"