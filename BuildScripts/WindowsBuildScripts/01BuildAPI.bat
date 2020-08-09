@echo on
@echo Building API
cp ../../../../secretData/config.ini ../../SkaldBotAPI
cd ../../SkaldBotAPI
docker build --tag skaldbotapi "./"