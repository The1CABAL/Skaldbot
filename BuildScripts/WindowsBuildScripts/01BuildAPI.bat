@echo on
@echo Building API
xcopy /s ../../../../secretData/config.ini d:../../SkaldBotAPI
cd ../../SkaldBotAPI
docker build --tag skaldbotapi "./"