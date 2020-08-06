@echo on
TITLE Build UI Environment
ECHO Building UI...
@echo before
npm install @vue/cli
npm install @vue/cli-service
cd C:\Program Files (x86)\Go Agent\pipelines\UI-QA\SkaldBotUI
@echo after
npm run build
