# Daily Manager

## Gestor diário de tarefas com mapa e relatórios em PDF

Projeto criado por [Mário Prazeres](https://github.com/MPrazeres-1983).

---

## Descrição

O **Daily Manager** é uma aplicação web simples, desenvolvida em Flask e totalmente em português, pensada para quem trabalha na rua ou precisa de associar tarefas a localizações reais (morada ou coordenadas GPS). Permite organizar, localizar, visualizar e exportar tarefas do dia a dia.

---

## Funcionalidades

- Registo e login de utilizadores
- Adicionar tarefas com:

  - Descrição
  - Localização (nome de rua, morada, ponto de interesse, ou coordenadas GPS)
  - Hora
  - Prioridade

- Listagem, edição, remoção e marcação de tarefas como concluídas
- Visualização das tarefas num mapa interativo (Folium/OpenStreetMap)
- Exportação do relatório diário para PDF (apresenta o endereço legível)
- Associação automática de cada tarefa a coordenadas geográficas (para uso no mapa)
- Sistema preparado para evoluir (ex: etiquetas, anexos, filtros)

---

## Potencialidades

- **Ideal para profissionais de rua, técnicos, freelancers, estudantes, pequenas equipas, logística, etc.**
- **Organização diária fácil:** Consulta rápida de todas as tarefas e respetivos locais no mapa.
- **Registo limpo:** Morada e coordenadas armazenadas separadamente para máxima flexibilidade.
- **Relatórios profissionais:** Exporta as tuas tarefas em PDF, prontos para arquivo ou envio.
- **Fácil de adaptar:** Perfeito para aprender Flask, programar webapps em português, ou adaptar à tua realidade.

---

## Instalação

1. **Clonar o repositório:**

   ```bash
   git clone https://github.com/MPrazeres-1983/daily_manager.git
   cd daily_manager
   ```

2. **Criar ambiente virtual:**

   ```bash
   python -m venv venv
   # Ativar no Windows:
   venv\Scripts\activate
   # Ou no Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Criar a base de dados (primeira vez):**

   ```python
   # No terminal Python
   from app import criar_app, db
   app = criar_app()
   with app.app_context():
       db.create_all()
   exit()
   ```

5. **Iniciar a app:**

   ```bash
   flask run
   ```

   Depois acede a [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Estrutura dos dados da tarefa

- **Descrição:** Texto livre
- **Endereço:** Nome da rua/morada inserida (legível)
- **Coordenadas:** Latitude e longitude (automático para o mapa)
- **Hora:** Texto livre (ex: "14:00", "manhã", etc.)
- **Prioridade:** Ex: baixa, média, alta

---

## Notas

- O ficheiro `tarefas.db` (base de dados) está dentro da pasta `instance/` e está incluído no `.gitignore`.
- Podes apagar a base de dados a qualquer altura para começar de novo (atenção: perdes os dados).
- Todos os campos estão prontos para futura evolução do projeto.

---

## Créditos

Desenvolvido por [Mário Prazeres](https://github.com/MPrazeres-1983).
Sente-te à vontade para dar sugestões ou contribuir!

---


## Segurança

Antes de iniciar a aplicação, configura a variável de ambiente `SECRET_KEY` com pelo menos 32 caracteres aleatórios. A chave antiga fixa foi removida; em ambientes que a utilizaram, considera inválidas as sessões anteriores. Ações que alteram tarefas usam POST e proteção CSRF. Os pedidos de geocodificação têm timeout. Não disponibilizar a aplicação publicamente sem rever as condições de utilização do Nominatim, limites de pedidos, privacidade e backups.
