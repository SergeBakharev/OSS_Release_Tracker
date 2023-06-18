from flask import Flask, render_template, request, redirect, url_for
from models import Repository
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate = Migrate(app, db)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/')
def index():
    repositories = Repository.query.all()
    return render_template('index.html', repositories=repositories)

@app.route('/repository/<int:repo_id>')
def repository_detail(repo_id):
    repository = Repository.query.get(repo_id)
    return render_template('repository_detail.html', repository=repository)

@app.route('/repository/add', methods=['GET', 'POST'])
def repository_add():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        type = request.form['type']
        notes = request.form['notes']
        
        repository = Repository(name=name, url=url, type=type, notes=notes)
        db.session.add(repository)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('repository_add.html')

@app.route('/repository/update/<int:repo_id>', methods=['GET', 'POST'])
def repository_update(repo_id):
    repository = Repository.query.get(repo_id)
    
    if request.method == 'POST':
        repository.name = request.form['name']
        repository.url = request.form['url']
        repository.type = request.form['type']
        repository.notes = request.form['notes']
        
        db.session.commit()
        
        return redirect(url_for('repository_detail', repo_id=repo_id))
    
    return render_template('repository_update.html', repository=repository)

if __name__ == '__main__':
    app.run(host='0.0.0.0')