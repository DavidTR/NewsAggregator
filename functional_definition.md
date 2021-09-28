# Definición funcional

## Idea inicial

La aplicacion consistirá en un agregador de noticias de distintos sitios web. La aplicación contará con soporte para usuarios registrados, sitios soportados y preferencias de usuarios. Se dispondrá, por tanto, de una base de datos en la que almacenar toda esta información (más adelante se detallará qué datos se guardarán exactamente). Para modelar los feeds de cada usuario se usarán etiquetas: Se dispondrá de un inventario de etiquetas en base de datos que permitirá clasificar los feeds RSS por temática (cada sitio podrá tener una o varias etiquetas). Cada usuario seleccionará un conjunto de etiquetas y se le asignarán los sitios que coincidan con las mismas. Una vez esta relación quede afianzada, el usuario podrá actualizar su feed regularmente para ir recibiendo noticias.

Las actualizaciones de los feeds RSS se almacenarán en una base de datos, en la que se tendrá en cuenta la fecha y hora de la última actualización. Esto permitirá que se puedan recoger registros de la base de datos si otro usuario ha actualizado un feed RSS que comparte con otro, ahorrando llamadas a los sitios web y ahorrando recursos.

## Actores

Entidades que interactúan con el sistema desde fuera.

* <span style="text-decoration: underline">Usuario básico</span>: Usuario de la aplicación. Representado por un registro en base de datos, de él se conocen:
    * Nombre.
    * Apellidos.
    * Correo electrónico.
    * Contraseña (encriptada).
    * [Perfil].
* [<span style="text-decoration: underline">Administradores</span>]: Usuarios especiales que tienen la posibilidad de consumir recursos administrativos que no están al alcance de usuarios básicos. De ellos se almacenará:
    * Nombre.
    * Apellidos.
    * Correo electrónico.
    * Contraseña (encriptada).
    * [Perfil].

## Sistema

El sistema está compuesto por los siguientes elementos lógicos:

* <span style="text-decoration: underline">Sitios RSS</span>: Direcciones en internet que sirven contenido usando el formato de transmisión RSS (Really Simple Syndication). De cada sitio se almacenará:
    * URL.
    * Nombre largo.
* <span style="text-decoration: underline">Etiquetas</span>: Cada etiqueta representa una categoría informativa (mundo, economía, tecnología, etc...). De las etiquetas se necesitará conocer:
    * Nombre largo.
    * Descripción.
* <span style="text-decoration: underline">Etiquetas de sitios RSS</span>: Relación de etiquetas para cada sitio RSS dado de alta. Sólo se deberá conocer la relación entre etiquetas y sitios RSS.
* <span style="text-decoration: underline">Suscripciones de usuarios a sitios RSS</span>: Relación de sitios RSS a los que se suscribe un usuario dado. De esta relación se deberá almacenar:
    * Correspondencia entre usuarios y sitios RSS.
    * Fecha de suscripción.
    * Orden de suscripción para el usuario.
* <span style="text-decoration: underline">Sesiones</span>: Cada vez que un usuario inicia sesión, se anotará para hacer seguimiento. De cada registro se tendrán en cuenta las siguientes características:
    * Usuario.
    * ID de sesión (generado automáticamente).
    * Fecha de creación.
    * Fecha de caducidad.
    * Estado de la sesión (abierta, cerrada).
* [<span style="text-decoration: underline">Perfiles</span>]: Perfiles disponibles. De cada perfil se deberá almacenar:
    * Nombre largo.
    * Código único.
* [<span style="text-decoration: underline">Acciones</span>]: Listado de formas de interacción entre los actores y el sistema. De cada acción se deberá almacenar:
    * Nombre largo.
    * Código único.
* [<span style="text-decoration: underline">Privilegios</span>]: Relación entre perfiles y acciones que indica qué usuarios de un perfil pueden realizar una acción determinada. De esta relación se tendrá en cuenta:
    * Correspondencia entre acciones y perfiles.
* [<span style="text-decoration: underline">Eventos</span>]: Este módulo registrará todos los eventos de interés que ocurran en el sistema. Se estudiará si puede hacerse de forma no bloqueante y con poco uso de recursos. Cada evento estará compuesto por:
    * Acción (si hubiera).
    * Usuario (si hubiera).
    * Fecha y hora.
    * Datos (como JSON).

> NOTA: Los elementos entre corchetes se añadirán en futuras revisiones de la aplicación.

## Software elegido

1. Intérprete: CPython (clásico).
2. ORM: SQLAlchemy.
3. Base de datos: MySQL.
4. Servidor web de aplicación: Tornado.
5. Servidor web externo: Nginx.
6. Control de procesos: Supervisor.

## Formato de respuesta

El cuerpo de todas las respuestas seguirán una misma estructura:

```
{
    "data": SERVICE_JSON_DATA <TODO>,
    ["error": ERROR_JSON_DATA] <TODO>
}
```

Estos datos estarán incluidos en una respuesta HTTP estándar. La aplicación usará los siguientes códigos HTTP para comunicar el resultado de las llamadas recibidas:

| Código HTTP |   Descripción             |        Condiciones                 |
|:---------------:|:------------------:|:------------------------------------:|
| 200              | Servicio ejecutado con éxito            | El servicio se ejecuta sin problemas, sin lanzar excepciones
|               |             | 
|               |             | 
|               |             | 
|               |             | 
|               |             | 
|               |             | 

Ver: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

# Referencias

* https://www.geeksforgeeks.org/designing-use-cases-for-a-project/
* https://www.guru99.com/functional-requirement-specification-example.html
* https://www.sitepoint.com/organize-project-files/
