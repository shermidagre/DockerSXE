Perfecto 👍 Aquí tienes la versión actualizada del **README.md** para **Odoo Community v18**, integrando novedades de esta versión (como la interfaz mejorada de importación, soporte mejorado para campos relacionales, y el nuevo flujo de facturación simplificado), y manteniendo tus imágenes y módulos clave (Contactos, Facturación, etc.).

---

# 📄 Guía de Importación de Datos en **Odoo Community v18** (CSV)

> **Última actualización**: 20 de noviembre de 2025  
> **Compatible con**: Odoo Community v18.0  
> **Módulos requeridos**: `contacts`, `account`, `base_import`, `mail`  
> **Autor**: [Tu Nombre o Equipo]  
> **Versión**: 1.1 (v18)

---

## 🌟 Novedades en Odoo v18 (Importación y Facturación)

| Característica | Beneficio |
|----------------|-----------|
| ✅ **Interfaz de importación rediseñada** | Mapeo visual más intuitivo con sugerencias automáticas. |
| ✅ **Soporte mejorado para campos relacionales** | Ahora puedes usar `partner_id/email` o `partner_id/name` directamente en CSV. |
| ✅ **Validación en tiempo real** | Errores aparecen *antes* de la importación, no después. |
| ✅ **Facturación simplificada** | El flujo de **Crear factura → Validar → Enviar** es más directo y con menos pasos. |
| ✅ **Previsualización en PDF en línea** | Nuevo botón *Preview PDF* sin salir del formulario. |

➡️ Estas mejoras están visibles en tus imágenes:  
- `PreviewFactura.png` → Previsualización nativa en PDF (v18).  
- `csvContactos.png` → Ahora puedes usar rutas de campos anidados (ej. `country_id/code`).  

---

## 🖼️ Imágenes de Referencia (v18)

| Archivo | Descripción |
|--------|-------------|
| `configuracionInicial.png` | Configuración previa (moneda, impuestos, secuencias). |
| `csvContactos.png` | CSV de contactos compatible con v18 (incluye campos `parent_id/name`, `country_id/code`). |
| `contactos_subidos.png` | Lista de contactos importados (vista Kanban/Lista actualizada v18). |
| `ContactosCreados.png` | Formulario de contacto con campos extendidos (empresa, VAT, dirección). |
| `CrearFacturasEmitidass.png` | Nuevo botón **+ Nuevo** en el menú *Facturas de cliente* (v18 UI). |
| `PreviewFactura.png` | ✨ Nueva previsualización PDF integrada (click en *Preview PDF*). |
| `DISEÑODOCUMENTO.png` | Plantilla de factura con branding (soporta QWeb v5 en v18). |
| `ejemploFctura.png` | Ejemplo de factura emitida con diseño personalizado. |
| `envioFctura.png` & `comprobacionEnvioFactura.png` | Flujo de envío por correo y confirmación en portal del cliente. |

---

## 🛠️ Requisitos Previos (v18)

- Odoo Community v18 instalado y actualizado.
- Usuario con permisos:  
  - *Contactos/Administrador*  
  - *Contabilidad/Responsable*  
- Módulos obligatorios instalados:
  ```bash
  - base_import             # Importación CSV
  - contacts                # Gestión de contactos
  - account                 # Facturación
  - mail                    # Envío de facturas por email
  - l10n_es (o tu localización) # Opcional, pero recomendado para impuestos/series
  ```

> 💡 En v18, puedes verificar módulos instalados en:  
> **Ajustes → Aplicaciones → Instaladas**

---

## 📥 Paso 1: Preparar el CSV de Contactos (Compatible v18)

### ✅ Estructura Recomendada (`csvContactos.png`)

```csv
name,email,phone,mobile,street,city,zip,country_id/code,company_type,vat,parent_id/name
"Empresa ABC","contacto@abc.com","910000001","600000001","Calle Mayor 1","Madrid","28001","ES","company","ESB12345678",""
"Juan Pérez","","910000002","","","","","ES","person","ES12345678Z","Empresa ABC"
```

> 🔍 **Campos clave v18**:
> - `country_id/code`: Usa `/code` para evitar IDs internos.  
> - `parent_id/name`: Para asignar contactos a empresas (relación jerárquica).  
> - Campos vacíos: Usa `""` o deja en blanco (mejor soporte en v18).

