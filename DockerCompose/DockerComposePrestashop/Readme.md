# 🐳 Subir un contenedor Docker con PrestaShop, MariaDB y phpMyAdmin

Este repositorio contiene los archivos necesarios para levantar un entorno completo de **PrestaShop** utilizando **Docker Compose**, incluyendo una base de datos (**MySQL/MariaDB**) y una interfaz de administración (**phpMyAdmin**).

---

## 📄 Archivo `docker-compose.yml`

### ¿Para qué sirve este archivo?

El archivo `docker-compose.yml` actúa como lanzador de los contenedores de Docker. En él se definen y configuran los servicios necesarios para ejecutar PrestaShop junto con su base de datos y herramientas de gestión.

En este ejemplo, se proporcionan dos enfoques:

1. **Versión básica**: Levanta PrestaShop sin instalación automática (requiere configuración manual vía navegador).
2. **Versión con instalación automática**: Configura PrestaShop automáticamente al levantar los contenedores, utilizando variables de entorno predefinidas.

---

## 📁 Estructura final del `docker-compose.yml`

A continuación, se muestra la versión completa y funcional del archivo `docker-compose.yml`, con soporte para:
- Variables de entorno desde un archivo `.env`
- Volúmenes para persistencia de datos
- Healthcheck para garantizar que la base de datos esté lista antes de iniciar otros servicios

```yaml
services:
  db:
    image: mysql:8.0
    container_name: prestashop_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  prestashop:
    image: prestashop/prestashop:latest
    container_name: prestashop_app
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8080:80"
    environment:
      DB_SERVER: db
      DB_NAME: ${MYSQL_DATABASE}
      DB_USER: ${MYSQL_USER}
      DB_PASSWD: ${MYSQL_PASSWORD}
      PS_INSTALL_AUTO: 1
      PS_DEV_MODE: 1
      PS_DOMAIN: localhost:8080
      PS_LANGUAGE: es
      PS_COUNTRY: ES
    volumes:
      - prestashop_data:/var/www/html
    restart: always

  phpmyadmin:
    image: phpmyadmin:latest
    container_name: prestashop_phpmyadmin
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    restart: always

volumes:
  db_data:
  prestashop_data:
```

> 💡 **Nota**: Se recomienda usar una versión específica de MySQL (como `mysql:8.0`) para evitar incompatibilidades con PrestaShop.

---

## 🔐 Gestión segura de credenciales con `.env`

Para evitar exponer credenciales directamente en el archivo `docker-compose.yml`, se utiliza un archivo `.env` en la misma carpeta.

### Archivo `.env`

Crea un archivo llamado `.env` con el siguiente contenido:

```env
MYSQL_ROOT_PASSWORD=rootpass
MYSQL_DATABASE=prestashop
MYSQL_USER=prestashop
MYSQL_PASSWORD=prestashoppas
```

Docker Compose cargará automáticamente estas variables al ejecutar `docker-compose up`.

> ⚠️ **Importante**: Asegúrate de **no incluir el archivo `.env` en tu repositorio público** si contiene credenciales sensibles. Agrega `.env` a tu `.gitignore`.

---

## 🎥 Tutoriales en video

### 1. Levantar el contenedor **sin instalación automática** de PrestaShop

[![Miniatura del video](https://img.youtube.com/vi/eRgJtPX-vcU/0.jpg)](https://youtu.be/eRgJtPX-vcU)

> 💡 Haz clic en la imagen para abrir el tutorial en YouTube.

---

### 2. Levantar el contenedor **con instalación automática** de PrestaShop

[![Miniatura del video](https://img.youtube.com/vi/V3Wif_E1dJs/0.jpg)](https://youtu.be/V3Wif_E1dJs)

> 💡 Haz clic en la imagen para abrir el tutorial en YouTube.

---

## 📌 ¿Por qué usar volúmenes?

Los volúmenes de Docker garantizan la **persistencia de datos**:

- **`db_data`**: Almacena los datos de la base de datos en `/var/lib/mysql`.  
  → Si eliminas y recreas el contenedor, **no perderás tu tienda ni productos**.
- **`prestashop_data`**: Guarda los archivos de PrestaShop en `/var/www/html`.  
  → Permite personalizar temas, módulos o configuraciones sin perderlos al reiniciar.

---

## 🩺 ¿Por qué usar `healthcheck`?

El `healthcheck` en el servicio de base de datos:

- Verifica que MySQL esté completamente operativo antes de que PrestaShop intente conectarse.
- Evita errores comunes como *"Can't connect to MySQL server"* durante el arranque.
- Usa `depends_on` con `condition: service_healthy` para sincronizar el inicio de los servicios.

---

## ▶️ Cómo usar este entorno

1. Clona este repositorio.
2. Crea el archivo `.env` con tus credenciales.
3. Ejecuta:

```bash
docker-compose up -d
```

4. Accede a:
   - **PrestaShop**: [http://localhost:8080](http://localhost:8080)
   - **phpMyAdmin**: [http://localhost:8081](http://localhost:8081)

> ✅ La primera vez, si `PS_INSTALL_AUTO=1`, PrestaShop se instalará automáticamente.

---

## 🛑 Notas importantes

- En producción, **nunca uses `PS_DEV_MODE=1`** ni contraseñas débiles.
- Considera usar **MariaDB** en lugar de MySQL si lo prefieres (solo cambia la imagen a `mariadb:10.6`).
- Para desarrollo local, asegúrate de que los puertos `8080` y `8081` no estén ocupados.

---

#### Archivo final yml

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

    healthcheck:
      test: [ "CMD", "mysqladmin", "ping", "-h", "localhost" ]
      interval: 10s
      timeout: 5s
      retries: 5


  prestashop:
    image: prestashop/prestashop:latest
    container_name: prestashop_app
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