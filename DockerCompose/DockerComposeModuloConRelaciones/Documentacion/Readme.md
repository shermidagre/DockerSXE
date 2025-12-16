
---

# 📄 Guía de Importación de un nuevo módulo en Odoo

> **✅ Compatible con**: Odoo Community v18.0  
> **🧑‍💻 Autor**: Samuel Hermida Gregores

---

## 🗂️ Paso 1: Estructura inicial del proyecto

Primero crearemos nuestra estructura del proyecto **sin datos**, para a posteriori establecer lo necesario.

![img.png](ImagenesReadme/34242.png)

// tengo que cambiar la imagen
---

### 🛠️ Creación del *scaffold* del módulo

```dotenv
docker ps
docker exec -it <Id de tu contenedor Odoo> bash
odoo scaffold modulo_medico_paciente /mnt/extra-addons/
```

---

#### 💡 Ejemplo de uso

![img8.png](ImagenesReadme/img8.png)

---

### 🐳 Configuración de `docker-compose.yaml`

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

### 📦 Archivo `odoo.conf`

```ini
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = admin
```

## 🗂️ Paso 2: Desarrollo del módulo

### 📦 Archivo `__manifest__.py`

#### Definición del módulo y sus dependencias (*linkear correctamente las views*).

```python
# -*- coding: utf-8 -*-
{
    'name': "modulo_medico_paciente",
    'summary': "Gestión de pacientes, médicos y diagnósticos",
    'description': """
        Módulo que permite gestionar:
        - Pacientes (nombre, apellidos, síntomas)
        - Médicos (nombre, apellidos, nº colegiado, consulta)
        - Relación muchos a muchos mediante diagnósticos
    """,
    'author': "Samuel Hermida Gregores",
    'website': "https://github.com/shermidagre",
    'category': 'Healthcare',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/paciente_views.xml',
        'views/medico_views.xml',
        'views/diagnostico_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
}
```

---

### 📦 Modelo `models/paciente.py`

#### Modulo para gestionar los pacientes y su relación con los médicos a través de diagnósticos.

#### *Campos obligatorios*

- ID Paciente
- Nombre
- Apellidos

#### *Relacion 1 : N con Diagnosticos*
#### *Relacion N : M con Medicos (mediante diagnosticos)*
#### Por cada paciente, se mostrará una lista de los médicos que lo han atendido (nombre y consulta) gracias al mapped.

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

### 📦 Modelo `models/medico.py`

#### Modulo para gestionar los médicos y su relación con los pacientes a través de diagnósticos.

#### *Campos obligatorios*

- ID Médico
- Nombre
- Apellidos
- Nº Colegiado
- Consulta

#### *Relacion 1 : N con Diagnosticos*
#### *Relacion N : M con Pacientes (mediante diagnosticos)*
#### Por cada médico, se mostrará una lista de los pacientes que ha atendido (nombre y síntomas) gracias al mapped.

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
    diagnostico_ids = fields.One2many('hospital.diagnostico', 'medico_id', string="Diagnósticos")
    paciente_ids = fields.Many2many('hospital.paciente', compute='_compute_pacientes', string="Pacientes atendidos")

    def _compute_pacientes(self):
        for medico in self:
            medico.paciente_ids = medico.diagnostico_ids.mapped('paciente_id')
```

---

### 📦 Modelo `models/diagnostico.py`

#### Modulo intermedio para la relación muchos a muchos entre el medico y el paciente, para asi poder controlar los diagnosticos de los cuales se encargan los medicos a los pacientes.

##### *Campos obligatorios*

- Médico (Many2one a hospital.medico)
- Paciente (Many2one a hospital.paciente)
- Síntomas (campo calculado, relacionado con el paciente)
- Consulta (campo calculado, relacionado con el médico)

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

### 📦 Archivo de permisos: `security/ir.model.access.csv`

#### Al tener que añadir mas de un modelo, el archivo completo quedaría así:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_hospital_paciente_user,access_hospital_paciente_user,model_hospital_paciente,base.group_user,1,1,1,1
access_hospital_medico_user,access_hospital_medico_user,model_hospital_medico,base.group_user,1,1,1,1
access_hospital_diagnostico_user,access_hospital_diagnostico_user,model_hospital_diagnostico,base.group_user,1,1,1,1
```

---

## 📦 Vistas XML

### Vista de el paciente
#### `views/paciente_views.xml`

