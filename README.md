# 🚀 Discord Webhook Notification System

Sistema de notificaciones basado en FastAPI que procesa y envía mensajes formateados a Discord a través de webhooks. Diseñado para ser fácil de usar y altamente personalizable.

## 🌟 Características

- 📝 Múltiples tipos de mensajes (INFO, ERROR, WARNING, SUCCESS, DEBUG, CRITICAL)
- 🎨 Formato personalizado para cada tipo de mensaje
- ⚡ Procesamiento en tiempo real
- 🐳 Containerización con Docker
- 🔄 Recarga automática durante desarrollo
- 🤖 Integración con Discord

## 📁 Estructura del Proyecto

```
project/
├── app/
│   ├── __init__.py
│   ├── input_handler.py    # Rutas FastAPI y validación
│   ├── processor.py        # Procesamiento y formato
│   └── output_handler.py   # Comunicación con Discord
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## 📋 Requisitos Previos

- 🐳 Docker y Docker Compose instalados
- 🔗 URL de webhook de Discord
- 🐍 Python 3.11 o superior (para desarrollo local)

## 🛠️ Instalación

1. Clona el repositorio
```bash
git clone https://github.com/qmatiaslopez/discord-alert
```

2. Crea un archivo `.env`:
```env
DISCORD_WEBHOOK_URL=tu_url_de_webhook_aqui
```

3. Construye y ejecuta con Docker Compose:
```bash
docker-compose up -d
```

## 💻 Ejemplos de Uso

### 1. Alerta de Seguridad 🔒
```bash
curl -X POST http://localhost:8000/webhook \
-H "Content-Type: application/json" \
-d '{
  "type": "ERROR",
  "content": "Actividad sospechosa detectada",
  "origin": "monitor_seguridad",
  "details": {
    "ip_address": "45.123.45.67",
    "location": "Desconocida",
    "intentos_fallidos": "5"
  }
}'
```

### 2. Notificación de Despliegue 🚀
```bash
curl -X POST http://localhost:8000/webhook \
-H "Content-Type: application/json" \
-d '{
  "type": "SUCCESS",
  "content": "Despliegue completado",
  "origin": "pipeline_ci",
  "details": {
    "version": "v2.3.4",
    "tiempo": "45s",
    "ambiente": "produccion"
  }
}'
```

## 🎨 Tipos de Mensajes

| Tipo | Color | Icono | Uso |
|------|--------|------|----------|
| INFO | Azul | ℹ️ | Información general |
| ERROR | Rojo | ⚠️ | Notificación de errores |
| WARNING | Amarillo | ⚡ | Alertas y advertencias |
| SUCCESS | Verde | ✅ | Mensajes de éxito |
| DEBUG | Gris | 🔍 | Información de depuración |
| CRITICAL | Rojo Oscuro | 🚨 | Alertas críticas |

## 👩‍💻 Desarrollo Local

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecuta con uvicorn:
```bash
uvicorn app.input_handler:app --reload
```

## 🐳 Comandos Docker

```bash
# Construir el contenedor
docker-compose build

# Iniciar el servicio
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener el servicio
docker-compose down
```

## 📖 Documentación API

Cuando el servicio esté corriendo, puedes acceder a:
- 📝 Swagger UI: http://localhost:8000/docs
- 📚 ReDoc: http://localhost:8000/redoc

## 📜 Licencia

Este proyecto está bajo la Licencia Apache 2.0. Ver el archivo `LICENSE` para más detalles.

---
⭐ ¡No olvides dar una estrella al proyecto si te ha sido útil! ⭐