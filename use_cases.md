<span style="background-color:blue;font-size:20px;">Se dejará de usar este enfoque de casos de uso por restricciones de tiempo</span>

# Casos de uso

Un caso de uso es una herramienta de diseño de software que refleja los diferentes flujos y resultados de ejecución de los recursos del sistema. Esto permitirá que el equipo de desarrollo y el equipo de producto o comercial se entiendan entre sí, al describir el sistema en un lenguaje que ambas partes entienden.

La idea es describir todos los comportamientos de cada recurso a alto nivel para, más adelante y con otras herramientas, ahondar en detalles y crear unos esquemas más cercanos a la implementación técnica (excepciones, tipos de datos devueltos, notificaciones emitidas, lógicas de reintentos, etc...).

Para el caso que nos ocupa, me quedaré sólo en esta fase (casos de uso), pues este proyecto no tiene como objetivo principal el trabajar estas técnicas de diseño de software, si no usarlas para desarrollar un sistema completo.

Ver: https://www.utm.mx/~caff/doc/OpenUPWeb/openup/guidances/guidelines/detail_ucs_and_scenarios_6BC56BB7.html

Listado de todas las interacciones posibles entre el sistema y los actores, desglosadas en pasos. Este listado se usará para implementar los servicios necesarios en el sistema.

## Registro de usuario

Un usuario se registra en el sistema.

* Actor principal: Usuario.
* Precondiciones:
    * El correo electrónico del usuario no existe en el sistema.
* Disparadores:
    * El usuario desea darse de alta en la aplicación. Para ello, consume el recurso de registro de usuarios.
* Escenarios OK:
    1. Registro OK. 
        * Pasos:
            * El usuario indica los datos requeridos con un formato y tipo adecuados y llama al recurso de registro de usuario.
            * El sistema recibe la llamada y hace las siguientes comprobaciones:
                1. Se comprueba que los datos son correctos en tipo y formato.
                2. Se comprueba que el correo electrónico no esté siendo utilizado por otro usuario.
            * Los datos son correctos y el correo electrónico no existe en base de datos, se procede a crear un nuevo usuario con los datos indicados. 
                1. Se utilizan los datos proporcionados por el usuario para crear su registro en base de datos.
                2. Se crea una contraseña inicial aleatoriamente, se encripta y se guarda en base de datos.
                3. Se envía un correo electrónico al usuario con su clave inicial. <span style="background-color:yellow"> PENDIENTE, POR AHORA NO SE IMPLEMENTA </span>
                4. Se devuelve una respuesta exitosa desde el recurso.
        * Postcondiciones:
            * Se crea un registro de usuario en la base de datos.

* Escenarios KO:
    1. Argumentos de tipo y/o formato incorrecto. 
        * Pasos:
            * El usuario llama al recurso de registro de usuario con uno o más datos erróneos.
            * El sistema recibe la llamada y hace las siguientes comprobaciones:
                1. Se comprueba que los datos son correctos en tipo y formato. La comprobación se hará en un orden determinado, elegido por el programador.
            * El sistema detecta que un parámetro tiene un tipo o formato incorrecto y emite una excepción dando información detallada y clara al usuario, abortando el proceso.
        * Postcondiciones:
            * No se crea registro del usuario ni se guarda información alguna en base de datos.
    2. El correo electrónico ya existe en base de datos. 
        * Pasos:
            * El usuario indica los datos requeridos con un formato y tipo adecuados y llama al recurso de registro de usuario.
            * El sistema recibe la llamada y hace las siguientes comprobaciones:
                1. Se comprueba que los datos son correctos en tipo y formato. La comprobación se hará en un orden determinado, elegido por el programador.
                2. Se comprueba que el correo electrónico no esté siendo utilizado por otro usuario.
            * El sistema detecta que el correo electrónico indicado ya existe en base de datos y emite una excepción dando información detallada y clara al usuario, abortando el proceso.
        * Postcondiciones:
            * No se crea registro del usuario ni se guarda información alguna en base de datos.
    3. Error no controlado en el sistema.
        * Pasos:
            * El usuario indica los datos requeridos con un formato y tipo adecuados y llama al recurso de registro de usuario.
            * El sistema recibe la llamada y hace las siguientes comprobaciones:
                1. Se comprueba que los datos son correctos en tipo y formato. La comprobación se hará en un orden determinado, elegido por el programador.
                2. Se comprueba que el correo electrónico no esté siendo utilizado por otro usuario.
            * El sistema experimenta un error no controlado en algún momento durante la ejecución del recurso y emite una excepción dando información detallada y clara al usuario, abortando el proceso. Se deberán cerrar conectores abiertos y liberar recursos.
        * Postcondiciones:
            * Dependiendo de dónde haya ocurrido el error se decidirá si aplicar ROLLBACK a la base de datos si es necesario. Por lo general, si no se ha modificado la base de datos, no se almacenará nada en ella.

        <br>

        > OJO: Si ocurriera un error al crear el usuario y la contraseña por ejemplo no se terminara de crear y almacenar, podría afectar a otros recursos y servicios. Tratar este tipo de situaciones y asegurar que esto no pueda ocurrir por diseño.

