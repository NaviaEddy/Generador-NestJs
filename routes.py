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
    return render_template("index.html")

@routes.route("/generate_project", methods=["POST"])
def set_project_name():
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
    data = request.json
    success, result, message = get_audit_table(data["db"], data["user"], data["password"], data["host"], data["port"], data["table_name"])
    return jsonify({"success": success, "result": result, "message": message}), 200


@routes.route("/generate_tables", methods=["POST"])
def generate_tables():
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
    