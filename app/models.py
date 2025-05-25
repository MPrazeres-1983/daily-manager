from . import db


from flask_login import UserMixin


class Utilizador(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tarefas = db.relationship("Tarefa", backref="utilizador", lazy=True)


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(200), nullable=True)  # Nome/morada original
    coordenadas = db.Column(db.String(50), nullable=True)  # Coordenadas lat,lon
    hora = db.Column(db.String(20), nullable=True)
    prioridade = db.Column(db.String(20), nullable=True)
    concluida = db.Column(db.Boolean, default=False)
    utilizador_id = db.Column(
        db.Integer, db.ForeignKey("utilizador.id"), nullable=False
    )
