# Mesa Larga - Restaurant Reservations Backend
## Instrucciones para ejecutar el proyecto

1. Clonar el repositorio
2. **Requisitos previos**: Tener instalado Docker y Docker Compose
3. **Configuracion**: Crear un archivo `.env` en la raíz basado en `.env.example`
4. Ejecutar el siguiente comando para levantar toda la infraestructura:
```
docker compose up --build -d
```
(La base de datos, las migraciones, la creación del superusuario y el seeding de los registros se ejecutarán de forma completamente automática en el primer arranque)

## Decisiones de Diseño y Trade-offs
- **Arquitectura**: Se implementó una separación de preocupaciones. El Django Admin (servido vía Gunicorn) gestiona exclusivamente la escritura y configuración administrativa. FastAPI (servido vía Uvicorn) gestiona el alto volumen de tráfico de lectura pública. Ambos comparten la base de datos PostgreSQL en el esquema content, pero operan de forma independiente aplicando el principio de Inversión de Dependencias y Patrones de Repositorio/Servicio
- **Caché y Degradación:** Se utiliza Redis para cachear respuestas de lista y detalle. Estrategia: Cache-Aside. Si Redis no es alcanzable, el sistema captura la excepción y redirige la consulta directamente a PostgreSQL para garantizar la disponibilidad
- **Timezone**: El manejo de tiempo es timezone-aware mediante la librería zoneinfo, la disponibilidad calcula el offset dinámico enviado por el cliente
- **Búsqueda Textual**: Se utilizó el operador nativo ILIKE de PostgreSQL en lugar de herramientas externas (como Elasticsearch) para mantener la infraestructura simple y cumplir con los requerimientos técnicos
- **Paginación**: Estandarizada mediante parámetros limit y offset inyectados desde el router hasta la base de datos para optimizar la transferencia de memoria


## Como probar el sistema
Ejecuta la suite de pruebas desde el contenedor de FastAPI para validar la lógica:
```
docker-compose exec fastapi pytest -v
```
### Endpoints Principales
**Frontend / Aplicación Web:** http://localhost/

**Panel de Administración (Django):** http://localhost/admin/

**Documentación OpenAPI (Swagger):** http://localhost/api/v1/openapi.json y http://localhost/docs

**Healthcheck**: http://localhost/api/v1/healthz y http://localhost/healthz/ (Retorna 200/503 según estado)

**Prueba de 404**: http://localhost/rutainvalida

## Manejo de Condiciones de Carrera
- Lógica de Negocio (Inventory / Capacity Enforcement): Si el cálculo de disponibilidad se implementa de manera ingenua (ej. obteniendo el número en memoria y restando), múltiples lecturas simultáneas podrían permitir la sobreventa de mesas (Overbooking)
- Solución aplicada: El sistema delega la verdad a la base de datos, se calcula la ocupación sumando dinámicamente el tamaño de los grupos (party_size) de todas las reservas con estado CONFIRMED usando una función de agregación (GROUP BY y SUM) en PostgreSQL al momento exacto de la petición

## Submission Reflection 
_La decisión por la que me siento mas orgullosa_:
Me siento orgullosa por la implementación de la capa de caché de Redis, la organización de las capas del proyecto y la limitación de velocidad en FastAPI, ambas funcionalidades cumplen con el requisito de "Graceful Degradation", cuando el contenedor de Redis no está disponible el sistema captura las excepciones de conexión y omite el caché para hacer consultas directamente a Postgres y la API sigue disponible

_La decisión que menos me satisface_:
Hay algunos enfoques de reserva en cuanto a la logica de negocio implementada en la API, el frontend llama a endpoints como /menu/ sin especificar un restaurant_id, dado que se daba un Restaurante como entidad diseñé el backend para que se capture el primer restaurante disponible, hubo una gran confusión de mi parte en cuanto al documento por lo que no me siento orgullosa de muchas decisiones que tome al realizar el modelado de la base de datos