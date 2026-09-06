# Flagsmith Connector — Discovery

**Vendor:** Flagsmith (https://flagsmith.com)  
**API Base URL:** `https://api.flagsmith.com/api/v1`  
**Authentication:** Master API Key (Authorization: Token <key>)

## Архитектура API
- **Ключевые сущности:** проекты (/projects), фичи/флаги (/features), окружения (/environments), состояния фич (/feature-states)
- **Формат обмена данными:** JSON / HTTPS REST.
- **Обработка ошибок:** Стандартные HTTP-коды (400, 401, 403, 404, 429, 500) с типизацией ответа.
- **Тестовая точка проверки подключения:** `GET /api/v1/projects/`.
