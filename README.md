# Python - Repositorio de Aprendizaje

Este repositorio contiene scripts de Python para aprender los fundamentos del lenguaje.

## Archivos

- **hola_mundo.py**: Programa básico "Hola Mundo" en Python
- **leccion1.py**: Introducción a variables y tipos de datos básicos
- **run_all.py**: Script para ejecutar todos los archivos Python del repositorio
- **view_versions.py**: Script para ver el historial de salidas de versiones

## Cómo ejecutar el código

### Ejecutar todos los archivos a la vez

```bash
python3 run_all.py
```

Este comando ejecutará todos los archivos Python y guardará las salidas en el directorio `versions/` para futuras referencias.

### Ejecutar archivos individuales

```bash
python3 hola_mundo.py
python3 leccion1.py
```

## 📊 Sistema de Versiones

Este repositorio ahora incluye un sistema de seguimiento de versiones que guarda automáticamente las salidas de cada ejecución.

### Ver historial de versiones

Para ver todas las versiones guardadas:
```bash
python3 view_versions.py list
```

Para filtrar por archivo específico:
```bash
python3 view_versions.py list hola_mundo
```

### Ver la salida de una versión específica

Para ver la versión más reciente (versión 1):
```bash
python3 view_versions.py show hola_mundo.py
```

Para ver una versión anterior (ej. versión 2):
```bash
python3 view_versions.py show hola_mundo.py 2
```

### Comparar dos versiones

Para comparar la salida de dos versiones diferentes:
```bash
python3 view_versions.py compare hola_mundo.py 1 2
```

Donde 1 es la versión más reciente y 2 es la versión anterior.

### Ver ayuda completa

```bash
python3 view_versions.py help
```

## Requisitos

- Python 3.x

## Contenido de los Scripts

### hola_mundo.py
Un programa simple que imprime un saludo personalizado.

### leccion1.py
Introducción a:
- Variables (Strings, Integers, Booleans)
- La función `print()`
- Formato de cadenas con f-strings

## 💡 Características del Sistema de Versiones

- **Seguimiento automático**: Cada vez que ejecutas `run_all.py`, las salidas se guardan automáticamente
- **Información de Git**: Cada versión incluye el commit y branch de Git
- **Marca de tiempo**: Todas las versiones tienen fecha y hora precisa
- **Comparación**: Compara fácilmente las salidas entre diferentes versiones
- **Historial completo**: Mantén un registro de cómo ha evolucionado tu código

---

❤️ ¡Feliz aprendizaje de Python!
