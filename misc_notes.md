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

## * como argumento en una función o método

Si este símbolo aparece como argumento en una función o método, implica que a partir de él, el resto de argumentos serán no posicionales. Esto permite dar "pistas" sobre qué se espera en argumentos posicionales sin tratarlos como opcionales:

```python

def function(first_operand: int, second_operand=None: int, *, third_operand=None: int):
    
    result = first_operand
    if second_operand:
        result += second_operand
    
    if third_operand:
        result += third_operand
    
    return result

>>> print(function(1, 2, 3))
Traceback (most recent call last):
....
TypeError: function() takes from 1 to 2 positional arguments but 3 were given
>>> print(function(1, 2))
3
>>> print(function(1, 2, third_operand=3))
6

```

## Django ORM, shell y Querysets

Django dispone de su propio ORM, permite crear tablas de mapeo y traducirlas a tablas de base de datos. Estas clases son parte del modelo y normalmente se encuentran en archivos `models.py` en las applicaciones que componen el proyecto. Por ejemplo:

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

Cada modelo está basado en la clase `django.db.models.Model`, ver documentación para más información.

Con cada cambio a estos modelos requerirá aplicarlos. Django también gestiona el versionado y aplica los parches cuando es necesario. Para ello, hay que ejecutar un par de comandos:

```plain
# Crea archivos de "parcheo" de base de datos.
python manage.py makemigrations

# Los aplica en base de datos.
python manage.py migrate
```

Django dispone de una shell especial que se puede invocar desde `manage.py`. Básicamente es un intérprete Python en el que `manage.py` carga la variable de entorno `DJANGO_SETTINGS_MODULE`, por lo que tiene acceso directo a las aplicaciones del proyecto.

```
python manage.py shell
```

Una vez dentro, se puede trabajar con los modelos y los registros guardados en base de datos con facilidad:

```python

# Modelo especial para trabajar con los usuarios disponibles en Django (por ejemplo, creados con python manage.py createsuperuser).
from django.contrib.auth.models import User

# Módulo que contiene timezone.now(), devuelve la hora actual en UTC con timezone.
from django.utils import timezone

# Importar los modelos.
from polls.models import Choice, Question

# Obtener todos los registros en base de datos del modelo Question.
Question.objects.all()

# Crear un nuevo registro.
question = Question(question_text="What's new?", pub_date=timezone.now())

# Hay que guardar el registro para que se grabe en base de datos.
question.save()

# El registro ya tiene ID asociado (pues ha sido almacenado en base de datos).
question.id

# El resto de campos también es accesible.
question.question_text
question.pub_date

# Es posible modificarlo directamente.
question.question_text = "How's your day?"
question.save()

# Crear otro registro.
question2 = Question(question_text="How many hours did you sleep today?", pub_date=timezone.now())
question2.save()

# Ahora sí hay registros almacenados.
all_questions = Question.objects.all()

# Se puede iterar sobre ellos para modificarlos y grabarlos directamente.
for question in all_questions:
    question.question_text = "Have you ever tried fried japanese rice?"
    question.save()

# O modificarlas todas a la vez.
all_questions.update(question_text="Have you ever tried fried japanese rice?")
for question in all_questions:
    question.save() 

# Se pueden obtener registros de base de datos fácilmente.
me = User.objects.get(username='david')

# Un registro de este tipo se puede usar en modelos que cuenten con una columna que referencie a AUTH_USER_MODEL, como:
# author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# Se pueden ordenar registros.
Questions.objects.order_by('pub_date')

# También inversamente.
Questions.objects.order_by('-pub_date')

# Aquellos métodos que devuelvan otro QuerySet permitirán encadenar peticiones y generar consultas más complejas.
Question.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')
```

## Clases base abstractas

En Python, estas clases actúan como lo serían las clases abstractas en Java: No se pueden instanciar, pero cualquiera que herede de ellas deberá implementar los métodos abstractos que declara:

