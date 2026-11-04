"""Task routes must enforce HTTP methods, ownership and CSRF."""
import os
import pytest
from werkzeug.security import generate_password_hash

os.environ.setdefault("SECRET_KEY", "ci-test-only-key-not-a-production-secret-2026")

from app import criar_app, db
from app.models import Utilizador, Tarefa


@pytest.fixture
def client():
    app = criar_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
                      WTF_CSRF_ENABLED=False)
    with app.app_context():
        db.create_all()
        a = Utilizador(nome="owner", password=generate_password_hash("pwd"))
        b = Utilizador(nome="other", password=generate_password_hash("pwd"))
        db.session.add_all([a, b])
        db.session.commit()
        task = Tarefa(descricao="task", utilizador_id=a.id)
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        yield app.test_client(), app, task_id
        db.session.remove()
        db.drop_all()


def test_mutating_get_is_not_allowed(client):
    http, app, task_id = client
    assert http.get(f"/apagar/{task_id}").status_code == 405
    assert http.get(f"/concluir/{task_id}").status_code == 405


def test_cross_user_deletion_is_blocked(client):
    http, app, task_id = client
    http.post("/login", data={"nome": "other", "password": "pwd"})
    response = http.post(f"/apagar/{task_id}")
    assert response.status_code == 302
    with app.app_context():
        assert db.session.get(Tarefa, task_id) is not None


def test_missing_csrf_is_rejected(client):
    http, app, task_id = client
    http.post("/login", data={"nome": "owner", "password": "pwd"})
    app.config["WTF_CSRF_ENABLED"] = True
    response = http.post(f"/apagar/{task_id}")
    assert response.status_code == 400
    with app.app_context():
        assert db.session.get(Tarefa, task_id) is not None
