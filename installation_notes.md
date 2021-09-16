# Installation notes

## NewsAggregator backend

1. Lista vacía en pyodbc al listar drivers disponibles.

Si al ejecutar pyodbc.drivers() se obtiene una lista vacía, hay que instalar los drivers ODBC necesarios, según los SGBD a emplear en la aplicación. Como en mi caso estoy usando MySQL, con acceder a esta página y seguir las instrucciones ha bastado: https://dev.mysql.com/doc/connector-odbc/en/connector-odbc-installation-binary-deb.html

Linux Mint es compatible con Ubuntu 18.04, por lo que seleccionando ese sistema operativo y versión, he podido descargar e instalar los paquetes necesarios. Sólo una nota al respecto: Al instalar el paquete mysql-connector-odbc_8.0.26-1ubuntu18.04_amd64.deb ha surgido una dependencia no satisfecha que impide su instalación. Bastará con descargar e instalar el siguiente paquete: https://repo.mysql.com/apt/ubuntu/pool/mysql-8.0/m/mysql-community/mysql-community-client-plugins_8.0.26-1ubuntu18.04_amd64.deb

## NewsAggregator frontend

1. Creción de un proyecto Django desde cero.

