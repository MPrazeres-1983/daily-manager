from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_file,
)
from flask_login import login_user, logout_user, login_required, current_user
from .models import Utilizador, Tarefa
from .formularios import LoginForm, RegistoForm, TarefaForm
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import folium
from fpdf import FPDF
import io
import requests

main = Blueprint("main", __name__)


def obter_coordenadas(endereco):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": endereco, "format": "json"}
    resposta = requests.get(
        url, params=params, headers={"User-Agent": "DailyManagerApp"}
    )
    if resposta.status_code == 200 and resposta.json():
        dados = resposta.json()[0]
        return f"{dados['lat']},{dados['lon']}"
    return ""


def is_coordenadas(s):
    if not s:
        return False
    partes = s.split(",")
    if len(partes) == 2:
        try:
            float(partes[0].strip())
            float(partes[1].strip())
            return True
        except ValueError:
            return False
    return False


@login_manager.user_loader
def load_user(user_id):
    return Utilizador.query.get(int(user_id))


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/registo", methods=["GET", "POST"])
def registo():
    form = RegistoForm()
    if form.validate_on_submit():
        if Utilizador.query.filter_by(nome=form.nome.data).first():
            flash("Utilizador já existe.")
            return redirect(url_for("main.registo"))
        utilizador = Utilizador(
            nome=form.nome.data, password=generate_password_hash(form.password.data)
        )
        db.session.add(utilizador)
        db.session.commit()
        flash("Registo feito! Pode entrar.")
        return redirect(url_for("main.login"))
    return render_template("registo.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        utilizador = Utilizador.query.filter_by(nome=form.nome.data).first()
        if utilizador and check_password_hash(utilizador.password, form.password.data):
            login_user(utilizador)
            return redirect(url_for("main.painel"))
        flash("Dados inválidos.")
    return render_template("login.html", form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/painel", methods=["GET", "POST"])
@login_required
def painel():
    form = TarefaForm()
    if form.validate_on_submit():
        endereco = form.localizacao.data.strip()
        if endereco and not is_coordenadas(endereco):
            try:
                coords = obter_coordenadas(endereco)
                print("DEBUG: Coordenadas obtidas =", coords)
            except Exception as e:
                print(f"Erro ao obter coordenadas: {e}")
                coords = ""
        else:
            coords = endereco if is_coordenadas(endereco) else ""
        tarefa = Tarefa(
            descricao=form.descricao.data,
            endereco=endereco,
            coordenadas=coords,
            hora=form.hora.data,
            prioridade=form.prioridade.data,
            utilizador_id=current_user.id,
        )
        db.session.add(tarefa)
        db.session.commit()
        flash("Tarefa adicionada!")
        return redirect(url_for("main.painel"))

    tarefas = Tarefa.query.filter_by(utilizador_id=current_user.id).all()
    return render_template("painel.html", form=form, tarefas=tarefas)


@main.route("/concluir/<int:tarefa_id>")
@login_required
def concluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    if tarefa.utilizador_id != current_user.id:
        flash("Acesso negado.")
        return redirect(url_for("main.painel"))
    tarefa.concluida = True
    db.session.commit()
    return redirect(url_for("main.painel"))


@main.route("/apagar/<int:tarefa_id>")
@login_required
def apagar_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    if tarefa.utilizador_id != current_user.id:
        flash("Acesso negado.")
        return redirect(url_for("main.painel"))
    db.session.delete(tarefa)
    db.session.commit()
    flash("Tarefa apagada!")
    return redirect(url_for("main.painel"))


@main.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
@login_required
def editar_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    if tarefa.utilizador_id != current_user.id:
        flash("Acesso negado.")
        return redirect(url_for("main.painel"))
    form = TarefaForm(obj=tarefa)
    if form.validate_on_submit():
        endereco = form.localizacao.data.strip()
        if endereco and not is_coordenadas(endereco):
            try:
                coords = obter_coordenadas(endereco)
                print("DEBUG: Coordenadas obtidas (editar) =", coords)
            except Exception as e:
                print(f"Erro ao obter coordenadas (editar): {e}")
                coords = ""
        else:
            coords = endereco if is_coordenadas(endereco) else ""
        tarefa.descricao = form.descricao.data
        tarefa.endereco = endereco
        tarefa.coordenadas = coords
        tarefa.hora = form.hora.data
        tarefa.prioridade = form.prioridade.data
        db.session.commit()
        flash("Tarefa atualizada!")
        return redirect(url_for("main.painel"))
    return render_template("editar_tarefa.html", form=form)


@main.route("/mapa")
@login_required
def mapa():
    tarefas = Tarefa.query.filter_by(utilizador_id=current_user.id).all()
    m = folium.Map(location=[38.7223, -9.1393], zoom_start=12)  # Lisboa por defeito
    for t in tarefas:
        print("DEBUG tarefa coordenadas:", repr(t.coordenadas))
        if t.coordenadas and is_coordenadas(t.coordenadas):
            try:
                latlon = [float(coord.strip()) for coord in t.coordenadas.split(",")]
                print("DEBUG marcador:", latlon)
                folium.Marker(location=latlon, popup=t.descricao).add_to(m)
            except Exception as e:
                print(f"Erro no marcador: {e}")
                continue
    map_html = m._repr_html_()
    return render_template("mapa.html", map_html=map_html)


@main.route("/relatorio")
@login_required
def relatorio():
    tarefas = Tarefa.query.filter_by(utilizador_id=current_user.id).all()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório Diário de Tarefas", ln=1, align="C")
    pdf.ln(10)
    for t in tarefas:
        estado = "Concluída" if t.concluida else "Pendente"
        pdf.cell(
            0,
            10,
            f"{t.descricao} | {t.endereco} | {t.hora} | {t.prioridade} | {estado}",
            ln=1,
        )
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    pdf_output = io.BytesIO(pdf_bytes)
    return send_file(
        pdf_output, download_name="relatorio_tarefas.pdf", as_attachment=True
    )
