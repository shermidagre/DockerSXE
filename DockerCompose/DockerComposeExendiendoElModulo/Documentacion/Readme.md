
---

# 📄 Guía de Importación de un nuevo módulo en Odoo

> **✅ Compatible con**: Odoo Community v18.0  
> **🧑‍💻 Autor**: Samuel Hermida Gregores

---

## 🗂️ Paso 1: Estructura inicial del proyecto

Primero crearemos nuestra estructura del proyecto **sin datos**, para a posteriori establecer lo necesario.

![img.png](ImagenesReadme/img.png)

---

### 🛠️ Creación del *scaffold* del módulo

Se empezará creando el *scaffold* de nuestro proyecto mediante los siguientes comandos e instrucciones:

```dotenv
Se ejecutará el docker ps para identificar qué contenedores están activos actualmente y así poder entrar a la consola de nuestro contenedor Odoo.

Comando --> docker ps 

Proseguido, cogeremos la ID de nuestro contenedor de Odoo para así poder ejecutar el exec sobre el mismo y entrar en la terminal.

Comando --> docker exec -it <Id de tu contenedor> bash

Dentro ya de la bash, ejecutaremos el comando para así poder crear el scaffold. Este mismo lo que hace es crear las carpetas necesarias para la creación del módulo a posteriori.

Comando --> odoo scaffold <Nombre que le vayas a dar a tu proyecto> /mnt/extra-addons/
```

---

#### 💡 Ejemplo de uso

![img8.png](ImagenesReadme/img8.png)

---

### 🐳 Configuración de `docker-compose.yaml`

Teniendo ya este formato, crearemos nuestro archivo `docker-compose.yaml` para levantar nuestro servicio Odoo:

```yaml
services:
  web:
    image: odoo:18.0
    container_name: "odoo"
    depends_on:
      - mydb
    ports:
      - "8069:8069"
    environment:
      - HOST=mydb
      - USER=odoo
      - PASSWORD=myodoo
    volumes:
      - odoo:/var/lib/odoo
      - ./config:/etc/odoo
      - ./extra-addons:/mnt/extra-addons

  mydb:
    image: postgres:15
    container_name: "postgres"
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=myodoo
      - POSTGRES_USER=odoo
    volumes:
      - db_odoo:/var/lib/postgresql/data

  pgAdmin:
    image: dpage/pgadmin4
    container_name: "pgAdmin"
    depends_on:
      - mydb
    ports:
      - "8081:80"
    environment:
      - PGADMIN_DEFAULT_EMAIL=shermidagre@gmail.com
      - PGADMIN_DEFAULT_PASSWORD=sxe_password_example
    volumes:
      - dbadmin_data:/var/lib/pgadmin

volumes:
  db_odoo:
  odoo:
  dbadmin_data:
```

---

### 📦 Archivo `__manifest__.py` (Manifest)

Especificaremos las características del módulo que queremos crear en Odoo en el archivo **Manifest**.

> Aquí irán las especificaciones básicas, pero se pueden incluir más campos si es necesario.

```env
# -*- coding: utf-8 -*-
{
    'name': "second_proyect_sxe",

    'summary': "Modulo que permite ver el signo del horoscopo chino ",

    'description': """
        Este modulo extiende el modelo res_parter añadiendo los siguientes 3 campos a contactos:
         Fecha de nacimiento
         Edad (Calculada automaticamente)
         Signo del horoscopo chino (calculado automaticamente)
    """,

    'author': "Alumno esclavista",
    'website': "https://www.noleolosuficientecomoparaquejarme.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
```
### 📦 Archivo `models.py` (Models)

```env

# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class second_proyect_sxe(models.Model):

    _inherit = 'res.partner'

    f_nac = fields.Date("Fecha de nacimiento")

    edad = fields.Integer(string = "Edad", readonly = True, compute = "_calcular_edad_china", store = True)
    signo_chino = fields.Char(string = "Signo Chino", readonly = True, compute = "_calcular_chinada", store = True)

    codigo_socio = fields.Char(string="Código de Socio")

    nivel_fidelidad = fields.Selection(
        [
            ('estandar', 'Estándar'),
            ('premium', 'Premium'),
            ('gold', 'Gold')
        ],
        string="Nivel de Fidelidad",
        compute="_compute_nivel_fidelidad",
        store=True,
        default='estandar'
    )

    @api.depends('f_nac')
    def _calcular_edad_china(self):
        for record in self:
            today = datetime.date.today()
            if record.f_nac:
                age = today.year - record.f_nac.year
                record.edad = age
            else:
                record.edad = 0

    @api.depends('f_nac')
    def _calcular_chinada(self):
        for record in self:
            if record.f_nac:
                record.signo_chino = "Calculado"
            else:
                record.signo_chino = "Sin calcular"

    @api.depends('codigo_socio')
    def _compute_nivel_fidelidad(self):
        for record in self:
            if not record.codigo_socio:
                # Si el código está vacío
                record.nivel_fidelidad = 'estandar'
            elif record.codigo_socio.upper().startswith('G'):
                # Si el código empieza por "G"
                record.nivel_fidelidad = 'gold'
            else:
                # Si el código tiene valor y no empieza por "G"
                record.nivel_fidelidad = 'premium'

```


---

## 🧪 Pruebas: Levantar y probar el módulo

### Paso 1: Crear base de datos

![img_1.png](ImagenesReadme/img_1.png)

---

### Paso 2: PgAdmin

#### Iniciamos sesion

![img_4.png](ImagenesReadme/img_4.png)

#### Conectamos nuestro odoo

![img_5.png](ImagenesReadme/img_5.png)

---

![img.png](ImagenesReadme/453.png)


### Paso 3: Buscar y activar el módulo

#### 🔐 Iniciar sesión

![img_2.png](ImagenesReadme/img_2.png)

#### Activamos la app contactos para a posterior

![img_6.png](ImagenesReadme/img_6.png)

#### 🔍 Activar modo desarrollador y buscar el módulo

![img_3.png](ImagenesReadme/img_3.png)

#### 📥 Instalar el módulo y comprobar res_parter

[![Miniatura del video](https://img.youtube.com/vi/6txDqTKZQIY/0.jpg)](https://youtu.be/6txDqTKZQIY)

> 💡 Haz clic en la imagen para abrir el tutorial en YouTube.

---

### 🎉 ¡Módulo instalado!

> Tan pronto se realiza la instalación, automáticamente ya te entra tu aplicación.

---

### ➕ Crear una nueva anotación


---

### 📝 ¿Qué haremos después de instalar nuestro módulo?



> *A partir de aquí son cookeadas a parte*

---

## 🔗 Enlaces Útiles (v18)

- 📚 **Documentación oficial DockerHub**: [https://hub.docker.com/_/odoo](https://hub.docker.com/_/odoo)
- 📚 **Documentación oficial Odoo**: [https://www.odoo.com/documentation/18.0](https://www.odoo.com/documentation/18.0)

---

## 🆘 Soporte

¿Problemas con la importación?  
📧 **Contacto**: shermidagre@gmail.com

🛠️ **Adjunta**:
- Captura del error

---

> ✨ ¡Y listo! Tu módulo debería estar funcionando correctamente dentro de tu instancia de Odoo Community v18.0.

---