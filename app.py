from flask import Flask, render_template, url_for, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import jsonify

# import os
# import openai
# from dotenv import load_dotenv
# import requests

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")



app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Configuración de usuarios simulada
usuarios = {
    "estudiante": {
        "password": generate_password_hash("12345"),
        "rol": "estudiante"
    },
    "profesor": {
        "password": generate_password_hash("1234"),
        "rol": "profesor"
    }
}


# NEWS_API_KEY = 'wasaa'


# Decorador para verificar si el usuario ha iniciado sesión
def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        selected_role = request.form.get('tipo')

        # Verifica si el usuario existe y la contraseña es correcta
        if username in usuarios and check_password_hash(usuarios[username]["password"], password):
            user_role = usuarios[username]["rol"]

            # Verifica que el rol seleccionado coincida con el rol del usuario
            if selected_role == user_role:
                session['username'] = username
                session['rol'] = user_role
                print(f"Usuario '{username}' ha iniciado sesión como {session['rol']}.")

                # Redirige según el rol
                return redirect(url_for('home_estudiante' if user_role == 'estudiante' else 'home_profesor'))
            else:
                flash("Rol seleccionado no coincide con el rol del usuario.")
        else:
            flash("Credenciales incorrectas")

    return render_template('login.html')


# Ruta principal - Página de novedades
@app.route('/')
@require_login
def index():
    # Solicita las noticias de la API
    # url = f'https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={NEWS_API_KEY}'
    # response = requests.get(url)

    # # Si la solicitud es exitosa, carga las noticias, si no, usa una lista vacía
    # news_data = response.json().get('articles', []) if response.status_code == 200 else []

    return render_template('index.html')


# @app.route('/chatbot', methods=['POST'])
# @require_login
# def chatbot():
#     user_message = request.json.get("message")
#
#     if not user_message:
#         return jsonify({"response": "No he recibido ningún mensaje. ¿Podrías intentarlo de nuevo?"}), 400
#
#     try:
#         # Llamada a la API de OpenAI
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "Eres un asistente de ayuda para estudiantes universitarios."},
#                 {"role": "user", "content": user_message}
#             ]
#         )
#
#         bot_response = response['choices'][0]['message']['content'].strip()
#
#     except openai.error.RateLimitError:
#         bot_response = "Se ha superado el límite de uso de la API. Por favor, intenta de nuevo más tarde o revisa tu plan de API."
#     except openai.error.InvalidRequestError as e:
#         bot_response = f"Hubo un problema con la solicitud: {str(e)}"
#     except openai.error.OpenAIError as e:
#         bot_response = "Hubo un problema al obtener la respuesta. Por favor, intenta de nuevo."
#         print(f"Error al llamar a la API de OpenAI: {e}")
#
#     return jsonify({"response": bot_response})


# Ruta de inicio para estudiantes
@app.route('/home_estudiante')
@require_login
def home_estudiante():
    print("Acceso autorizado a la página principal del estudiante.")
    return render_template('index.html')


# Ruta de inicio para profesores
@app.route('/home_profesor')
@require_login
def home_profesor():
    return render_template('home_profesor.html')

@app.route('/perfil_profesor')
@require_login
def perfil_profesor():
    return render_template('perfil_profesor.html')


# Otras rutas protegidas por `@require_login`
@app.route('/mis_clases')
@require_login
def mis_clases():
    return render_template('mis_clases.html')

@app.route('/herramientas')
@require_login
def herramientas():
    return render_template('herramientas.html')

@app.route('/horarios')
@require_login
def horarios():
    return render_template('MAPA.html')

@app.route('/reclamos1')
@require_login
def reclamos1():
    return render_template('Reclamo1.html')

