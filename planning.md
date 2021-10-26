# Planificación

A continuación se lista, por cada versión mayor, las funcionalidades, mejoras o ideas que incorporarán.

# Formato de etiquetas Git

Para este proyecto se usarán etiquetas para identificar los commits que incluyen todos los avances necesarios para cerrar una versión dada. El formato (en expresión regular) será el siguiente:

```re
^v([0-9]\.?){1,4}(-\w+)?$
```

Este formato permitirá la existencia de etiquetas que identifiquen versiones con hasta 4 niveles de profundidad, por ejemplo: `v0.1.2.3`. Además, la parte final hará posible que se añadan descriptores adicionales para versiones especiales, por ejemplo: `v0.1-rc1` o `v0.1-fastapi`.

## Metodología de programación y características transversales

Estas características serán incorporadas a todas las versiones:

* TDD: Se desarrollarán los tests unitarios y posteriormente se trabajará sobre la implementación de los servicios.
* Etiquetado de tipos (type hinting).
* Aplicar concurrencia en el servidor web y gestionar las llamadas externas con paralelismo.
* Inyección de dependencias.
* Tests de estrés (con jMeter o Postman).
* Identificación de versiones en repositorio con tags Git.
* Zen of Python (PEP 20) y Guía de estilos para código Python (PEP 8).


# Versiones

## Versión 0.1

* Pilares de la aplicación terminados: 
    * Tornado.
    * API REST.
    * Implementación de clases de mapeo en ORM.
    * Esquema inicial de excepciones. 
    * Esquema de proyecto (archivos).
    * Conexión a base de datos.
    * Gestor de configuración para proteger contraseñas y organizar archivos -> Dynaconf.
* Servicios y API incluidos:
    * Alta.
    * Listar datos de usuario (datos personales + intereses).
* Tests unitarios para los servicios desarrollados.

## Versión 0.2

* Sistema de logging a fichero con rotación diaria.
* Servicios y API incluidos:
    * Baja de cuenta de usuario (lógica).
    * Modificación de suscripciones RSS de usuarios.
        * Suscribirse a un nuevo sitio RSS.
        * Ordenar.
        * Eliminar suscripción.
* Tests unitarios para los servicios desarrollados.

## Versión 0.3

* Servicios y API incluidos:
    * Modificación de datos de usuario (datos personales + intereses).  
    * Actualizar suscripciones RSS de un usuario (volver a pedir noticias vía internet).
* Tests unitarios para los servicios desarrollados.
* Nginx.
* Supervisor.

# POR PLANIFICAR


* Generador de documentación Swagger con Tornado.
* Cacheo para API (envío de cabeceras).
* Anotar todos los eventos del sistema en una nueva tabla de base de datos ("eventos"). Deberá evaluarse si puede hacerse con muy poco impacto al sistema y a la base de datos, anotando la información mínima indispensable. Se recomienda incluir el código como decorador o metaclase. 
* Verificación de correo electrónico en alta de cuenta. Agregar soporte para reconocer usuarios activos o inactivos y usuarios con email verificado o no verificado. El proceso de alta se modificará para que fije al usuario como inactivo y con email no verificado (enviando un email para que active la cuenta a su vez), lo cual le impedirá hacer login hasta que lo verifique. Se deberá crear otra sección para reenviar el correo electrónico de activación desde el servicio de login. Estos correos deben tener un tiempo de expiración y su envío deberá anotarse en la base de datos, con fecha, usuario y resultado (tabla eventos).
* Agregar una clasificación para cada feed RSS por popularidad (investigar si esta información existe). También se pueden usar otros criterios, como: 
    * Rapidez a la hora de publicar noticias.
    * Número medio de noticias publicadas por día.
    * Independencia ideológica/libertad del medio de comunicación.
* Soporte a APML, tanto para importar preferencias de usuario como para exportarlas.
* Sugerir al usuario qué feeds podrían interesarles, ordenados por los criterios listados en el punto 1 de esta lista. El usuario podrá ir eligiendo uno a uno. Esto debería ser una nueva sección de la aplicación, evitando ser invasiva.
* Soportar conectores a los sistemas gestores de bases de datos más populares: PostgreSQL, MySQL, Oracle, etc...
* Dockerizar aplicación y orquestarla con Kubernetes.
* Sistema de privilegios, perfiles y acciones.
* Aplicar principios SOLID. Se comenzó el curso de Udemy pero el modificar mi forma de programar para incorporar estos principios llevará tiempo que no tengo para la versión 0.1.
* Nueva versión con FastAPI + GEvent como servidor web.
* Uso de PyODBC como capa de abstracción.
* GraphQL que coexista con el API REST.
* Configuración de Supervisor.
* Instalación y configuración de Nginx.
* Usar long polling para simular conexiones siempre abiertas entre cliente y servidor: https://en.wikipedia.org/wiki/Push_technology#Long_polling. Tornado funciona muy bien con esta técnica, por lo visto.

## Requerimientos descartados:

* Login y generación y mantenimiento de sesiones. Mecanismo para evitar que dos sesiones tengan el mismo ID (hash): Tanto API REST como GraphQL son "stateless". No se deberá almacenar ningún estado del usuario en el sistema. Cada petición deberá poder procesarse tantas veces como sea necesario sin problema alguno: Esto generaría un problema en un sistema tradicional para con el servicio de login, por ejemplo.
