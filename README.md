# 🛠️ Generador NestJs

Generador NestJs es una aplicación web desarrollada en Python con Flask, diseñada para generar la estructura base de proyectos NestJS de forma automatizada.

## ✨ Características

- **Generación automatizada:** Crea la estructura inicial para proyectos NestJS.
- **Interfaz web intuitiva:** Permite configurar parámetros y personalizar la generación del proyecto.
- **Integración opcional:** Compatible con Node.js y NestJS CLI para continuar el desarrollo del proyecto generado.

## 📋 Requisitos

- **Python 3.6+** (se recomienda Python 3.8 o superior)
- **Node.js y NestJS CLI** para trabajar con el proyecto generado.

## 📁 Estructura del Proyecto
```plaintext
Generador-NestJs/
├── app.py                  # Archivo principal para iniciar la aplicación Flask.
├── config.py               # Configuración general de la aplicación.
├── requirements.txt        # Dependencias necesarias para el proyecto.
├── templates/              # Archivos de plantillas HTML para la interfaz web.
├── static/                 # Archivos estáticos (CSS, JavaScript, imágenes).
├── generators/             # Módulo encargado de la generación del código NestJS.
├── nestjs/                 # Carpeta donde se generaran los proyectos de NestJS.
└── README.md               # Documentación y detalles del proyecto.
```

## ⬇️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/NaviaEddy/Generador-NestJs.git
```
### 2. Dirigirse al directorio del proyecto
```bash
cd Generador-NestJs
```
### 3. Crear un entorno virtual (opcional, pero recomendado)
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```
### 4. Instalar las dependencias
```bash
pip install -r requirements.txt
```

## ⚙️ Configuraciones y Personalizaciones
  - **Clave Secreta de Flask**: La variable app.secret_key en app.py debe modificarse por una clave secreta segura para producción.
  - **Parámetros de Conexión a PostgreSQL**: Verifique y ajuste los parámetros de conexión según la configuración de su servidor de base de datos.

## 🚀 Ejecución del Proyecto

Para ejecutar la aplicación, asegúrate de haber instalado las dependencias y luego corre:
```bash
python app.py
```
La aplicación se ejecutará en el puerto 5000 por defecto. Accede a ella en tu navegador en:
```bash
http://127.0.0.1:5000
```
## 🔧 Uso de la Aplicación
  1. Accede a la interfaz web.
  2. Configura los parámetros necesarios para generar tu proyecto NestJS.
  3. Haz clic en el botón para generar la estructura base del proyecto.
  4. Ingresa tus credenciales PostgreSql.
  5. Selecciona las tablas que deseas generar.
  6. Haz correr el proyecto
  7. La estructura generada se guardará en la ubicación definida.

## 👥 Contribuciones
Siéntase libre de contribuir a este proyecto. Puede abrir un issue o enviar un pull request con sus mejoras.

## 📄 Licencia
Este proyecto está bajo la licencia MIT.
