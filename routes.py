import os
import subprocess
import time
from flask import Blueprint, render_template, request, jsonify
from config import test_connection, get_tables, get_audit_table
from templates_nestjs.prisma import prisma_template
from templates_nestjs.controller import controller_template
from templates_nestjs.module import module_template
from templates_nestjs.service import service_template
from templates_nestjs.auth import auth_template
from templates_nestjs.user import user_template

routes = Blueprint("routes", __name__)

proyect_name = ""

@routes.route("/", methods=["GET"])
def index():
    """
    La función `index` en una aplicación Python Flask sirve la plantilla `index.html` cuando se realiza una petición GET
    a la ruta raíz.
    :return: La función `index()` devuelve el resultado de renderizar la plantilla «index.html».
    """
    return render_template("index.html")

@routes.route("/generate_project", methods=["POST"])
def set_project_name():
    """
    Esta función de Python establece el nombre del proyecto a partir de una solicitud POST, ejecuta un subproceso para crear un proyecto NestJS
    utilizando un script por lotes, y devuelve mensajes de éxito o error en consecuencia.
    :return: La función `set_project_name()` devuelve una respuesta JSON con un estado de éxito y un
    mensaje basado en el resultado del proceso de generación del proyecto.
    """
    global proyect_name
    try:
        data = request.json
        proyect_name = data.get("project")
        if not proyect_name:
            raise ValueError("El nombre del proyecto es requerido.")

        try:
            subprocess.run(
                [
                    "cmd",
                    "/c",
                    "D:\\USFX\\8vo Semestre - CICO\\SHC134\\Practica3\\generator-nestjs\\create_nestjs_project.bat",
                    proyect_name,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": f"Error al ejecutar el script: {str(e)}",
                    }
                ),
                500,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "message": f'Proyecto "{proyect_name}" creado exitosamente.',
                }
            ),
            201,
        )

    except ValueError as ve:
        return jsonify({"success": False, "message": str(ve)}), 400

    except Exception as e:
        return (
            jsonify({"success": False, "message": "Ocurrió un error inesperado."}),
            500,
        )


@routes.route("/test_db", methods=["POST"])
def test_db():
    """
    Esta función Python prueba una conexión de base de datos, recupera tablas si tiene éxito, genera archivos Prisma
    y devuelve una respuesta JSON con el estado de éxito, el mensaje y las tablas.
    :return: El código devuelve una respuesta JSON con las claves «success», «message» y «tables» si
    los archivos Prisma se han generado correctamente. Si se produce un error durante la generación de los archivos Prisma
    devuelve una respuesta JSON con el valor False de «success» y un mensaje que indica un error inesperado.
    inesperado.
    """
    base_path = f"./nestjs/{proyect_name}/"
    app_path = f"./nestjs/{proyect_name}/src/app.module.ts"
    data = request.json
    success, message = test_connection(
        data["db"], data["user"], data["password"], data["host"], data["port"]
    )
    tables = (
        get_tables(
            data["db"], data["user"], data["password"], data["host"], data["port"]
        )
        if success
        else []
    )

    # ======== Generar archivos prisma ========
    prisma_generator = prisma_template(app_path, base_path, data)
    prisma_success = prisma_generator.create_prisma_files()
    if prisma_success:
        return jsonify({"success": success, "message": message, "tables": tables}), 200
    else:
        return jsonify({"success": False, "message": "Ocurrio un error inesperado"}), 500
    #return jsonify({"success": success, "message": message, "tables": tables}), 200

@routes.route("/test_db_audit", methods=["POST"])
def test_db_audit():
    """
    Esta función comprueba una conexión a una base de datos y recupera tablas basándose en las credenciales de la base de datos proporcionadas.
    proporcionadas.
    :return: La función `test_db_audit` devuelve una respuesta JSON con tres pares clave-valor:
    «success» que indica si la prueba de conexión se ha realizado correctamente, “message” que proporciona un mensaje
    relacionado con el éxito o el fracaso de la prueba de conexión, y «tables» que contiene una lista de tablas
    si la prueba de conexión se ha realizado correctamente o una lista vacía en caso contrario. El código de estado HTTP devuelto
    es 200 (OK) si la prueba de conexión es exitosa, o 500 (Error interno del servidor) si hay un error inesperado.
    """
    data = request.json
    success, message = test_connection(
        data["db"], data["user"], data["password"], data["host"], data["port"]
    )
    tables = (
        get_tables(
            data["db"], data["user"], data["password"], data["host"], data["port"]
        )
        if success
        else []
    )

    return jsonify({"success": success, "message": message, "tables": tables}), 200

