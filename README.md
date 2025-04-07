# 🛠️ Generador NestJs

Generador NestJs es una aplicación web desarrollada en Python con Flask, diseñada para generar la estructura base de proyectos NestJS de forma automatizada.

## ✨ Características

- **Generación automatizada:** Crea la estructura inicial para proyectos NestJS.
- **Interfaz web intuitiva:** Permite configurar parámetros y personalizar la generación del proyecto.
- **Integración opcional:** Compatible con Node.js y NestJS CLI para continuar el desarrollo del proyecto generado.

## 📋 Requisitos

- **Python 3.6+** (se recomienda Python 3.8 o superior)
- **Node.js y NestJS CLI** para trabajar con el proyecto generado.
- **PostgreSQL**

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
> [!NOTE]
> En el módulo **User**, asegúrate de configurarlo con la tabla `User` respectiva de tu base de datos, ya que el módulo que se genera inicialmente solo contiene datos estáticos y no está conectado a ninguna
> base de datos. Esto es importante para asegurar el rendimiento del JWT en las rutas de los demás módulos.

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
1. Interfaz principal, puedes generar un proyecto o realizar un auditoria
   ![image](https://github.com/user-attachments/assets/c9c63719-127c-4695-85d9-06e763c98e91)
2. Ingresa a crear un proyecto y escribes un nombre para el proyecto
   ![image](https://github.com/user-attachments/assets/d717a99f-4f70-4112-8b50-e7d35167921b)
   ![image](https://github.com/user-attachments/assets/08d830e3-d9d4-4916-a33a-6331593ad7e0)
   - Empezara a descargar todo lo necesario para el proyecto (puedes verificarlo en la consola de ejecucion)
     ![Screenshot 2025-04-07 053050](https://github.com/user-attachments/assets/89932f71-ccc0-40ff-96f0-4ab22bb9af6f)
3. Proyecto creado exitosamente
   ![image](https://github.com/user-attachments/assets/bf4b1228-c0af-4454-a942-1b0c09517bb5)
5. Ingresa tus credenciales de acceso a tu base de datos
   > [!IMPORTANT]
   > La base de datos debe estar vacia, ya que hara una limpieza para no tener problemas
   ![image](https://github.com/user-attachments/assets/1aa1fed2-2203-48b2-af1f-0de435e368e0)
6. Se desplegara todas las tablas creadas en tu base de datos con la opcion para elegir que tablas quieres generar o si quieres generar todas las tablas
   ![image](https://github.com/user-attachments/assets/0b4819c3-5a52-43cb-9fed-620e05a0735a)
7. Seleccion las tablas interesadas
   ![image](https://github.com/user-attachments/assets/a945c15c-66d7-4370-9075-6b262730b740)
8. Dale al boton Generar
   ![image](https://github.com/user-attachments/assets/232887f6-9219-44ec-b302-63a7306c822e)
   - Puedes fijarte en la consola de ejecucion que procesos archivos creo
     ![image](https://github.com/user-attachments/assets/38beb4e9-90d8-4177-8bdc-4e7d893cc8cc)
9. Tu proyecto ya estara creado en la carpeta ./nestjs/
   ![image](https://github.com/user-attachments/assets/df4bada6-d9ee-476f-9246-38c96c4f7beb)
10. Dale al boton Run_server, iniciara el servidor de tu proyecto!
    ![image](https://github.com/user-attachments/assets/ab60301a-9305-43cd-bd72-4fff7c012727)
    - Vista desde la consola de ejecucion
    ![image](https://github.com/user-attachments/assets/3690006d-c5e9-422a-8c1a-9dcb4ae08c42)
    > [!IMPORTANT]
    > Debes aceptar el procedimiento de las migraciones a la base de datos (Y/N) en la consola
    ![image](https://github.com/user-attachments/assets/ddb70263-e7dc-47b0-9a96-65f3d8cbffa5)
11. Tu proyecto ya esta corriendo!!!
    ![image](https://github.com/user-attachments/assets/ed6359bb-b4d4-45dd-b932-07967c1c2c11)
12. Dale al boton de Generar configuracion de auditoria
    ![image](https://github.com/user-attachments/assets/2da97d6d-508c-4d25-9ac2-3b6e08766734)
13. Mensaje de exito con la configuracion realiza
    > [!CAUTION]
    > La clave de encriptacion no la debes compartir con nadie
    ![image](https://github.com/user-attachments/assets/78534771-28cb-4559-ab36-79d87231bf5c)
14. Ingresas datos de prueba con Postman.
    - Debes logearte, todas las rutas estan protegidas con JWT
      ![image](https://github.com/user-attachments/assets/bc11b3ca-02d0-453e-8ef5-43f5e541fe9a)
    - Ingresas el token generado en el apartado de Authorization, en el tipo de token eliges BEARER y pegas el token
      ![image](https://github.com/user-attachments/assets/d0f67cf6-cbf7-4761-be15-d5d550cf5117)
    - Mandas la solicitud de creacion
      ![image](https://github.com/user-attachments/assets/23a45e01-e14e-40da-b916-e9b7de13f00a)
    > [!NOTE]
    > Tu proyecto de NestJS ya esta listo para trabajar!!!!
15. Para realizar una auditoria a la base de datos necesitas ir al inicio del sistema y elegir el apartado Auditoria.
    ![image](https://github.com/user-attachments/assets/0732eba9-3611-4c27-ace0-d893dd5803fc)
16. Ingresa las credenciales de tu base de datos
    ![image](https://github.com/user-attachments/assets/06a6eeaa-2513-4f87-b913-c95ca12181df)
17. Elige una tabla a la cual quieras realizar una auditoria.
    > [!NOTE]
    > Las tablas para la auditoria estan encriptadas y creadas en un esquema privado para mas seguridad en PostgreSQL
    ![image](https://github.com/user-attachments/assets/1f1361a8-3752-4c70-b9aa-4251263d0060)
18. La tabla elegida con los datos desencriptados
    ![image](https://github.com/user-attachments/assets/e9385e8d-73f2-439a-8ad6-080b18d0bbab)

## 👥 Contribuciones
Siéntase libre de contribuir a este proyecto. Puede abrir un issue o enviar un pull request con sus mejoras.

## 📄 Licencia
Este proyecto está bajo la licencia MIT.
