@echo on
TITLE Build UI Environment
ECHO Building UI...
@echo before
cd C:\Program Files (x86)\Go Agent\pipelines\UI-QA\SkaldBotUI
npm install @vue/cli
npm install @vue/cli-service
@echo after
npm run build
