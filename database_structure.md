# Definición de base de datos

Definición de estructura de tablas de base de datos.

> **users**

Usuarios registrados en el sistema.

| Nombre de campo |   Tipo        |        Restricciones           |
|:---------------:|:-------------:|:------------------------------:|
| id              | NUMERIC       | AUTO INCREMENT, PRIMARY KEY    |
| name            | STRING (50)   | UTF-8                          |
| surname         | STRING (50)   | UTF-8                          |
| email           | STRING (50)   | UTF-8, NOT NULL, UNIQUE, INDEX |
| password        | STRING (100)  | UTF-8                          |
| is_active       | BOOLEAN       |                                |

> **rss_feeds**

Sitios que exponen feeds RSS.

| Nombre de campo |   Tipo        |        Restricciones        |
|:---------------:|:-------------:|:---------------------------:|
| id              | NUMERIC       | AUTO INCREMENT, PRIMARY KEY |
| url             | STRING (50)   | UTF-8, UNIQUE               |
| title           | STRING (100)  | UTF-8                       |


> **tags**

Etiquetas que permiten clasificar los sitios RSS e identificar intereses de usuarios.

| Nombre de campo |   Tipo        |        Restricciones        |
|:---------------:|:-------------:|:---------------------------:|
| id              | NUMERIC       | AUTO INCREMENT, PRIMARY KEY |
| title           | STRING (50)   | UTF-8, NOT NULL             |
| description     | STRING (200)  | UTF-8                       |

> **rss_feeds_tags**

Correspondencia entre sitios RSS y etiquetas. Cada sitio RSS puede tener varias etiquetas distintas, dando una idea a los usuarios sobre el tipo de contenido que publica.

| Nombre de campo |   Tipo        |        Restricciones                |
|:---------------:|:-------------:|:-----------------------------------:|
| rss_feed_id     | NUMERIC       | PRIMARY KEY, FOREIGN KEY (rss_feed) |
| tag_id          | NUMERIC       | PRIMARY KEY, FOREIGN KEY (tags)     |

> **subscriptions**

Suscripciones de usuarios a sitios RSS.

| Nombre de campo |   Tipo        |        Restricciones                |
|:---------------:|:-------------:|:-----------------------------------:|
| user_id         | NUMERIC       | PRIMARY KEY, FOREIGN KEY (users)    |
| rss_feed_id     | NUMERIC       | PRIMARY KEY, FOREIGN KEY (rss_feed) |

> **sessions**

Registros de todas las sesiones creadas en el sistema por logins de usuarios.

| Nombre de campo |   Tipo             |        Restricciones                 |
|:---------------:|:------------------:|:------------------------------------:|
| id              | NUMERIC            | AUTO INCREMENT, PRIMARY KEY          |
| user_id         | NUMERIC            | FOREIGN KEY (users), NOT NULL, INDEX |
| session_id      | STRING (100)       | UTF-8, NOT NULL, UNIQUE, INDEX       |
| creation_date   | DATETIME (UTC + 2) | NOT NULL, DEFAULT NOW (UTC + 2)      |
| expiration_date | DATETIME (UTC + 2) | NOT NULL                             |
| closing_date    | DATETIME (UTC + 2) |                                      |
| is_alive        | BOOLEAN            |                                      |