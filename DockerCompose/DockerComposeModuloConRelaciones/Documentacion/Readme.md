
---

# 📄 Guía de Importación de un nuevo módulo en Odoo

> **✅ Compatible con**: Odoo Community v18.0  
> **🧑‍💻 Autor**: Samuel Hermida Gregores

---

## 🗂️ Paso 1: Estructura inicial del proyecto

Primero crearemos nuestra estructura del proyecto **sin datos**, para a posteriori establecer lo necesario.

![img.png](ImagenesReadme/34242.png)

---

### 🛠️ Creación del *scaffold* del módulo

Se empezará creando el *scaffold* de nuestro proyecto mediante los siguientes comandos e instrucciones:

```dotenv
Se ejecutará el docker ps para identificar qué contenedores están activos actualmente y así poder entrar a la consola de nuestro contenedor Odoo.

Comando --> docker ps 

Proseguido, cogeremos la ID de nuestro contenedor de Odoo para así poder ejecutar el exec sobre el mismo y entrar en la terminal.

Comando --> docker exec -it <Id de tu contenedor> bash

Dentro ya de la bash, ejecutaremos el comando para así poder crear el scaffold. Este mismo lo que hace es crear las carpetas necesarias para la creación del módulo a posteriori.

Comando --> odoo scaffold modulo_medico_paciente /mnt/extra-addons/
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
      - PGADMIN_DEFAULT_PASSWORD=admin
    volumes:
      - dbadmin_data:/var/lib/pgadmin

volumes:
  db_odoo:
  odoo:
  dbadmin_data:
```

---

### 📦 Archivo `__manifest__.py` (Manifest)

```python
# -*- coding: utf-8 -*-
{
    'name': "modulo_medico_paciente",

    'summary': "Gestión de pacientes, médicos y diagnósticos",

    'description': """
        Módulo que permite gestionar:
        - Pacientes (nombre, apellidos, síntomas)
        - Médicos (nombre, apellidos, nº colegiado, consulta asignada)
        - Relación muchos a muchos mediante diagnósticos (registro de atención)
    """,

    'author': "Samuel Hermida Gregores",
    'website': "https://github.com/shermidagre",

    'category': 'Healthcare',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/diagnostico_views.xml',
        'views/medico_views.xml',
        'views/paciente_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
}
```

---

### 📦 Modelo `paciente.py`

```python
from odoo import models, fields

class Paciente(models.Model):
    _name = 'hospital.paciente'
    _description = 'Paciente'

    id_paciente = fields.Char(string="ID Paciente", required=True)
    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    sintomas = fields.Text(string="Síntomas")
    diagnostico_ids = fields.One2many('hospital.diagnostico', 'paciente_id', string="Diagnósticos")
    medico_ids = fields.Many2many('hospital.medico', compute='_compute_medicos', string="Médicos que lo han atendido")

    def _compute_medicos(self):
        for paciente in self:
            paciente.medico_ids = paciente.diagnostico_ids.mapped('medico_id')
```

---

### 📦 Modelo `medico.py`

```python
from odoo import models, fields

class Medico(models.Model):
    _name = 'hospital.medico'
    _description = 'Médico'

    id_medico = fields.Char(string="ID Médico", required=True)
    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    num_colegiado = fields.Char(string="Nº Colegiado", required=True)
    consulta = fields.Char(string="Consulta", required=True)
    paciente_ids = fields.Many2many('hospital.paciente', compute='_compute_pacientes', string="Pacientes atendidos")
    diagnostico_ids = fields.One2many('hospital.diagnostico', 'medico_id', string="Diagnósticos")

    def _compute_pacientes(self):
        for medico in self:
            medico.paciente_ids = medico.diagnostico_ids.mapped('paciente_id')
```

---

### 📦 Modelo `diagnostico.py` (modelo de relación)

