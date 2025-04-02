import os

class module_template:
    def __init__(self, app_path: str, table_path: str, table_name: str):
        self.app_path = app_path
        self.table_path = table_path
        self.table_name = table_name
        if "_" in self.table_name:
            self.table_name_pascal = '_'.join(word.capitalize() for word in self.table_name.split('_'))
        else:
            self.table_name_pascal = self.table_name.capitalize()  # Si no tiene '_', solo capitaliza la primera letra
        self.import_line = f"import {{ {self.table_name_pascal}Module }} from './{self.table_name}/{self.table_name}.module';\n"
        
    def create_module_file(self):
        """Crea la estructura de archivos para los modulos"""
        try:
            self._create_module()
            self._update_app_module_imports()
            return True
        except Exception as e:
            print(f"Error creating module file: {str(e)}")
            return False
    
    
    def _create_module(self):
        content = f"""import {{ Module }} from '@nestjs/common';
import {{ {self.table_name_pascal}Controller }} from './{self.table_name}.controller';
import {{ {self.table_name_pascal}Service }} from './{self.table_name}.service';
import {{ PrismaModule }} from 'prisma/prisma.module';

@Module({{
    providers: [{self.table_name_pascal}Service],
    controllers: [{self.table_name_pascal}Controller],
    imports: [PrismaModule],
}})
export class {self.table_name_pascal}Module {{}}
"""
        self._write_file(f"{self.table_name}.module.ts", content)

    def _write_file(self, filename: str, content: str):
        file_path = os.path.join(self.table_path, filename)
        with open(file_path, "w") as f:
            f.write(content)

    def _update_app_module_imports(self):
        try:
            with open(self.app_path, "r") as file:
                lines = file.readlines()
            
            # Revisar si ya está importado
            if any(self.import_line.strip() in line.strip() for line in lines):
                print(f"El Modulo {self.table_name} ya está importado.")
                return
            
            # Insertar la importación después de las existentes
            import_index = next((i for i, line in enumerate(lines) if "import" not in line), len(lines))
            lines.insert(import_index, self.import_line)
            
            # Buscar la sección donde están los providers
            for i, line in enumerate(lines):
                if "imports: [" in line:
                    end_index = i
                    while "]" not in lines[end_index]:
                        end_index += 1
                    
                    # Insertar el nuevo servicio en la lista de providers
                    lines[end_index] = lines[end_index].replace("]", f", {self.table_name_pascal}Module ]")
                    break
            
            # Escribir los cambios en el archivo
            with open(self.app_path, "w") as file:
                file.writelines(lines)

            print(f"Modulo {self.table_name} agregado exitosamente a {self.app_path}.")
        
        except Exception as e:
            print(f"Error actualizando {self.app_path}: {str(e)}")