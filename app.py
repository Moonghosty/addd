from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para flash messages

# Middleware para verificar se a sessão está ativa
@app.before_request
def check_session():
    if 'tasks' not in session and request.endpoint not in ['login', 'static']:
        return redirect(url_for('login'))

# Página inicial com a lista de tarefas
@app.route('/')
def index():
    tasks = session.get('tasks', [])
    total_tasks = len(tasks)
    response = make_response(render_template('index.html', tasks=tasks, total_tasks=total_tasks))
    return response

# Página de login (sem login real, apenas para simular a sessão)
@app.route('/login')
def login():
    return render_template('login.html')

# Página para adicionar uma tarefa
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        # Validando se o título e a descrição foram preenchidos
        if not title or not description:
            flash('Título e descrição são obrigatórios!', 'error')
            return redirect(url_for('add_task'))

        # Adicionando tarefa à sessão
        task = {
            'title': title,
            'description': description,
            'due_date': request.form.get('due_date')
        }
        tasks = session.get('tasks', [])
        tasks.append(task)
        session['tasks'] = tasks

        # Atualizando o cookie de número de tarefas
        task_count = len(tasks)
        resp = make_response(render_template('task_added.html', task=task))
        resp.set_cookie('task_count', str(task_count))

        # Flash message de sucesso
        flash('Tarefa adicionada com sucesso!', 'success')
        return resp

    return render_template('add_task.html')

# Página para deslogar (limpa a sessão)
@app.route('/logout')
def logout():
    session.pop('tasks', None)
    flash('Você foi deslogado!', 'info')
    return redirect(url_for('login'))

# Página de erro 404 personalizada
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_message="Página não encontrada"), 404

# Gerenciamento de erro genérico
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_message="Ocorreu um erro no servidor"), 500

if __name__ == '__main__':
    app.run(debug=True)





<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Agenda de Tarefas</title>
</head>
<body>
    <h1>Agenda de Tarefas</h1>
    <p>Total de tarefas: {{ total_tasks }}</p>

    <a href="{{ url_for('add_task') }}">Adicionar Tarefa</a> | <a href="{{ url_for('logout') }}">Deslogar</a>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul>
                {% for category, message in messages %}
                    <li class="{{ category }}">{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}

    <ul>
        {% for task in tasks %}
            <li><strong>{{ task.title }}</strong> - {{ task.description }} - {{ task.due_date }}</li>
        {% else %}
            <li>Nenhuma tarefa cadastrada.</li>
        {% endfor %}
    </ul>
</body>
</html>


<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Adicionar Tarefa</title>
</head>
<body>
    <h1>Adicionar Tarefa</h1>
    <form action="{{ url_for('add_task') }}" method="POST">
        <label for="title">Título:</label>
        <input type="text" id="title" name="title" required><br>
        
        <label for="description">Descrição:</label>
        <textarea id="description" name="description" required></textarea><br>
        
        <label for="due_date">Data de Vencimento:</label>
        <input type="date" id="due_date" name="due_date"><br>
        
        <button type="submit">Adicionar Tarefa</button>
    </form>

    <a href="{{ url_for('index') }}">Voltar para a Agenda</a>
</body>
</html>