@app.route('/Reportes')
@require_login
def reportes():
    return render_template('Proyectos.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Aquí puedes agregar lógica para verificar si el correo existe en la base de datos.
        if email == "test@example.com":  # Simula una verificación de usuario.
            flash('Se ha enviado un correo para restablecer su contraseña.', 'success')
        else:
            flash('El correo electrónico no está registrado.', 'error')
        return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')


@app.route('/clases')
@require_login
def clases():
    return render_template('clases.html')

@app.route('/reclamo')
@require_login
def reclamo():
    return render_template('Reclamo.html')

@app.route('/biblioteca')
@require_login
def biblioteca():
    books = [
        {'title': "Fundamentos de Programación", 'author': "Luis Joyanes",
         'description': "Una introducción a los fundamentos de la programación.", 'img': "static/images/libro1.jpg",
         'available': True},
        {'title': "Sistemas Operativos Modernos", 'author': "Andrew Tanenbaum",
         'description': "Un libro completo sobre sistemas operativos.", 'img': "static/images/libro2.jpg",
         'available': True},
        {'title': "Estructuras de Datos", 'author': "Mark Allen Weiss",
         'description': "Exploración profunda de estructuras de datos.", 'img': "static/images/libro3.jpg",
         'available': True},
        {'title': "Inteligencia Artificial", 'author': "Stuart Russell",
         'description': "Teoría y aplicaciones de la inteligencia artificial.",
         'img': "static/images/libro4.jpg", 'available': True},
        {'title': "Redes de Computadoras", 'author': "James Kurose",
         'description': "Principios y prácticas modernas en redes.", 'img': "static/images/libro5.jpg",
         'available': True},
        {'title': "Algoritmos: Diseño y Análisis", 'author': "Thomas H. Cormen",
         'description': "Un enfoque en el diseño y análisis de algoritmos.",
         'img': "static/images/libro6.jpg", 'available': True},
        {'title': "Bases de Datos", 'author': "Elmasri & Navathe",
         'description': "Fundamentos del diseño de bases de datos relacionales.",
         'img': "static/images/libro7.jpg", 'available': True},
        {'title': "Cálculo con Geometría Analítica", 'author': "Louis Leithold",
         'description': "Un clásico en el estudio del cálculo diferencial e integral.",
         'img': "static/images/libro8.jpg", 'available': False},
        {'title': "Aprendizaje Automático", 'author': "Tom Mitchell",
         'description': "Fundamentos del aprendizaje automático y sus aplicaciones.",
         'img': "static/images/libro9.jpg", 'available': False},
        {'title': "Programación en C", 'author': "Dennis Ritchie",
         'description': "Conceptos básicos y avanzados del lenguaje C.", 'img': "static/images/libro10.jpg",
         'available': False},
        {'title': "Diseño de Compiladores", 'author': "Alfred V. Aho",
         'description': "Una guía para el diseño y desarrollo de compiladores.",
         'img': "static/images/libro11.jpg", 'available': True},
        {'title': "Desarrollo Web con HTML y CSS", 'author': "Jon Duckett",
         'description': "Introducción al diseño y desarrollo web moderno.",
         'img': "static/images/libro12.jpg", 'available': True},
        {'title': "Java: Cómo Programar", 'author': "Deitel & Deitel",
         'description': "Un libro completo para aprender Java.", 'img': "static/images/libro13.jpg",
         'available': True},
        {'title': "Python para Todos", 'author': "Charles Severance",
         'description': "Aprender Python desde cero con ejemplos prácticos.",
         'img': "static/images/libro14.jpg", 'available': True},
        {'title': "Seguridad Informática", 'author': "William Stallings",
         'description': "Conceptos clave en criptografía y seguridad.", 'img': "static/images/libro15.jpg",
         'available': False},
        {'title': "Computación Cuántica", 'author': "Michael A. Nielsen",
         'description': "Introducción a la computación cuántica y sus aplicaciones.",
         'img': "static/images/libro16.jpg", 'available': False},
        {'title': "Big Data y Machine Learning", 'author': "Davy Cielen",
         'description': "Exploración de técnicas avanzadas de análisis de datos.",
         'img': "static/images/libro17.jpg", 'available': False},
        {'title': "Ingeniería de Software", 'author': "Ian Sommerville",
         'description': "Principios y prácticas de la ingeniería de software.",
         'img': "static/images/libro18.jpg", 'available': False},
        {'title': "Fundamentos de Redes Neuronales", 'author': "Simon Haykin",
         'description': "Estudio profundo de redes neuronales y su funcionamiento.",
         'img': "static/images/libro19.jpg", 'available': True},
        {'title': "Blockchain y Criptomonedas", 'author': "Andreas Antonopoulos",
         'description': "Una guía práctica sobre blockchain y bitcoin.", 'img': "static/images/libro20.jpg",
         'available': False}
    ]

    return render_template('biblioteca.html', books=books)


@app.route('/tareas')
@require_login
def tareas():
    return render_template('tareas.html')

@app.route('/reservas')
@require_login
def reservas():
    return render_template('reservas.html')

@app.route('/Reserva_auditorio')
@require_login
def Reserva_auditorio():
    return render_template('Reserva_Auditorio.html')

@app.route('/Reserva_canchita')
@require_login
def Reserva_canchita():
    return render_template('Reserva_canchita.html')

@app.route('/Reserva_salones')
@require_login
def Reserva_salones():
    return render_template('Reserva_salones.html')


@app.route('/drive')
@require_login
def drive():
    return render_template('drive.html')


@app.route('/perfil')
@require_login
def perfil():
    return render_template('perfil.html')


# Ruta de cierre de sesión
@app.route('/logout')
@require_login
def logout():
    session.pop('username', None)
    session.pop('rol', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)