```xml
<odoo>
    <record id="view_hospital_paciente_form" model="ir.ui.view">
        <field name="name">hospital.paciente.form</field>
        <field name="model">hospital.paciente</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="id_paciente"/>
                        <field name="nombre"/>
                        <field name="apellidos"/>
                        <field name="sintomas" widget="text"/>
                    </group>
                    <notebook>
                        <page string="Médicos que lo han atendido">
                            <field name="medico_ids" readonly="1">
                                <tree>
                                    <field name="nombre"/>
                                    <field name="apellidos"/>
                                    <field name="consulta"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_hospital_paciente_tree" model="ir.ui.view">
        <field name="name">hospital.paciente.tree</field>
        <field name="model">hospital.paciente</field>
        <field name="arch" type="xml">
            <tree>
                <field name="id_paciente"/>
                <field name="nombre"/>
                <field name="apellidos"/>
            </tree>
        </field>
    </record>

    <record id="action_hospital_paciente" model="ir.actions.act_window">
        <field name="name">Pacientes</field>
        <field name="res_model">hospital.paciente</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

---

### Vista de el medico

#### `views/medico_views.xml`

```xml
<odoo>
    <record id="view_hospital_medico_form" model="ir.ui.view">
        <field name="name">hospital.medico.form</field>
        <field name="model">hospital.medico</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="id_medico"/>
                        <field name="nombre"/>
                        <field name="apellidos"/>
                        <field name="num_colegiado"/>
                        <field name="consulta"/>
                    </group>
                    <notebook>
                        <page string="Pacientes atendidos">
                            <field name="paciente_ids" readonly="1">
                                <tree>
                                    <field name="nombre"/>
                                    <field name="apellidos"/>
                                    <field name="sintomas"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_hospital_medico_tree" model="ir.ui.view">
        <field name="name">hospital.medico.tree</field>
        <field name="model">hospital.medico</field>
        <field name="arch" type="xml">
            <tree>
                <field name="id_medico"/>
                <field name="nombre"/>
                <field name="apellidos"/>
                <field name="num_colegiado"/>
                <field name="consulta"/>
            </tree>
        </field>
    </record>

    <record id="action_hospital_medico" model="ir.actions.act_window">
        <field name="name">Médicos</field>
        <field name="res_model">hospital.medico</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

---

#### `views/diagnostico_views.xml`

```xml
<odoo>
    <record id="view_hospital_diagnostico_form" model="ir.ui.view">
        <field name="name">hospital.diagnostico.form</field>
        <field name="model">hospital.diagnostico</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="medico_id"/>
                        <field name="paciente_id"/>
                        <field name="sintoma" readonly="1"/>
                        <field name="consulta" readonly="1"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_hospital_diagnostico_tree" model="ir.ui.view">
        <field name="name">hospital.diagnostico.tree</field>
        <field name="model">hospital.diagnostico</field>
        <field name="arch" type="xml">
            <tree>
                <field name="medico_id"/>
                <field name="paciente_id"/>
                <field name="consulta"/>
            </tree>
        </field>
    </record>

    <record id="action_hospital_diagnostico" model="ir.actions.act_window">
        <field name="name">Diagnósticos</field>
        <field name="res_model">hospital.diagnostico</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

---

#### `views/menu_views.xml`

```xml
<odoo>
    <menuitem id="menu_hospital_root" name="Hospital" sequence="10"/>

    <menuitem id="menu_hospital_pacientes" name="Pacientes" parent="menu_hospital_root" action="action_hospital_paciente"/>
    <menuitem id="menu_hospital_medicos" name="Médicos" parent="menu_hospital_root" action="action_hospital_medico"/>
    <menuitem id="menu_hospital_diagnosticos" name="Diagnósticos" parent="menu_hospital_root" action="action_hospital_diagnostico"/>
</odoo>
```

---

## 🧪 Pruebas: Levantar y probar el módulo

*(Sección reutilizada tal cual de tu plantilla original)*

### Paso 1: Crear base de datos  
![img_1.png](ImagenesReadme/img_1.png)

### Paso 2: PgAdmin  
- Iniciar sesión  
- Conectar con Odoo  
![img_4.png](ImagenesReadme/img_4.png)  
![img_5.png](ImagenesReadme/img_5.png)

### Paso 3: Buscar y activar el módulo  
- Iniciar sesión en Odoo  
- Instalar **modulo_medico_paciente**

[![Miniatura del video](https://img.youtube.com/vi/p2IjtaCv_sE/0.jpg)](https://youtu.be/p2IjtaCv_sE)

> 💡 Haz clic en la imagen para abrir el tutorial en YouTube.

### 🎉 ¡Módulo instalado!

Accede al menú **Hospital** para gestionar pacientes, médicos y diagnósticos.

---

### 📝 Manual de uso

#### 1. Registrar un paciente
- Ve a **Hospital → Pacientes → Crear**
- Rellena todos los campos
- Guarda

#### 2. Registrar un médico
- Ve a **Hospital → Médicos → Crear**
- Completa datos obligatorios
- Guarda

#### 3. Crear un diagnóstico
- Ve a **Hospital → Diagnósticos → Crear**
- Selecciona médico y paciente
- Al guardar, se vinculan automáticamente

> ✨ El paciente verá al médico en su ficha. El médico verá al paciente en su historial.

---

## 👁️ Guía Visual de Vistas

- **Paciente**: muestra lista de médicos que lo atendieron (nombre + consulta)
- **Médico**: muestra lista de pacientes (nombre + síntomas)
- **Diagnóstico**: formulario simple con selección y campos calculados

---

## 🛠️ Estructura del Proyecto

```
modulo_medico_paciente/
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── paciente.py
│   ├── medico.py
│   └── diagnostico.py
├── views/
│   ├── paciente_views.xml
│   ├── medico_views.xml
│   ├── diagnostico_views.xml
│   └── menu_views.xml
├── security/
│   └── ir.model.access.csv
└── README.md
```

---

## 🔗 Enlaces Útiles (v18)

- 📚 **Docker Odoo**: [https://hub.docker.com/_/odoo](https://hub.docker.com/_/odoo)
- 📚 **Documentación Odoo**: [https://www.odoo.com/documentation/18.0](https://www.odoo.com/documentation/18.0)

---

## 🆘 Soporte

¿Problemas con la importación?  
📧 **Contacto**: shermidagre@gmail.com

🛠️ **Adjunta**:
- Captura del error
- Comandos ejecutados

---

> ✨ ¡Y listo! Tu módulo hospitalario está listo para usarse en Odoo Community v18.0.

---
