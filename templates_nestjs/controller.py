import os

class controller_template:
    def __init__(self, app_path: str, table_path: str, table_name: str):
        self.app_path = app_path
        self.table_path = table_path
        self.table_name = table_name
        if "_" in self.table_name:
            self.table_name_pascal = '_'.join(word.capitalize() for word in self.table_name.split('_'))
        else:
            self.table_name_pascal = self.table_name.capitalize()  # Si no tiene '_', solo capitaliza la primera letra
        self.import_line = f"import {{ {self.table_name_pascal}Controller }} from './{self.table_name}/{self.table_name}.controller';\n"
        
    def create_controller_file(self):
        """Crea la estructura de archivos para los controladores"""
        try:
            self._create_controller()
            self._update_app_module_controller()
            return True
        except Exception as e:
            print(f"Error creating controller file: {str(e)}")
            return False
    
    
    def _create_controller(self):
        content = f"""import {{ 
    Controller, 
    Get,
    Post,
    Put,
    Delete,
    Body,
    NotFoundException,
    InternalServerErrorException,
    Param,
    UseGuards,
}} from '@nestjs/common';
import {{ {self.table_name_pascal}Service }} from './{self.table_name}.service';
import {{ {self.table_name} }} from '@prisma/client';
import {{ AuthGuard }} from '../auth/auth.guard';

@Controller('{self.table_name}')
export class {self.table_name_pascal}Controller {{
    constructor(private readonly {self.table_name}Service: {self.table_name_pascal}Service) {{}}

    @Get()
    @UseGuards(AuthGuard)
    async get{self.table_name_pascal}(){{
        return this.{self.table_name}Service.get{self.table_name_pascal}();
    }}

    @Get(':id')
    @UseGuards(AuthGuard)
    async get{self.table_name_pascal}ById(@Param('id') id: string) {{
        const {self.table_name}_id = await this.{self.table_name}Service.get{self.table_name_pascal}ById(
            Number(id),
        );
        if (!{self.table_name}_id)
            throw new NotFoundException('No se encontró el registro.');
        return {self.table_name}_id;
    }}

    @Post()
    @UseGuards(AuthGuard)
    async create{self.table_name_pascal}(@Body() data: {self.table_name}) {{
        const {self.table_name}_create = 
            await this.{self.table_name}Service.create{self.table_name_pascal}(data);
        if (!{self.table_name}_create)
            throw new InternalServerErrorException('No se pudo crear el registro.');
        return {self.table_name}_create;
    }}

    @Put(':id')
    @UseGuards(AuthGuard)
    async update{self.table_name_pascal}(@Body() data: {self.table_name}, @Param('id') id: string) {{
        const {self.table_name}_update = 
            await this.{self.table_name}Service.update{self.table_name_pascal}(Number(id), data);
        if (!{self.table_name}_update)
            throw new InternalServerErrorException('No se pudo actualizar el registro.');
        return {self.table_name}_update;
    }}

    @Delete(':id')
    @UseGuards(AuthGuard)
    async delete{self.table_name_pascal}(@Param('id') id: string) {{
        const {self.table_name}_delete = 
            await this.{self.table_name}Service.delete{self.table_name_pascal}(Number(id));
        if (!{self.table_name}_delete)
            throw new InternalServerErrorException('No se pudo eliminar el registro.');
        return {self.table_name}_delete;
    }}
}}
"""
        self._write_file(f"{self.table_name}.controller.ts", content)

    def _write_file(self, filename: str, content: str):
        file_path = os.path.join(self.table_path, filename)
        with open(file_path, "w") as f:
            f.write(content)

    def _update_app_module_controller(self):
        try:
            with open(self.app_path, "r") as file:
                lines = file.readlines()
            
            # Revisar si ya está importado
            if any(self.import_line.strip() in line.strip() for line in lines):
                print(f"El Controlador {self.table_name} ya está importado.")
                return
            
            # Insertar la importación después de las existentes
            import_index = next((i for i, line in enumerate(lines) if "import" not in line), len(lines))
            lines.insert(import_index, self.import_line)
            
            # Buscar la sección donde están los providers
            for i, line in enumerate(lines):
                if "controllers: [" in line:
                    end_index = i
                    while "]" not in lines[end_index]:
                        end_index += 1
                    
                    # Insertar el nuevo servicio en la lista de providers
                    lines[end_index] = lines[end_index].replace("]", f", {self.table_name_pascal}Controller ]")
                    break
            
            # Escribir los cambios en el archivo
            with open(self.app_path, "w") as file:
                file.writelines(lines)

            print(f"Controlador {self.table_name} agregado exitosamente a {self.app_path}.")
        
        except Exception as e:
            print(f"Error actualizando {self.app_path}: {str(e)}")