from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    nome = StringField('Nome de utilizador', validators=[DataRequired()])
    password = PasswordField('Palavra-passe', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegistoForm(FlaskForm):
    nome = StringField('Nome de utilizador', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Palavra-passe', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Registar')

class TarefaForm(FlaskForm):
    descricao = StringField('Descrição', validators=[DataRequired()])
    localizacao = StringField('Localização (coordenadas: lat,long, opcional)')
    hora = StringField('Hora prevista')
    prioridade = StringField('Prioridade')
    submit = SubmitField('Adicionar tarefa')

class AcaoTarefaForm(FlaskForm):
    """Formulário vazio para validar o token CSRF nas ações sobre tarefas."""
    pass
