Valores de la db en el archivo .env

# Creacion de la nueva bd

![img.png](img.png)

### Importante seleccionar el modo demo

## Inicio despues de crear la bd

![img_1.png](img_1.png)

## Instalamos los modulos necesarios

![img_2.png](img_2.png)

## Configuramos la bd de pgadmin

![img_4.png](img_4.png)

![img_3.png](img_3.png)

### Revisamos si se ha creado correctamente la bd

![img_5.png](img_5.png)

#### Procedemos a realizar las consultas a la bd

Entramos en la query tool

![img_6.png](img_6.png)


```dotenv

CREATE TABLE EmpresasFCT (
    idEmpresa SERIAL PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    quiereAlumnos BOOLEAN,
    numAlumnos INTEGER,
    fechaContacto DATE
);

```

En el cuadro de abajo se puede ver la tabla creada correctamente

![img_8.png](img_8.png)

----

### Insertar datos en la tabla

```dotenv

INSERT INTO EmpresasFCT (nombre, quiereAlumnos, numAlumnos, fechaContacto) VALUES
('TecnoDev SL', TRUE, 3, '2025-10-20'),
('Marketing Global FCT', TRUE, 1, '2025-11-15'),
('Soluciones Logísticas FCT', FALSE, 0, '2024-05-01'),
('Innovación y Diseño FCT', TRUE, 2, '2025-11-23'),
('Servicios Administrativos EZ', FALSE, 1, '2025-01-10');
```

----

![img_7.png](img_7.png)

----


