# Flagsmith Connector — Auth & Credentials Standard

**Compliance:** AUTH_AND_CREDENTIALS_STANDARD.md (B1–B10)

## Схема аутентификации
- **Метод:** Master API Key (Authorization: Token <key>)
- **Хранение:** Секреты сохраняются изолированно в хранилище секретов платформы Imperal.
- **Валидация:** При сохранении ключа выполняется тестовый запрос `GET /api/v1/projects/`.
- **Отключение:** Удаление локальных ключей без воздействия на аккаунт вендора.
