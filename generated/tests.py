import pytest
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

# Define the models

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    last_polled = db.Column(db.DateTime)
    notes = db.Column(db.Text)

class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    url = db.Column(db.String(200))
    hash = db.Column(db.String(100))
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'), nullable=False)
    repository = db.relationship('Repository', backref=db.backref('releases', lazy=True))

# Define the routes

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/repositories')
def repository_list():
    repositories = Repository.query.all()
    return render_template('repository_list.html', repositories=repositories)

@app.route('/repositories/<int:repository_id>')
def repository_detail(repository_id):
    repository = Repository.query.get(repository_id)
    return render_template('repository_detail.html', repository=repository)

@app.route('/repositories/add', methods=['GET', 'POST'])
def repository_add():
    if request.method == 'POST':
        name = request.form['name']
        date_added = datetime.now()
        url = request.form['url']
        type = request.form['type']
        notes = request.form['notes']
        repository = Repository(name=name, date_added=date_added, url=url, type=type, notes=notes)
        db.session.add(repository)
        db.session.commit()
        return redirect(url_for('repository_list'))
    return render_template('repository_add.html')

@app.route('/repositories/<int:repository_id>/update', methods=['GET', 'POST'])
def repository_update(repository_id):
    repository = Repository.query.get(repository_id)
    if request.method == 'POST':
        repository.name = request.form['name']
        repository.url = request.form['url']
        repository.type = request.form['type']
        repository.notes = request.form['notes']
        db.session.commit()
        return redirect(url_for('repository_detail', repository_id=repository_id))
    return render_template('repository_update.html', repository=repository)

# Define the tests

def test_index():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'

def test_repository_list():
    response = app.test_client().get('/repositories')
    assert response.status_code == 200

def test_repository_detail():
    response = app.test_client().get('/repositories/1')
    assert response.status_code == 200

def test_repository_add():
    response = app.test_client().post('/repositories/add', data={
        'name': 'Test Repository',
        'url': 'https://github.com/test/test-repo',
        'type': 'github',
        'notes': 'This is a test repository'
    })
    assert response.status_code == 302

def test_repository_update():
    response = app.test_client().post('/repositories/1/update', data={
        'name': 'Updated Repository',
        'url': 'https://github.com/test/updated-repo',
        'type': 'github',
        'notes': 'This is an updated repository'
    })
    assert response.status_code == 302

if __name__ == '__main__':
    app.run()