import os

class service_template:
    def __init__(self, app_path: str, table_path: str, table_name: str, id_table: str):
        self.app_path = app_path
        self.table_path = table_path
        self.table_name = table_name
        self.id_table = id_table
        if "_" in self.table_name:
            self.table_name_pascal = '_'.join(word.capitalize() for word in self.table_name.split('_'))
        else:
            self.table_name_pascal = self.table_name.capitalize()  # Si no tiene '_', solo capitaliza la primera letra
        self.import_line = f"import {{ {self.table_name_pascal}Service }} from './{self.table_name}/{self.table_name}.service';\n"
        
    def create_service_file(self):
        """Crea la estructura de archivos para los modulos"""
        try:
            self._create_service()
            self._update_app_module_service()
            return True
        except Exception as e:
            print(f"Error creating service file: {str(e)}")
            return False
    
    
    def _create_service(self):
        content = f"""import {{ Injectable }} from '@nestjs/common';
import {{ PrismaService }} from '../../prisma/prisma.service';
import {{ {self.table_name} }} from '@prisma/client';

@Injectable()
export class {self.table_name_pascal}Service {{
    constructor(private readonly prisma: PrismaService) {{}}

    async get{self.table_name_pascal}(): Promise<{self.table_name}[]> {{
        return this.prisma.{self.table_name}.findMany();
    }}

    async get{self.table_name_pascal}ById(id: number): Promise<{self.table_name} | null> {{
        return this.prisma.{self.table_name}.findUnique({{ 
            where: {{ 
                {self.id_table}: id, 
            }} 
        }});
    }}

    async create{self.table_name_pascal}(data: {self.table_name}): Promise<{self.table_name}> {{
        return this.prisma.{self.table_name}.create({{ 
            data 
        }});
    }}

    async update{self.table_name_pascal}(
        id: number, 
        data: {self.table_name},
    ): Promise<{self.table_name}> {{
        return this.prisma.{self.table_name}.update({{ 
            where: {{ 
                {self.id_table}: id, 
            }}, 
            data,
        }});
    }}

    async delete{self.table_name_pascal}(id: number): Promise<{self.table_name} | null> {{
        return this.prisma.{self.table_name}.delete({{ 
            where: {{ 
                {self.id_table}: id, 
            }} 
        }});
    }}
    
}}
"""
        self._write_file(f"{self.table_name}.service.ts", content)

    def _write_file(self, filename: str, content: str):
        file_path = os.path.join(self.table_path, filename)
        with open(file_path, "w") as f:
            f.write(content)

    def _update_app_module_service(self):
        try:
            with open(self.app_path, "r") as file:
                lines = file.readlines()
            
            # Revisar si ya está importado
            if any(self.import_line.strip() in line.strip() for line in lines):
                print(f"El servicio {self.table_name} ya está importado.")
                return
            
            # Insertar la importación después de las existentes
            import_index = next((i for i, line in enumerate(lines) if "import" not in line), len(lines))
            lines.insert(import_index, self.import_line)
            
            # Buscar la sección donde están los providers
            for i, line in enumerate(lines):
                if "providers: [" in line:
                    end_index = i
                    while "]" not in lines[end_index]:
                        end_index += 1
                    
                    # Insertar el nuevo servicio en la lista de providers
                    lines[end_index] = lines[end_index].replace("]", f", {self.table_name_pascal}Service ]")
                    break
            
            # Escribir los cambios en el archivo
            with open(self.app_path, "w") as file:
                file.writelines(lines)

            print(f"Servicio {self.table_name} agregado exitosamente a {self.app_path}.")
        
        except Exception as e:
            print(f"Error actualizando {self.app_path}: {str(e)}")
