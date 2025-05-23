
# SisFact: Sistema de Gestión de Facturas

Este programa es una aplicación de escritorio desarrollada con [Flet](https://flet.dev/) en Python, diseñada para gestionar empresas, facturas y facturas de manera sencilla y visual.

## ¿Qué puedes hacer?

- **Registrar empresas** con sus datos principales (nombre, NIT, correo, teléfono).
- **Crear facturas** (pagadas y no pagadas) para cada empresa.
- **Agregar ítems** y detalles a cada factura.
- **Adjuntar evidencia de soporte** a cada factura.
- **Visualizar y filtrar** facturas por fecha o número de factura.
- **Mover facturas** entre pagadas y no pagadas.
- **Eliminar facturas** seleccionadas.
- **Ver información detallada** de cada empresa.

## Requisitos

- Python 3.8 o superior
- **Flet versión 0.23.0**

Para instalar Flet, ejecuta:

```
pip install flet>=0.23.0
```

## ¿Cómo ejecutar la aplicación?

1. Descarga o clona este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta:

```
flet run main.py
```

## Notas

- Los datos se almacenan en carpetas y archivos CSV dentro de la carpeta `SisFact`.
- Cada empresa tiene su propia carpeta con sus facturas y registro.
- El nombre de la empresa se muestra centrado en la pantalla de facturas.

---
