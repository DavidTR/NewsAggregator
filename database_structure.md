# Definición de base de datos

Database table structure definition.

> **users**

Signed up users in the application.

| Nombre de campo |   Tipo        |        Restricciones           |
|:---------------:|:-------------:|:------------------------------:|
| id              | NUMERIC       | AUTO INCREMENT, PRIMARY KEY    |
| name            | STRING (50)   | UTF-8                          |
| surname         | STRING (50)   | UTF-8                          |
| email           | STRING (50)   | UTF-8, NOT NULL, UNIQUE        |
| password        | STRING (100)  | UTF-8, NOT NULL                |
| is_active       | BOOLEAN       | NOT NULL, DEFAULT TRUE         |

> **rss_feeds**

Sites that expose their news using RSS.

| Nombre de campo |   Tipo        |        Restricciones        |
|:---------------:|:-------------:|:---------------------------:|
| id              | NUMERIC       | AUTO INCREMENT, PRIMARY KEY |
| url             | STRING (50)   | UTF-8, UNIQUE               |
| title           | STRING (100)  | UTF-8                       |


> **rss_feeds_news**

News obtained from the RSS sites stored in the *rss_feeds* table. Every row in this table will hold all the news received from a RSS feed in a given date. This information will be used as:
    1. Cache to avoid calls to news sites made by different users in a short period of time.
    2. Store a history of news for later use (maybe as a library of some kind).

| Nombre de campo |   Tipo        |        Restricciones              |
|:---------------:|:-------------:|:---------------------------------:|
| id              | NUMERIC       | AUTO INCREMENT, PRIMARY KEY       |
| rss_feed_id     | NUMERIC       | FOREIGN KEY (rss_feeds), NOT NULL |
| query_date      | DATETIME      |                                   |
| news_data       | JSON          |                                   |


> **tags**

Tags will be used to classify the RSS feeds and identify users interests.

| Nombre de campo |   Tipo        |        Restricciones        |
|:---------------:|:-------------:|:---------------------------:|
| id              | NUMERIC       | AUTO INCREMENT, PRIMARY KEY |
| title           | STRING (50)   | UTF-8, NOT NULL             |
| description     | STRING (200)  | UTF-8                       |

> **rss_feeds_tags**

Relationship between RSS sites and tags. Each RSS site may have more than one tag, giving information about the type of content they publish to potential subscribers.

| Nombre de campo |   Tipo        |        Restricciones                |
|:---------------:|:-------------:|:-----------------------------------:|
| rss_feed_id     | NUMERIC       | PRIMARY KEY, FOREIGN KEY (rss_feed) |
| tag_id          | NUMERIC       | PRIMARY KEY, FOREIGN KEY (tags)     |

> **subscriptions**

Users subscribed to RSS feeds.

| Nombre de campo |   Tipo        |        Restricciones                |
|:---------------:|:-------------:|:-----------------------------------:|
| user_id         | NUMERIC       | PRIMARY KEY, FOREIGN KEY (users)    |
| rss_feed_id     | NUMERIC       | PRIMARY KEY, FOREIGN KEY (rss_feed) |

> **sessions**

All the sessions that users create when they log-in are stored here. For the sake of simplicity (as this is a personal, academic project), the DATETIME fields will use the same time zone as the server that hosts the DBMS.

| Nombre de campo |   Tipo             |        Restricciones                 |
|:---------------:|:------------------:|:------------------------------------:|
| id              | NUMERIC            | AUTO INCREMENT, PRIMARY KEY          |
| user_id         | NUMERIC            | FOREIGN KEY (users), NOT NULL, INDEX |
| session_id      | STRING (100)       | UTF-8, NOT NULL, UNIQUE, INDEX       |
| creation_date   | DATETIME (SYSTEM)  | NOT NULL, DEFAULT NOW (SYSTEM)       |
| expiration_date | DATETIME (SYSTEM)  | NOT NULL                             |
| closing_date    | DATETIME (SYSTEM)  |                                      |
| is_alive        | BOOLEAN            |                                      |