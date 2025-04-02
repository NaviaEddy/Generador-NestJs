import os

class prisma_template:
    def __init__(self, app_path: str, base_path: str, data: dict):
        self.data = data
        self.app_path = app_path
        self.base_path = base_path
        self.prisma_dir = os.path.join(self.base_path, "prisma")
        self.import_line = f"import {{ PrismaModule }} from 'prisma/prisma.module';\n"
        
    def create_prisma_files(self):
        """Crea la estructura de archivos para Prisma"""
        try:
            self._create_directory()
            self._create_schema_prisma()
            self._create_prisma_module()
            self._create_prisma_service()
            self._create_env()
            self._update_app_module_imports()
            return True
        except Exception as e:
            print(f"Error creating Prisma files: {str(e)}")
            return False
    
    def _create_directory(self):
        """Crea el directorio prisma si no existe"""
        os.makedirs(self.prisma_dir, exist_ok=True)
    
    def _create_schema_prisma(self):
        content = """generator client {
    provider = "prisma-client-js"
}

datasource db {
    provider = "postgresql"
    url      = env("DATABASE_URL")
}
"""
        self._write_file("schema.prisma", content)
    
    def _create_prisma_module(self):
        content = """import { Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Module({
    providers: [PrismaService],
    exports: [PrismaService],
})
export class PrismaModule {}
"""
        self._write_file("prisma.module.ts", content)
    
    def _create_prisma_service(self):
        content = """import { Injectable, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
    async onModuleInit() {
        await this.$connect();
    }
}
"""
        self._write_file("prisma.service.ts", content)
    
    def _write_file(self, filename: str, content: str):
        file_path = os.path.join(self.prisma_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
    
    def _update_app_module_imports(self):
        try:
            with open(self.app_path, "r") as file:
                lines = file.readlines()
            
            # Revisar si ya está importado
            if any(self.import_line.strip() in line.strip() for line in lines):
                print(f"El Modulo prisma ya está importado.")
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
                    lines[end_index] = lines[end_index].replace("]", f"PrismaModule ]")
                    break
            
            # Escribir los cambios en el archivo
            with open(self.app_path, "w") as file:
                file.writelines(lines)

            print(f"Modulo prisma agregado exitosamente a {self.app_path}.")
        
        except Exception as e:
            print(f"Error actualizando {self.app_path}: {str(e)}")

    def _create_env(self):
        content = f"""DATABASE_URL="postgresql://{self.data["user"]}:{self.data["password"]}@{self.data["host"]}:{self.data["port"]}/{self.data["db"]}?schema=public"
        """
        file_path = os.path.join(self.base_path, ".env")
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Archivo .env creado exitosamente en {self.base_path}.")