## Identificación de usuario

Un usuario se identifica en la aplicación.

* Actor principal: Usuario.
* Precondiciones:
    * El usuario está registrado en el sistema.
    * El usuario está activo.
* Disparadores:
    * El usuario desea identificarse para poder acceder a la aplicación. Para ello, consume el recurso de identificación de usuarios.
* Escenarios OK:
    1. Identificación OK. 
        * Pasos:
            * El usuario indica los datos requeridos con un formato y tipo adecuados y llama al recurso de identificación de usuario.
            * El sistema recibe la llamada y hace las siguientes comprobaciones:
                1. Se comprueba que los datos son correctos en tipo y formato. La comprobación se hará en un orden determinado, elegido por el programador.
                2. Se comprueba que el usuario exista y esté activo.
                3. Se comprueba si la contraseña proporcionada coincide con la almacenada en base de datos.

                    <span style="background-color:red"> CONTINUAR </span>

        * Postcondiciones:
            - <span style="background-color:red"> CONTINUAR </span>

* Escenarios KO:
    1. <span style="background-color:red"> CONTINUAR </span>

## Listar datos de usuario

Un usuario pide un listado completo de sus datos.

* Actor principal: Usuario.
* Precondiciones:
    * El usuario está registrado en el sistema.
    * El usuario está activo.
* Disparadores:
    * El usuario desea obtener un listado de sus datos personales, incluyendo datos de usuario, suscripciones e intereses. Para ello, consume el recurso de listado de datos de usuario.
* Escenarios OK:
    1. Listado OK. 
        * Pasos:
            * El usuario indica los datos requeridos con un formato y tipo adecuados y llama al recurso de listado de datos de usuario.
            * Se supone que el usuario existe y está activo, pues previamente ha tenido que obtener un token de acceso y para ello se han hecho todas estas comprobaciones.
            * Una vez pasadas todas las comprobaciones con éxito, el sistema sigue el siguiente flujo de ejecución: 
                1. Se recuperan los registros necesarios de base de datos para componer la respuesta del servicio.
                2. Se seleccionan los datos requeridos de cada registro y se compone la respuesta final.
                3. Se devuelve una respuesta exitosa desde el recurso.
        * Postcondiciones:
            * Ninguna.
* Escenarios KO:
    1. Argumentos de tipo y/o formato incorrecto. 
        * Pasos:
            * El usuario llama al recurso de listado de datos de usuario con uno o más datos erróneos.
            * El sistema recibe la llamada y hace las siguientes comprobaciones:
                1. Se comprueba que los datos son correctos en tipo y formato.
            * El sistema detecta que un parámetro tiene un tipo o formato incorrecto y emite una excepción dando información detallada y clara al usuario, abortando el proceso.
        * Postcondiciones:
            * Ninguna.
    2. Error no controlado en el sistema.
        * Pasos:
            * El usuario indica los datos requeridos con un formato y tipo adecuados y llama al recurso de listado de datos de usuario.
            * El sistema recibe la llamada y hace las siguientes comprobaciones:
                1. Se comprueba que los datos son correctos en tipo y formato. 
                2. Se comprueba que el correo electrónico pertenece al usuario que consume el recurso.
            * El sistema experimenta un error no controlado en algún momento durante la ejecución del recurso y emite una excepción dando información detallada y clara al usuario, abortando el proceso. Se deberá cerrar conectores abiertos y liberar recursos.
        * Postcondiciones:
            * Ninguna.

