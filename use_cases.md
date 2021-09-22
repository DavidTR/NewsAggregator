# Casos de uso

<span style="background-color:yellow;font-size:50px;">TODO</span>

Listado detallado de todas las interacciones posibles entre el sistema y los actores, desglosadas en pasos. Este listado se usará para implementar los servicios necesarios en el sistema.

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
                1. Se comprueba que los datos son correctos en tipo y formato. La comprobación se hará en un orden determinado, elegido por el programador.
                2. Se comprueba que el correo electrónico no esté siendo utilizado por otro usuario.
            * Los datos son correctos y el correo electrónico no existe en base de datos, se procede a crear un nuevo usuario con los datos indicados. 
                1. Se utilizan los datos proporcionados por el usuario para crear su registro en base de datos.
                2. Se crea una contraseña inicial aleatoriamente, se encripta y se guarda en base de datos.
                3. Se envía un correo electrónico al usuario con su clave inicial.
                4. Se devuelve una respuesta exitosa desde el recurso.
        * Postcondiciones:
            * Se crea un registro de usuario en la base de datos.
            * Se genera una contraseña aleatoria y se almacena en el registro de base de datos recién creado.
            * Se envía un correo electrónico al usuario informándole del alta exitosa y proporcionándole su contraseña.

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

        > OJO: Si ocurriera un error al crear el usuario y la contraseña por ejemplo no se terminara de crear y almacenar, podría afectar a otros recursos y servicios. Tratar este tipo de cosas en consecuencia y asegurar que esto no pueda ocurrir por diseño.

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
            * Los datos son correctos y el correo electrónico no existe en base de datos, se procede a crear un nuevo usuario con los datos indicados. 
                1. Se utilizan los datos proporcionados por el usuario para crear su registro en base de datos.
                2. Se crea una contraseña inicial aleatoriamente, se encripta y se guarda en base de datos.
                3. Se envía un correo electrónico al usuario con su clave inicial.
                4. Se devuelve una respuesta exitosa desde el recurso.
        * Postcondiciones:
            * Se crea un registro de usuario en la base de datos.
            * Se genera una contraseña aleatoria y se almacena en el registro de base de datos recién creado.
            * Se envía un correo electrónico al usuario informándole del alta exitosa y proporcionándole su contraseña.

* Escenarios KO:
    1. Argumentos de tipo y/o formato incorrecto. 
        * Pasos:
            * El usuario llama al recurso de identificación de usuario con uno o más datos erróneos.
            * El sistema recibe la llamada y hace las siguientes comprobaciones:
                1. Se comprueba que los datos son correctos en tipo y formato. La comprobación se hará en un orden determinado, elegido por el programador.
            * El sistema detecta que un parámetro tiene un tipo o formato incorrecto y emite una excepción dando información detallada y clara al usuario, abortando el proceso.
        * Postcondiciones:
            * No se crea registro del usuario ni se guarda información alguna en base de datos.