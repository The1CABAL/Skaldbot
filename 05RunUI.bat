@echo on
TITLE Build UI Environment
ECHO Building UI...
START cmd.exe /k "cd C:\Program Files (x86)\Go Agent\pipelines\UI-QA\SkaldBotUI&npm run build"
