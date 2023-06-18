from flask import Flask, render_template, request, redirect, url_for
from database import db_session
from models import Repository, Release
from config import Config
from utils import poll_repositories, send_slack_notification

app = Flask(__name__)
app.config.from_object(Config)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    repositories = Repository.query.all()
    return render_template('repository_list.html', repositories=repositories)

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
        db_session.add(repository)
        db_session.commit()
        
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
        
        db_session.commit()
        
        return redirect(url_for('repository_detail', repo_id=repo_id))
    
    return render_template('repository_update.html', repository=repository)

if __name__ == '__main__':
    app.run()