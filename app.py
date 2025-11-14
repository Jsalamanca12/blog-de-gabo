# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXT = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-change-this')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# === INDEX ===
@app.route('/')
def index():
    return render_template('index.html')


# === SOBRE EL EQUIPO ===
@app.route('/sobre')
def sobre():
    members = [
        {'name': 'X1', 'role': 'Coordinación y redacción', 'photo': 'foto_X1.jpg', 'bio': 'Estudiante...'},
        {'name': 'X2', 'role': 'Investigación y contenidos', 'photo': 'foto_X2.jpg', 'bio': 'Estudiante...'},
        {'name': 'X3', 'role': 'Edición multimedia', 'photo': 'foto_X3.jpg', 'bio': 'Estudiante...'},
        {'name': 'X4', 'role': 'Diseño y publicación web', 'photo': 'foto_X4.jpg', 'bio': 'Estudiante...'},
    ]
    return render_template('about.html', members=members)


# === CORTES (SECCIONES PRINCIPALES) ===
@app.route('/corte/<int:n>')
def corte(n):
    cortes = {
        1: {
            'id': 1,
            'title': 'Sobre Gabo',
            'summary': 'Una mirada íntima a la vida y esencia de Gabriel García Márquez.',
            'file': None
        },
        2: {
            'id': 2,
            'title': 'Obra',
            'summary': 'Exploramos sus obras más destacadas, su evolución literaria y su impacto cultural.',
            'file': None
        },
        3: {
            'id': 3,
            'title': 'Cronología',
            'summary': 'Un recorrido a través de los hitos más importantes en la vida de Gabo.',
            'file': None
        },
        4: {
            'id': 4,
            'title': 'Legado',
            'summary': 'El impacto duradero de su obra en la literatura, el cine y la cultura universal.',
            'file': None
        }
    }

    corte = cortes.get(n)
    if not corte:
        return render_template('404.html'), 404

    # enviamos corte y n al template
    return render_template('corte.html', corte=corte, n=n)


# === MULTIMEDIA ===
@app.route('/multimedia')
def multimedia():
    uploads = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        uploads = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('multimedia.html', uploads=uploads)


# === ARCHIVOS SUBIDOS ===
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# === CONTACTO ===
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        mensaje = request.form.get('mensaje')
        with open('messages.txt', 'a', encoding='utf-8') as f:
            f.write(f"{nombre} | {correo} | {mensaje}\n")
        flash('Mensaje enviado. ¡Gracias!', 'success')
        return redirect(url_for('contacto'))
    return render_template('contacto.html')


# === SUBIR ARCHIVOS ===
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.referrer or url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.referrer or url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Archivo subido correctamente', 'success')
        return redirect(request.referrer or url_for('multimedia'))

    flash('Tipo de archivo no permitido', 'danger')
    return redirect(request.referrer or url_for('index'))

# === SITEMAP ===
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

# === ROBOTS ===
@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
