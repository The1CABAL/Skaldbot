@echo on
@echo Building API
copy ..\..\..\..\secretData\SkaldBot\config.ini ..\..\SkaldBotAPI
cd ../../SkaldBotAPI
docker build --tag skaldbotapi "./"