# 🚀 Discord Webhook Notification Service

Sistema de notificaciones basado en FastAPI que procesa y envía mensajes formateados a Discord a través de webhooks. Diseñado para ser fácil de usar y altamente personalizable.

## 🌟 Características

- 📝 Múltiples tipos de mensajes (INFO, ERROR, WARNING, SUCCESS, DEBUG, CRITICAL)
- 🎨 Formato personalizado con emojis y colores para cada tipo de mensaje
- ⚡ Procesamiento asíncrono en tiempo real
- 🔄 Reintentos automáticos con backoff exponencial
- 🔍 Validación robusta de mensajes
- 🐳 Containerización con Docker y healthchecks
- 🛡️ Seguridad mejorada con usuario no-root
- 📊 Endpoints de estado y monitoreo

## 📁 Estructura del Proyecto

```
discord-alert/
├── src/
│   ├── app/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── message.py      # Modelos Pydantic
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── input.py        # Validación de mensajes
│   │       ├── output.py       # Cliente Discord
│   │       └── process.py      # Lógica de procesamiento
│   ├── api.py                  # Endpoints FastAPI
│   └── __init__.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## 📋 Requisitos Previos

- 🐳 Docker y Docker Compose instalados
- 🔗 URL de webhook de Discord
- 🐍 Python 3.11 o superior (para desarrollo local)

## 🛠️ Instalación

1. Clona el repositorio
```bash
git clone https://github.com/yourusername/discord-alert
```

2. Configura las variables de entorno:
```env
DISCORD_WEBHOOK_URL=tu_url_de_webhook_aqui
```

3. Construye y ejecuta con Docker Compose:
```bash
docker-compose up -d
```

## 💻 Ejemplos de Uso

### Envío de Mensaje 📨
```bash
curl -X POST http://localhost:8000/webhook \
-H "Content-Type: application/json" \
-d '{
  "type": "INFO",
  "content": "Usuario login exitoso",
  "origin": "auth_service",
  "details": {
    "user_id": "123",
    "ip": "192.168.1.1"
  }
}'
```

### Verificación de Salud 🏥
```bash
curl http://localhost:8000/health
```

## 🎨 Tipos de Mensajes y Formatos

| Tipo | Color | Emoji | Símbolo | Uso |
|------|--------|-------|---------|-----|
| INFO | 🔵 #3498db | 📢 | ℹ️ | Información general |
| ERROR | 🔴 #e74c3c | ❌ | ⚠️ | Notificación de errores |
| WARNING | 🟡 #f1c40f | ⚠️ | ⚡ | Alertas y advertencias |
| SUCCESS | 🟢 #2ecc71 | 🎉 | ✅ | Mensajes de éxito |
| DEBUG | ⚪ #95a5a6 | 🐛 | 🔍 | Información de depuración |
| CRITICAL | 🔴 #992d22 | 💀 | 🚨 | Alertas críticas |

## 🐳 Comandos Docker

```bash
# Construir y levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f discord_alert

# Verificar estado
curl http://localhost:8000/health

# Detener servicios
docker-compose down
```

## 🧪 Testing

El proyecto utiliza pytest y pytest-asyncio para testing. Para ejecutar los tests:

```bash
# Instalar dependencias de desarrollo
pip install -r requirements.txt
```

## 📖 Documentación API

Cuando el servicio esté corriendo, puedes acceder a:
- 📝 Swagger UI: http://localhost:8000/docs
- 📚 ReDoc: http://localhost:8000/redoc

## 📜 Licencia

Este proyecto está bajo la Licencia Apache 2.0. Ver el archivo `LICENSE` para más detalles.

---
⭐ ¡No olvides dar una estrella al proyecto si te ha sido útil! ⭐
