import os

class user_template:
    def __init__(self, app_path: str, base_path: str, name: str):
        self.app_path = app_path
        self.base_path = base_path
        self.name = name

    def create_user_files(self):
        """Crea la estructura de archivos para los modulos"""
        try:
            self._create_user_module()
            self._create_user_service()
            self._update_app_module_imports()
            return True
        except Exception as e:
            print(f"Error creating auth files: {str(e)}")
            return False
    
    def _create_user_module(self):
        content = f"""import {{ Module }} from '@nestjs/common';
import {{ UserService }} from './user.service';

@Module({{
  providers: [UserService],
  exports: [UserService],
}})
export class UserModule {{}}

"""
        self._write_file("user.module.ts", content)

    def _create_user_service(self):
        content = f"""import {{ Injectable }} from '@nestjs/common';

@Injectable()
export class UserService {{
  private readonly users = [
    {{
      userId: 1,
      email: 'admin@gmail.com',
      password: 'admin',
      rol: 'admin',
    }},
    {{
      userId: 2,
      email: 'user@gmail.com',
      password: 'user',
      rol: 'user',
    }},
  ];

  findOne(email: string) {{
    const user = this.users.find((user) => user.email === email);
    return user;
  }}
}}
"""
        self._write_file("user.service.ts", content)

    def _update_app_module_imports(self):
        try:
            with open(self.app_path, "r") as file:
                lines = file.readlines()
            
            # Insertar la importación después de las existentes
            import_statement = "import { UserModule } from './user/user.module';\n"
            import_index = next((i for i, line in enumerate(lines) if "import" not in line), len(lines))
            lines.insert(import_index, import_statement)
            
            # Buscar la sección donde están los imports y agregar UserModule
            for i, line in enumerate(lines):
                if "imports: [" in line:
                    end_index = i
                    while "]" not in lines[end_index]:
                        end_index += 1
                    # Insertar UserModule en la lista de imports (evitando duplicados)
                    if "UserModule" not in "".join(lines[i:end_index+1]):
                        lines[end_index] = lines[end_index].replace("]", f", UserModule ]")
                    break
            
            # Escribir los cambios en el archivo
            with open(self.app_path, "w") as file:
                file.writelines(lines)

            print(f"UserModule agregado exitosamente a {self.app_path}.")
        
        except Exception as e:
            print(f"Error actualizando {self.app_path}: {str(e)}")


    def _write_file(self, filename: str, content: str):
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, "w") as f:
            f.write(content)
        print(f"User file {filename} created successfully at {file_path}.")