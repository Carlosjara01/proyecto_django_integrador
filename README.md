# 🛒 Proyecto Django Integrador: Sistema de Gestión de Productos

Este es un proyecto desarrollado con **Django** que simula un sistema de gestión de productos para una tienda. Incluye modelos de datos para Productos, Categorías y Proveedores, así como funcionalidades CRUD (Crear, Leer, Actualizar y Eliminar) y gestión de APIs.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django (versión [PONER VERSIÓN DE DJANGO])
* **Base de Datos:** SQLite3 (por defecto)
* **Frontend:** HTML, CSS, JavaScript, Bootstrap 5

## ⚙️ Instalación y Configuración

Sigue estos pasos para tener una copia local del proyecto funcionando en tu máquina.

### Requisitos Previos

Necesitas tener instalado Python y Git en tu sistema.

### Pasos

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Carlosjara01/proyecto_django_integrador.git](https://github.com/Carlosjara01/proyecto_django_integrador.git)
    cd proyecto_django_integrador
    ```

2.  **Crear y activar el entorno virtual (venv):**
    ```bash
    python -m venv venv
    # En Windows PowerShell:
    .\venv\Scripts\Activate.ps1
    # O en Linux/macOS:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    Instala todas las librerías necesarias (Django, etc.):
    ```bash
    pip install -r requirements.txt
    # O si no tienes requirements.txt, usa:
    pip install django djangorestframework
    ```

4.  **Ejecutar migraciones:**
    Crea la base de datos y aplica las migraciones.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
    *(Opcional: Crea un superusuario para acceder al panel de administración: `python manage.py createsuperuser`)*

5.  **Ejecutar el servidor:**
    ```bash
    python manage.py runserver
    ```
    El proyecto estará disponible en `http://127.0.0.1:8000/`.

## 📌 Endpoints de la API (DRF)

El proyecto expone una API RESTful para la gestión de productos:

| Ruta | Método | Descripción |
| :--- | :--- | :--- |
| `/api/productos/` | GET | Listar todos los productos. |
| `/api/productos/` | POST | Crear un nuevo producto. |
| `/api/productos/<id>/` | GET | Obtener detalles de un producto específico. |
| `/api/productos/<id>/` | PUT/PATCH | Actualizar un producto existente. |
| `/api/productos/<id>/` | DELETE | Eliminar un producto. |

## 🤝 Autor

**Carlos Jara**

* carloscj0971@gmail.com

---
*(Este proyecto fue desarrollado de manera individual)*
