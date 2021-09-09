# Definición funcional

## Idea inicial

La aplicacion consistirá en un agregador de noticias de distintos sitios web. La aplicación contará con soporte para usuarios registrados, sitios soportados y preferencias de usuarios. Se dispondrá, por tanto, de una base de datos en la que almacenar toda esta información (más adelante se detallará qué datos se guardarán exactamente). Para modelar los feeds de cada usuario se usarán etiquetas: Se dispondrá de un inventario de etiquetas en base de datos que permitirá clasificar los feeds RSS por temática (cada sitio podrá tener una o varias etiquetas). Cada usuario seleccionará un conjunto de etiquetas y se le asignarán los sitios que coincidan con las mismas. Una vez esta relación quede afianzada, el usuario podrá actualizar su feed regularmente para ir recibiendo noticias.

Las actualizaciones de los feeds RSS se almacenarán en una base de datos, en la que se tendrá en cuenta la fecha y hora de la última actualización. Esto permitirá que se puedan recoger registros de la base de datos si otro usuario ha actualizado un feed RSS que comparte con otro, ahorrando llamadas a los sitios web y ahorrando recursos.

### Actores

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

### Sistema

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

### Casos de uso

<span style="background-color:yellow;font-size:50px;">TODO</span>

Listado detallado de todas las interacciones posibles entre el sistema y los actores, desglosadas en pasos.

* Registro de usuario
    * Actor principal: Usuario.
    * Precondiciones:
        * Los datos del usuario no existen en el sistema.
    * Disparadores:
        * El usuario desea darse de alta en la aplicación. Para ello, hace click sobre el botón de registro (o alternativamente, consume el recurso de registro de usuarios).
    * Escenarios OK:
        * El usuario indica los datos requeridos

### Definición de base de datos.

<span style="background-color:yellow;font-size:50px;">TODO</span>

## Iteraciones de software

A continuación se lista, por cada versión mayor, las funcionalidades, mejoras o ideas que incorporarán.

### Versión 0.1

* Aplicación básica funcional:
    * Alta.
    * Login. 
    * Generación y mantenimiento de sesiones. Mecanismo para evitar que dos sesiones tengan el mismo ID (hash).
    * Gestión de datos de usuario: 
        * Datos personales. 
        * Intereses.
    * Baja de cuenta de usuario (lógica).
    * Modificación de suscripciones RSS de usuarios.
        * Suscribirse a un nuevo sitio RSS.
        * Ordenar.
        * Eliminar suscripción.
    * Actualizar suscripciones RSS de un usuario (volver a pedir noticias vía internet).
* Sistema de logging a fichero con rotación diaria.
* Organización de archivos según DDD.
* API REST con nombres adecuados en recursos.
* Comprobación de datos de entrada.
* Aplicar principios SOLID y fail fast.
* Aplicar concurrencia en el servidor web y gestionar las llamadas externas con paralelismo.
* 

### Versión 1.0

Se proponen las siguientes mejoras:

* Anotar todos los eventos del sistema en una nueva tabla de base de datos ("eventos"). Deberá evaluarse si puede hacerse con muy poco impacto al sistema y a la base de datos, anotando la información mínima indispensable. Se recomienda incluir el código como decorador o metaclase. 
* Verificación de correo electrónico en alta de cuenta. Agregar soporte para reconocer usuarios activos o inactivos y usuarios con email verificado o no verificado. El proceso de alta se modificará para que fije al usuario como inactivo y con email no verificado (enviando un email para que active la cuenta a su vez), lo cual le impedirá hacer login hasta que lo verifique. Se deberá crear otra sección para reenviar el correo electrónico de activación desde el servicio de login. Estos correos deben tener un tiempo de expiración y su envío deberá anotarse en la base de datos, con fecha, usuario y resultado (tabla eventos).

### Sucesivas versiones (por planificar)

* Agregar una clasificación para cada feed RSS por popularidad (investigar si esta información existe). También se pueden usar otros criterios, como: 
    * Rapidez a la hora de publicar noticias.
    * Número medio de noticias publicadas por día.
    * Independencia ideológica/libertad del medio de comunicación.
* Soporte a APML, tanto para importar preferencias de usuario como para exportarlas.
* Sugerir al usuario qué feeds podrían interesarles, ordenados por los criterios listados en el punto 1 de esta lista. El usuario podrá ir eligiendo uno a uno. Esto debería ser una nueva sección de la aplicación, evitando ser invasiva.
* Soportar conectores a los sistemas gestores de bases de datos más populares: PostgreSQL, MySQL, Oracle, etc...
* Dockerizar aplicación y orquestarla con Kubernetes.
* Sistema de privilegios, perfiles y acciones.

# Referencias

* https://www.geeksforgeeks.org/designing-use-cases-for-a-project/
* https://www.guru99.com/functional-requirement-specification-example.html