```python
from abc import ABCMeta, abstractmethod

class AbstactClassCSV(metaclass = ABCMeta):
 
    def __init__(self, path, file_name):
        self._path = path
        self._file_name = file_name

    # Método abstracto, getter para el atributo privado _path.
    @property
    @abstractmethod
    def path(self):
        pass

    @path.setter
    @abstractmethod
    def path(self,value):
        pass
 
    @property
    @abstractmethod
    def file_name(self):
        pass

    @file_name.setter
    @abstractmethod
    def file_name(self,value):
        pass

    @abstractmethod
    def display_summary(self):
        pass
```

Los métodos abstractos, identificados por `@abstractmethod` no se implementan en esta clase, pero sí deberán implementarse en las clases que hereden de ésta.

## Bound y unbound forms en Django

Se dice que un formulario es "bound" cuando se inicializa con datos, mientras que su estado será "unbound" cuando no dispone de datos.

Esta distinción es clave, pues Django no hará validaciones en formularios "unbound" (como es lógico).

Un ejemplo de esta distinción lo tenemos al tratar peticiones POST y GET en una misma vista:

```python

if request.method == "POST":
    form = PostForm(request.POST)

    # Checks whether the form's fields have errors or the form is bound. The form will be bound as it has data associated, i.e., when is instantiated with data. This occurs in the previos sentence, when the form is instantiated with the request.POST data.
    if form.is_valid():

        # Get the model's instance (record) but don't save yet, as the author needs to be added.
        post = form.save(commit=False)
        post.author = request.user
        post.publish()
        post.save()
else:
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

```

## Referencia a URLs del panel de administración Django.

Si se requiere hacer referencia mediante el tag {% url ... %} en algún template, Django dispone de patrones específicos para el panel de administración: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#reversing-admin-urls

También en esta categoría caen URLs como la de login: https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-login-required-decorator, a la que Django redirige si un usuario no está identificado e intenta acceder a una URL cuya view está protegida por el decorador `login_required`. 

## Cómo Django trata las contraseñas (básico)

Django incorpora varias formas de computar y tratar las contraseñas (https://docs.djangoproject.com/en/3.2/topics/auth/passwords/). Según señalan en su documentación, el sistema de identificado de usuarios no debería reinventarse frecuentemente, pues bastará con usar una implementación que se compruebe es segura y robusta.

En el caso de Django, se usan contraseñas almacenadas como hashes. Estas cadenas se componen de la siguiente manera:

`<algorithm>$<iterations>$<salt>$<hash>`

Donde:
* `<algorithm>`: Algoritmo seleccionado para calcular el hash. Es uno de los que soporta Django y que se pueden encontrar en `settings.PASSWORD_HASHERS`, en el archivo `global_settings.py` (no se encuentra en el proyecto). Por defecto el algoritmo empleado es PBKDF2, que cuenta con hashes SHA256.
* `<iterations>`: Número de iteraciones del algoritmo (cuantas más mejor, aunque más coste computacional se asocia a la computación de cada contraseña).
* `<salt>`: Cadena aleatoria, para evitar ataques Rainbow table (https://en.wikipedia.org/wiki/Rainbow_table).
* `<hash>`: Resultado de la función de hashing.

Django ofrece la posibilidad de cambiar el algoritmo y modificar algunos parámetros, aunque no es recomendable si no es completamente necesario.

## Arreglo para error NO_PUBKEY en Linux Mint

El error en cuestión se obtiene al usar ciertos mirrors para su uso con `apt-get`:

> W: GPG error: https://mirror.dogado.de/linuxmint tara Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY A6616109451BBBF2

La solución pasa por obtener la clave pública y almacenarla, con el siguiente comando:

```
sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com A6616109451BBBF2
```

Como argumento (o argumentos si son varios mirrors los que fallan), hay que indicar la clave o claves públicas que `apt-get update` no puede obtener.