@routes.route("/generate_audit_tables", methods=["POST"])
def generate_audit_tables():
    """
    La función `generate_audit_tables` recibe datos JSON, llama a `get_audit_table` con los parámetros especificados y devuelve el resultado como respuesta JSON.
    y devuelve el resultado como una respuesta JSON.
    :return: La función `generate_audit_tables` devuelve una respuesta JSON con tres claves:
    «success», “result”, y “message”. Los valores de estas claves se obtienen de la función
    que se llama con los datos proporcionados en la solicitud POST. La respuesta
    se devuelve con un código de estado 200.
    """
    data = request.json
    success, result, message = get_audit_table(data["db"], data["user"], data["password"], data["host"], data["port"], data["table_name"])
    return jsonify({"success": success, "result": result, "message": message}), 200


@routes.route("/generate_tables", methods=["POST"])
def generate_tables():
    """
    La función `generate_tables` crea archivos de controlador, módulo, servicio, usuario y autenticación basados en los datos de entrada del proyecto NestJS.
    datos de entrada para un proyecto NestJS.
    :return: La función `generate_tables()` devuelve una respuesta JSON con un estado de éxito y los datos de las tablas procesadas.
    datos de las tablas que se procesaron. La respuesta incluye un código de estado 201 (Creado) si la
    operación fue exitosa.
    """
    global proyect_name
    data = request.json
    tables = data.get("tables", [])
    base_path = f"./nestjs/{proyect_name}/src/"
    app_path = f"./nestjs/{proyect_name}/src/app.module.ts"

    if not os.path.exists(base_path):
        return jsonify({"success": False, "message": "El proyecto no existe."}), 404

    for table in tables:
        table_name = table.get("table")
        id_table = table.get("first_attribute")
        # ======== Generar carpeta  ========
        table_path = os.path.join(base_path, table_name)
        if not os.path.exists(table_path):
            os.makedirs(table_path)

        # ======== Generar archivos del controlador ========
        controller_generator = controller_template(app_path, table_path, table_name)
        controller_success = controller_generator.create_controller_file()
        if controller_success:
            print(f"Controller files for {table_name} created successfully.")
        else:
            print(f"Error creating controller files for {table_name}.")

        # ======== Generar archivos del modelo ========
        module_generator = module_template(app_path, table_path, table_name)
        module_success = module_generator.create_module_file()
        if module_success:
            print(f"Module files for {table_name} created successfully.")
        else:
            print(f"Error creating module files for {table_name}.")

        # ======== Generar archivos del servicio ========
        service_generator = service_template(app_path, table_path, table_name, id_table)
        service_success = service_generator.create_service_file()
        if service_success:
            print(f"Service files for {table_name} created successfully.")
        else:
            print(f"Error creating service files for {table_name}.")

        time.sleep(0.5)
    
    # ======== Generar archivos del user ========
    table_path = os.path.join(base_path, "user")
    if not os.path.exists(table_path):
        os.makedirs(table_path)

    user_generator = user_template(app_path, table_path, "user")
    user_success = user_generator.create_user_files()
    if user_success:
        print(f"User files created successfully.")
    else:
        print(f"Error creating user files.")

    # ======== Generar archivos del auth ========
    table_path = os.path.join(base_path, "auth")
    if not os.path.exists(table_path):
        os.makedirs(table_path)
    
    auth_generator = auth_template(app_path, table_path, "auth")
    auth_success = auth_generator.create_auth_files()
    if auth_success:
        print(f"Auth files created successfully.")
    else:
        print(f"Error creating auth files.")

    return jsonify({"success": True, "data": tables}), 201


@routes.route("/run_server", methods=["POST"])
def run_server():
    """
    La función `run_server` en este fragmento de código Python inicia un servidor para un proyecto usando el subproceso
    y devuelve mensajes de éxito o error en consecuencia.
    :return: La función `run_server` devuelve una respuesta JSON con un estado de éxito y un mensaje.
    """
    global proyect_name
    try:
        if not proyect_name:
            raise ValueError("El nombre del proyecto es requerido.")

        try:
            subprocess.run(
                [
                    "cmd",
                    "/c",
                    "D:\\USFX\\8vo Semestre - CICO\\SHC134\\Practica3\\generator-nestjs\\run_nestjs_project.bat",
                    proyect_name,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": f"Error al iniciar el servidor: {str(e)}",
                    }
                ),
                500,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "message": 'Servidor en ejecucion!',
                }
            ),
            201,
        )

    except ValueError as ve:
        return jsonify({"success": False, "message": str(ve)}), 400

    except Exception as e:
        return (
            jsonify({"success": False, "message": "Ocurrió un error inesperado."}),
            500,
        )
    