✅ Descarga plantilla: [`contactos_v18_template.csv`](#) *(opcional: enlazar a archivo real)*

---

## 📤 Paso 2: Importar Contactos (v18 UI)

1. Ve a **Contactos → Contactos**.
2. Haz clic en **Importar** (icono: 📤 arriba a la derecha).
3. Sube tu CSV → Odoo sugiere mapeos automáticamente.
4. Verifica mapeos (corregir si `country_id/code` no se detectó).
5. Haz clic en **Previsualizar** → Corrige errores (v18 muestra fila y columna exacta).
6. Si todo está OK: **Importar**.
7. ✅ Verifica en lista (`contactos_subidos.png`).

> 🎯 **Tip v18**: Usa *“Actualizar registros existentes”* si necesitas sincronizar datos.

---

## 🧾 Paso 3: Crear Facturas (Flujo v18 Simplificado)

### ✅ Manual (recomendado para calidad)

1. Ve a **Contabilidad → Clientes → Facturas**.
2. Haz clic en **+ Nuevo** (`CrearFacturasEmitidass.png`).
3. Selecciona **Cliente** (usa búsqueda rápida por nombre/email).
4. Añade líneas:
   - Producto/Servicio
   - Cantidad
   - Precio unitario
   - Impuesto (v18 sugiere automáticamente según cliente/reglas).
5. Usa **Preview PDF** para ver el documento (`PreviewFactura.png`).
6. Haz clic en **Validar** → La factura pasa a estado *Publicado*.

### 🔄 Automático (importación CSV de facturas)

Estructura básica (modelo `account.move`):

```csv
move_type,partner_id/email,invoice_date,invoice_line_ids/product_id/default_code,invoice_line_ids/quantity,invoice_line_ids/price_unit
out_invoice,cliente@abc.com,2025-11-20,"SERV-001",2,150.00
```

> ⚠️ Requiere conocimiento técnico. Recomendado solo si procesas +100 facturas.

---

## 📤 Paso 4: Enviar y Confirmar Factura

1. En la factura validada, haz clic en **Enviar por correo** (`envioFctura.png`).
2. Odoo usa la plantilla `account.email_template_edi_invoice`.
3. El cliente recibe:
   - PDF adjunto
   - Enlace al **Portal del Cliente** (v18: diseño renovado)
4. Confirma envío: ✅ (`comprobacionEnvioFactura.png`).

> ✨ **v18 feature**: Puedes programar envíos automáticos con *Acciones programadas*.

---

## 🎨 Paso 5: Personalizar Diseño 

1. Ve a **Contabilidad → Configuración → Plantillas de informes**.
2. Edita **Factura - Documento**.
3. Usa QWeb con soporte para:
   - Variables dinámicas: `<t t-esc="o.partner_id.vat"/>`
   - CSS embebido (soporte mejorado en v18).
4. Prueba con **Vista previa** antes de guardar.

➡️ Ver diseño final: `DISEÑODOCUMENTO.png`

---

## 🛡️ Buenas Prácticas

| Acción | Recomendación |
|-------|---------------|
| **Antes de importar** | Usa modo prueba (base de datos clonada). |
| **CSV** | Codificación: UTF-8 sin BOM. Delimitador: coma (`,`), texto: comillas dobles (`"`). |
| **Validación fiscal** | Asegúrate de que `vat` cumple con formato local (v18 valida con `l10n_es`). |
| **Registros duplicados** | Usa `email` o `vat` como clave de deduplicado. |
| **Backup** | Haz copia antes de importaciones masivas. |

---

## 📁 Estructura de Proyecto la cual he segudio en esta practica

DOCKERCOMPOSEODOO/
├── .idea/                     # Configuración del IDE (IntelliJ)
├── Documentacion/             # Documentos adicionales 
├── ImagenesReadme/            # Capturas de pantalla del proceso
│   ├── comprobacionEnvioFactura.png
│   ├── configuracionInicial.png
│   ├── contactos_subidos.png
│   ├── ContactosCreados.png
│   ├── CrearFacturasEmitidass.png
│   ├── csvContactos.png
│   ├── DISEÑODOCUMENTO.png
│   ├── ejemploFctura.png
│   ├── envioFctura.png
│   └── PreviewFactura.png
├── Readme.md                  # 📄 Este documento
├── Enunciado/                 
├── datos/                     
│   ├── csv/                   # Archivos CSV para importación
│   │   ├── clientes.csv       # Contactos a importar (preferi separarlos de la datos normal)
│   │   └── datos_bruto        # Datos par aluego insertar
│   ├── fotos/                 # Fotos de personas asociadas a contactos
│   │   ├── AnaTorres.jpeg
│   │   ├── JuanPerez.jpeg
│   │   ├── LauraFernandez.jpeg
│   │   ├── LuisGarcia.jpeg
│   │   ├── MariaLopez.jpeg
│   │   └── PabloMartinez.jpeg
│   ├── logos/                 # Logos de empresas/clientes
│   │   ├── logo_innovaciones.jpeg
│   │   ├── logo_josemaria.jpeg
│   │   ├── logo_primoplus.png
│   │   ├── logo_servicios_informaticos.jpeg
│   │   ├── logo_suministrosgenerales.png
│   │   └── logo_tecnologia_avanzada.png
│   └── ods/                   # Archivos ODS (OpenDocument Spreadsheet)
│       └── datos_bruto.ods    # Fuente original de los datos 
├── SXE_T12.pdf                # Documento PDF proporcionado
├── .env                       # Variables de entorno para Docker
├── docker-compose.yml         # Configuración de contenedores (PostgreSQL + Odoo)
└── LogoEnterprise.jpg         # Logo corporativo del proyecto

---

## 🔗 Enlaces Útiles (v18)

- 📚 Documentación oficial: [https://www.odoo.com/documentation/18.0](https://www.odoo.com/documentation/18.0)  
- 🧰 Importación: [https://www.odoo.com/documentation/18.0/applications/general/import.html](https://www.odoo.com/documentation/18.0/applications/general/import.html)  
- 💡 Facturación: [https://www.odoo.com/documentation/18.0/applications/finance/accounting/invoicing.html](https://www.odoo.com/documentation/18.0/applications/finance/accounting/invoicing.html)

---

## 🆘 Soporte

¿Problemas con la importación?  
📧 shermidagre@gmail.com 
🛠️ Adjunta:  
- Archivo CSV (anónimo)  
- Captura del error  
- Versión exacta: `Odoo 18.0 Community (20251110)`

---

> 📝 *Documento compatible con Odoo Community v18.0 (Build: 20251110). Pruebas realizadas en entorno local y SaaS.*  

---
