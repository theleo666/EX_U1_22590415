import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv 

# Cargar las variables de entorno
load_dotenv()

# Crear instancia
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Categoría
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

# Modelo Post
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

# Ruta para ver todos los posts
@app.route('/')
def index():
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template('index.html', posts=posts, categories=categories)

# Eliminar post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('index'))

# Ruta para crear un nuevo post
@app.route('/post/new', methods=['GET','POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form.get('category_id')
        new_post = Post(title=title, content=content, category_id=category_id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))
    
    # Aqui sigue si es GET
    categories = Category.query.all()
    return render_template('create_post.html', categories=categories)

# Ruta para actualizar un post (Nueva ruta agregada)
@app.route('/post/update/<int:id>', methods=['GET', 'POST'])
def update_post(id):
    # Obtenemos el post de la base de datos por su ID
    post = Post.query.get(id)
    
    if request.method == 'POST':
        # Actualizamos los atributos del post con los datos del formulario
        post.title = request.form['title']
        post.content = request.form['content']
        post.category_id = request.form.get('category_id')
        
        # Guardamos los cambios en la base de datos
        db.session.commit()
        return redirect(url_for('index'))
        
    # Si la petición es GET, obtenemos las categorías y mostramos la plantilla
    categories = Category.query.all()
    return render_template('update_post.html', post=post, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)