```python
from odoo import models, fields

class Diagnostico(models.Model):
    _name = 'hospital.diagnostico'
    _description = 'Diagnóstico'

    medico_id = fields.Many2one('hospital.medico', string="Médico", required=True)
    paciente_id = fields.Many2one('hospital.paciente', string="Paciente", required=True)
    sintoma = fields.Text(related='paciente_id.sintomas', string="Síntomas", readonly=True)
    consulta = fields.Char(related='medico_id.consulta', string="Consulta", readonly=True)
```

---

### 📦 Archivos de vistas (resumen)

- **`diagnostico_views.xml`**: Vista formulario/tree para registrar diagnósticos (medico + paciente).
- **`medico_views.xml`**: Incluye notebook con pestaña para ver diagnósticos/pacientes atendidos.
- **`paciente_views.xml`**: Muestra lista de médicos que lo han atendido y detalles del diagnóstico.
- **`menu_views.xml`**: Menú raíz "Hospital" con submenús para Pacientes, Médicos y Diagnósticos.

> *Los archivos XML completos no se incluyen aquí por brevedad, pero siguen la lógica estándar de Odoo con `tree`, `form` y `many2many`/`one2many`.*

---

## 🧪 Pruebas: Levantar y probar el módulo

> *Pasos necesarios a seguir si no tienes nada realizado aun*

### Paso 1: Crear base de datos  
![img_1.png](ImagenesReadme/img_1.png)

### Paso 2: PgAdmin  
- Iniciar sesión  
- Conectar con la base de datos Odoo  
![img_4.png](ImagenesReadme/img_4.png)  
![img_5.png](ImagenesReadme/img_5.png)

### Paso 3: Buscar y activar el módulo  
- Iniciar sesión en Odoo  
- Activar modo desarrollador  
- Instalar el módulo **modulo_medico_paciente**

[![Miniatura del video](https://img.youtube.com/vi/p2IjtaCv_sE/0.jpg)](https://youtu.be/p2IjtaCv_sE)

> 💡 Haz clic en la imagen para abrir el tutorial en YouTube.

### 🎉 ¡Módulo instalado!

Accede al menú **Hospital** para gestionar pacientes, médicos y diagnósticos.

---

### 📝 Manual de uso

#### 1. Registrar un paciente
1. Ve a **Hospital → Pacientes → Crear**.
2. Rellena **ID, nombre, apellidos y síntomas**.
3. Guarda. No necesita médicos asignados inicialmente.

#### 2. Registrar un médico
1. Ve a **Hospital → Médicos → Crear**.
2. Indica **ID, nombre, apellidos, nº colegiado y consulta**.
3. Guarda.

#### 3. Crear un diagnóstico (vincular paciente y médico)
1. Ve a **Hospital → Diagnósticos → Crear**.
2. Selecciona un **médico** y un **paciente**.
3. Al guardar, se registrará la atención.  
   → El paciente verá al médico en su ficha.  
   → El médico verá al paciente en su historial.

> **Nota**: Los campos *Síntomas* y *Consulta* en el diagnóstico se rellenan automáticamente desde los modelos relacionados.

---

## 👁️ Guía Visual de Vistas

### Vista del Paciente
- Muestra: nombre, síntomas, ID.
- Pestaña: **Médicos que lo han atendido** → lista de médicos (con nombre y consulta).

### Vista del Médico
- Muestra: nombre, nº colegiado, consulta.
- Pestaña: **Pacientes atendidos** → lista con nombre y síntomas.

### Vista de Diagnóstico
- Formulario con selección de médico y paciente.
- Campos calculados: síntomas del paciente y consulta del médico.

---

## 🛠️ Estructura del Proyecto

- `models/paciente.py`
- `models/medico.py`
- `models/diagnostico.py`
- `views/diagnostico_views.xml`
- `views/medico_views.xml`
- `views/paciente_views.xml`
- `views/menu_views.xml`
- `security/ir.model.access.csv`
- `__manifest__.py`

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
- Versión de Odoo y Docker usada

---

> ✨ ¡Y listo! Tu módulo de gestión hospitalaria debería estar funcionando correctamente dentro de tu instancia de Odoo Community v18.0.

---
