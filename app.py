from flask import Flask
from routes import routes

# En el fragmento de código Python proporcionado, `app = Flask(__name__)` crea una instancia de aplicación Flask
# con el nombre del módulo. Esta es una forma común de crear un objeto de aplicación Flask.
app = Flask(__name__)

# `app.secret_key = 'none'` está estableciendo la clave secreta para la aplicación Flask `app`. La clave secreta
# se utiliza para firmar de forma segura las cookies de sesión y otras funciones relacionadas con la seguridad en Flask. Es
# es importante establecer una clave secreta fuerte y única para mejorar la seguridad de la aplicación. En 
# este caso, la clave secreta es `'none'`, pero en una aplicación real, debería ser una cadena larga y aleatoria para mayor seguridad.
# cadena aleatoria para mejorar la seguridad.
app.secret_key = 'none'

# `app.register_blueprint(routes)` está registrando un blueprint llamado `routes` con la aplicación # Flask
# aplicación `app`.
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
