# Subir un contenedor Docker con PrestaShop, MariaDB y phpMyAdmin

Este repositorio contiene los archivos necesarios para levantar un entorno completo de PrestaShop utilizando Docker Compose, incluyendo una base de datos mysql y una interfaz de administración phpMyAdmin.

---

## 📄 Archivo `docker-compose.yml`

### ¿Para qué sirve este archivo?

El archivo `docker-compose.yml` actúa como lanzador de los contenedores de Docker. En él se definen y configuran los servicios necesarios para ejecutar PrestaShop junto con su base de datos y herramientas de gestión.

En este ejemplo, se proporcionan dos enfoques:

1. **Versión básica**: Levanta PrestaShop sin instalación automática (requiere configuración manual vía navegador).
2. **Versión con instalación automática**: Configura PrestaShop automáticamente al levantar los contenedores, utilizando variables de entorno predefinidas.

---

## 📁 Estructura del `docker-compose.yml` (sin volumenes)

A continuación, se muestra un ejemplo funcional del archivo `docker-compose.yml`:

```yaml

services:
  db:
    image: mysql
    container_name: prestashop_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}

    volumes:
      - db_data:/var/lib/mysql

  prestashop:
    image: prestashop/prestashop:latest
    container_name: prestashop_app
    depends_on:
      - db
    ports:
      - "8080:80"
    environment:
      DB_SERVER: db
      DB_NAME: ${MYSQL_DATABASE}
      DB_USER: ${MYSQL_USER}
      DB_PASSWD: ${MYSQL_PASSWORD}

          ## Aqui se establece la instalacion automatica del propio perstashop

      PS_INSTALL_AUTO: 1
      PS_DEV_MODE: 1
      PS_DOMAIN:  localhost:8080
    volumes:
      - prestashop_data:/var/www/html
    restart: always

  phpmyadmin:
    image: phpmyadmin:latest
    container_name: prestashop_phpmyadmin
    depends_on:
      - db
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: rootpass
    restart: always

volumes:
  db_data:
  prestashop_data:

```

1. Levantar el contenedor sin instalar automaticamente prestashop

[![Miniatura del video](https://img.youtube.com/vi/OJctgGheJWM/0.jpg)](https://youtu.be/OJctgGheJWM)

> 💡 Haz clic en la imagen para abrir el tutorial en YouTube.

---


2. Levantar el contenedor instalando automaticamente prestashop

[![Miniatura del video](https://img.youtube.com/vi/OJctgGheJWM/0.jpg)](https://youtu.be/OJctgGheJWM)

> 💡 Haz clic en la imagen para abrir el tutorial en YouTube.

---



### Ya que asi los valores estan muy dispersos se creara un archivo .dev en la misma carpeta que tienes este yml para asi que las credenciales no esten expuestas a la vista de cualquier


```dev

MYSQL_ROOT_PASSWORD=rootpass
MYSQL_DATABASE=prestashop
MYSQL_USER=prestashop
MYSQL_PASSWORD=prestashoppas


```
### Al pasar las credenciales a un documento externo podemos asi llamarlas ya en el propio programa , y quedaria tal que asi 

```yml

services:
  db:
    image: mysql
    container_name: prestashop_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}

  prestashop:
    image: prestashop/prestashop:latest
    container_name: prestashop_app
    depends_on:
      - db
    ports:
      - "8080:80"
    environment:
      DB_SERVER: db
      DB_NAME: ${MYSQL_DATABASE}
      DB_USER: ${MYSQL_USER}
      DB_PASSWD: ${MYSQL_PASSWORD}
      PS_INSTALL_AUTO: 1
      PS_DEV_MODE: 1
      PS_DOMAIN:  localhost:8080

    restart: always

  phpmyadmin:
    image: phpmyadmin:latest
    container_name: prestashop_phpmyadmin
    depends_on:
      - db
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: rootpass
    restart: always

volumes:
  db_data:
  prestashop_data:

```

### Ya que tenemos lo principal configurado vamos a añadirle los volumenes a nuestro yml.

#### Para que se añaden estos volumenes?¿

- Persistencia de Datos: Utilizar volúmenes de Docker (volumes) para que
los datos de la base de datos (/var/lib/mysql) y los ficheros de
PrestaShop (/var/www/html) persistan aunque los contenedores se eliminen
y se vuelvan a crear.


```yml
 
 services:
  db:
    image: mysql
    container_name: prestashop_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
 # -->
    volumes:
      - db_data:/var/lib/mysql

  prestashop:
    image: prestashop/prestashop:latest
    container_name: prestashop_app
    depends_on:
      - db
    ports:
      - "8080:80"
    environment:
      DB_SERVER: db
      DB_NAME: ${MYSQL_DATABASE}
      DB_USER: ${MYSQL_USER}
      DB_PASSWD: ${MYSQL_PASSWORD}
      PS_INSTALL_AUTO: 1
      PS_DEV_MODE: 1
      PS_DOMAIN:  localhost:8080
 # -->
 volumes:
      - prestashop_data:/var/www/html
    restart: always

  phpmyadmin:
    image: phpmyadmin:latest
    container_name: prestashop_phpmyadmin
    depends_on:
      - db
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: rootpass
    restart: always

### Indicamos donde los hemos añadido 

volumes:
  db_data:
  prestashop_data:

```

### casi no nos queda nada por configurar, por ultimo vamos a configuarar el healthcheck

#### Para que nos sirve el healthcheck¿?

Añadir una directiva healthcheck al servicio de la base de datos (db). Esta
comprobación debe verificar activamente que el servicio de base de datos
está operativo.


```yml

services:
  db:
    image: mysql
    container_name: prestashop_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}

    volumes:
      - db_data:/var/lib/mysql

# -->
    healthcheck:
      test: [ "CMD", "mysqladmin", "ping", "-h", "localhost" ]
      interval: 10s
      timeout: 5s
      retries: 5


  prestashop:
    image: prestashop/prestashop:latest
    container_name: prestashop_app

    # -->

    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_SERVER: db
      DB_NAME: ${MYSQL_DATABASE}
      DB_USER: ${MYSQL_USER}
      DB_PASSWD: ${MYSQL_PASSWORD}
      PS_INSTALL_AUTO: 1
      PS_DEV_MODE: 1
      PS_DOMAIN:  localhost:8080
      PS_LANGUAGE: es
      PS_COUNTRY: ES
    
    ports:
      - "8080:80"
      
    volumes:
        - prestashop_data:/var/www/html

    restart: always

  phpmyadmin:
      image: phpmyadmin:latest
      container_name: prestashop_phpmyadmin

      # -->
      depends_on:
        db:
          condition: service_healthy
      ports:
        - "8081:80"
      environment:
        PMA_HOST: db
        PMA_USER: root
        PMA_PASSWORD: rootpass

      restart: always

volumes:
  db_data:
  prestashop_data:


```
