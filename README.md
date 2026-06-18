# ✨ Shinny Tienda

Shinny Tienda es una tienda virtual desarrollada con **Django**, diseñada para exhibir y gestionar productos de joyería y accesorios de forma sencilla y elegante.

## 🚀 Características

* 🛍️ Catálogo de productos con imágenes y descripciones.
* 📂 Organización por colecciones y categorías.
* ⭐ Productos destacados y promociones.
* 🛒 Carrito de compras.
* 📱 Contacto directo por WhatsApp.
* ⚙️ Panel administrativo para gestionar productos y configuraciones.
* 🎨 Diseño responsivo y moderno.
* ☁️ Aplicación desplegada en Railway.

## 🛠 Tecnologías utilizadas

* Python 3.12
* Django 5
* PostgreSQL
* HTML5
* CSS3
* JavaScript
* Bootstrap
* Gunicorn
* WhiteNoise
* Railway

## 📂 Estructura del proyecto

```text
shinnytienda/
│
├── products/      # Gestión de productos y colecciones
├── store/         # Información de la tienda
├── cart/          # Carrito de compras
├── templates/     # Plantillas HTML
├── static/        # Archivos estáticos
├── media/         # Imágenes y archivos subidos
├── manage.py
└── requirements.txt
```

## ⚙️ Instalación

```bash
git clone https://github.com/TU_USUARIO/shinnytienda.git
cd shinnytienda

python -m venv .venv

# Windows
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## 🌐 Despliegue

La aplicación se encuentra desplegada y en funcionamiento utilizando:

* Railway
* PostgreSQL
* Gunicorn
* WhiteNoise

## 📌 Estado del proyecto

🟢 **Activo y desplegado en producción**

Shinny Tienda se encuentra actualmente operativa y continúa recibiendo mejoras y nuevas funcionalidades.
