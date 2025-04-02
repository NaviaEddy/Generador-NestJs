import os

class auth_template:
    def __init__(self, app_path: str, base_path: str, name: str):
        self.app_path = app_path
        self.base_path = base_path
        self.name = name

    def create_auth_files(self):
        """Crea la estructura de archivos para los modulos"""
        try:
            self._create_auth_module()
            self._create_auth_service()
            self._create_auth_controller()
            self._create_auth_guard()
            self._create_constants()
            self._update_app_module_imports()
            return True
        except Exception as e:
            print(f"Error creating auth files: {str(e)}")
            return False
    
    def _create_auth_module(self):
        content = f"""import {{ Module }} from '@nestjs/common';
import {{ AuthService }} from './auth.service';
import {{ AuthController }} from './auth.controller';
import {{ UserModule }} from '../user/user.module';
import {{ JwtModule }} from '@nestjs/jwt';
import {{ jwtConstants }} from './constants';

@Module({{
  imports: [
    UserModule,
    JwtModule.register({{
      global: true,
      secret: jwtConstants.secret,
      signOptions: {{ expiresIn: '1hr' }},
    }}),
  ],
  controllers: [AuthController],
  providers: [AuthService],
}})
export class AuthModule {{}}
"""
        self._write_file("auth.module.ts", content)

    def _create_auth_service(self):
        content = f"""import {{ Injectable, UnauthorizedException }} from '@nestjs/common';
import {{ UserService }} from '../user/user.service';
import {{ JwtService }} from '@nestjs/jwt';

@Injectable()
export class AuthService {{
  constructor(
    private usersService: UserService,
    private jwtService: JwtService,
  ) {{}}

  async signIn(
    email: string,
    password: string,
  ): Promise<{{ access_token: string }}> {{
    const user = this.usersService.findOne(email);
    if (user?.password !== password) {{
      throw new UnauthorizedException();
    }}
    const payload = {{ email: user.email, sub: user.userId, rol: user.rol }};
    return {{
      access_token: await this.jwtService.signAsync(payload),
    }};
  }}
}}
"""
        self._write_file("auth.service.ts", content)

    def _create_auth_controller(self):
        content = f"""import {{ Body, Controller, Post, HttpCode, HttpStatus }} from '@nestjs/common';
import {{ AuthService }} from './auth.service';

@Controller('auth')
export class AuthController {{
  constructor(private readonly authService: AuthService) {{}}

  @HttpCode(HttpStatus.OK)
  @Post('login')
  signIn(@Body() body: {{ email: string; password: string }}) {{
    return this.authService.signIn(body.email, body.password);
  }}
}}
"""
        self._write_file(f"auth.controller.ts", content)

    def _create_auth_guard(self):
        content = f"""import {{
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
}} from '@nestjs/common';
import {{ JwtService }} from '@nestjs/jwt';
import {{ jwtConstants }} from './constants';
import {{ Request }} from 'express';

@Injectable()
export class AuthGuard implements CanActivate {{
  constructor(private jwtService: JwtService) {{}}
  async canActivate(context: ExecutionContext): Promise<boolean> {{
    const request = context.switchToHttp().getRequest<Request>();
    const token = this.extractTokenFromHeader(request);
    if (!token) {{
      throw new UnauthorizedException();
    }}
    try {{
      const payload = await this.jwtService.verifyAsync<{{ rol: string }}>(
        token,
        {{
          secret: jwtConstants.secret,
        }},
      );
      if (payload.rol !== 'admin') {{
        throw new UnauthorizedException();
      }}
    }} catch {{
      throw new UnauthorizedException();
    }}
    return true;
  }}

  private extractTokenFromHeader(request: Request): string | undefined {{
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }}
}}
"""
        self._write_file(f"auth.guard.ts", content)

    def _create_constants(self):
        content = f"""export const jwtConstants = {{
  secret: 'jpk123ppsdqwe',
}};
"""
        self._write_file(f"constants.ts", content)

    def _update_app_module_imports(self):
        try:
            with open(self.app_path, "r") as file:
                lines = file.readlines()

            # Definir las importaciones a agregar
            new_imports = [
                "import { AuthModule } from './auth/auth.module';\n",
                "import { AuthController } from './auth/auth.controller';\n",
                "import { AuthService } from './auth/auth.service';\n"
            ]

            # Agregar cada import si aún no existe
            # Se ubica después de la última línea que comienza con "import"
            last_import_index = -1
            for i, line in enumerate(lines):
                if line.strip().startswith("import "):
                    last_import_index = i
            insert_index = last_import_index + 1

            for imp in new_imports:
                if not any(imp.strip() in line.strip() for line in lines):
                    lines.insert(insert_index, imp)
                    insert_index += 1  # Incrementamos el índice para que las siguientes se inserten en orden

            # Función auxiliar para insertar un nuevo elemento en la lista de un módulo
            def insertar_en_lista(busqueda, nuevo_elemento):
                for i, line in enumerate(lines):
                    if busqueda in line:
                        # Encontrar el final de la lista (puede estar en la misma o en otra línea)
                        j = i
                        while j < len(lines) and "]" not in lines[j]:
                            j += 1
                        # Si la línea del cierre tiene sólo "]" o contiene otros elementos,
                        # se inserta antes de la "]"
                        if "]" in lines[j]:
                            # Si ya se ha agregado, se evita duplicados
                            if nuevo_elemento not in "".join(lines[i:j+1]):
                                lines[j] = lines[j].replace("]", f" {nuevo_elemento},]")
                        break

            # Actualizar cada sección según lo solicitado
            insertar_en_lista("imports: [", ", AuthModule")
            insertar_en_lista("controllers: [", ", AuthController")
            insertar_en_lista("providers: [", ", AuthService")

            # Escribir los cambios en el archivo
            with open(self.app_path, "w") as file:
                file.writelines(lines)

            print(f"Módulo actualizado exitosamente en {self.app_path}.")
        
        except Exception as e:
            print(f"Error actualizando {self.app_path}: {str(e)}")


    def _write_file(self, filename: str, content: str):
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Auth file {filename} created successfully at {file_path}.")