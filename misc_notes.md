# Notas 

En este archivo se irán recopilando notas sobre temas interesantes que vayan surgiendo durante la codificación del proyecto.

## Fechas, almacenamiento y tratamiento de distintas timezones. 

Lo mejor es almacenar las fechas en formato UTC. Si es necesario hacer distinciones entre distintos usuarios (que se encuentren en zonas horarias distintas) se recomienda usar datetime en el backend y almacenar las timezones en formato IANA (estándar) en base de datos, en una columna independiente. De esta forma el backend podrá trabajar con las fechas y formatearlas con la timezone del cliente cuando sea necesario (normalmente para imprimirlo para humanos), pero siempre las guardará en UTC en base de datos.

La columna independiente debería estar donde se haga la distinción por timezone. Por ejemplo, la zona horaria de Madrid quedaría identificada por la cadena "Europe/Madrid" si se sigue IANA.

En Python se pueden usar los módulos datetime y pytz para trabajar con este tipo de objetos:

```python
import datetime
import pytz

# The datetime objects should be stored in UTC in the database, along with the timezone (in a different column).
# Whenever needed, the date and the timezone should be fetched from the database to construct the datetime object
# as needed.

# The following lines create a UTC localized time (with timezone) that holds the present time in UTC.
utc_timezone = pytz.timezone('UTC')
now = utc_timezone.localize(datetime.datetime.utcnow())

print(f"UTC time: {now}")

# This is the timezone string that should be stored in the database
# (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
# If the present time needs to be formatted with a timezone:
madrid_timezone = pytz.timezone('Europe/Madrid')
madrid_local_time = now.astimezone(madrid_timezone)

print(f"Madrid local time: {madrid_local_time}")

# These lines already consider DST, which can be checked by calling the "dst()" method. This method outputs the
# number of ours (positive or negative) with respect to UTC applied to the date object as DST.
print(f"Madrid local time DST: {madrid_local_time.dst()}")
```

> Ver: 
<br>https://stackoverflow.com/questions/44965545/best-practices-with-saving-datetime-timezone-info-in-database-when-data-is-dep
<br>https://en.wikipedia.org/wiki/List_of_tz_database_time_zones


## Imports relativos

Cuando se utiliza la instrucción `import`, Python busca primero en `sys.modules` (módulos que han sido cargados previamente). Si no lo encuentra ahí, buscará en un listado de paquetes built-in. En caso de no encontrarlo aquí tampoco, buscará en la lista de directorios declarada en `sys.path`. Este listado incluye el directorio actual, en el que buscará en primer lugar.

Una vez Python encuentra el módulo, lo asocia a un nombre en el ámbito (scope) actual, ya sea archivo, clase, método, función...

Para módulos a importar propios, dentro de la estructura de archivos del proyecto, normalmente se usan imports absolutos, que comienzan a listar módulos desde el raíz del proyecto. Suponiendo que tenemos la siguiente estructura de archivos:

app
    - admin.py
    - models
        - post.py
    - manage.py

Si tuviéramos que importar la clase `Post` -incluida en el archivo `post.py`- en `admin.py` con un import absoluto, quedaría así: 

```python
from app.models.post import Post
```

Por otro lado, con imports relativos se toma como referencia el directorio actual, usando `.`. Si se requiere buscar en un directorio superior, se usaría `..`. Con esto, el import relativo quedaría así:

```python
from .models.post import Post
```

No se recomienda el uso de imports relativos.

