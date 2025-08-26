# -*- coding: utf-8 -*-
# Código Python para um sistema de gerenciamento de pessoas
# Usando o framework Flask para o backend e HTML para o frontend.
# O HTML e JavaScript estão incorporados como uma string multilinha.

from flask import Flask, render_template_string, request, redirect, url_for
import json
import os # Importa a biblioteca 'os' para acessar variáveis de ambiente

app = Flask(__name__)

# Base de dados em memória.
# Usamos um dicionário onde a chave é o ID e o valor é um dicionário com os detalhes da pessoa.
people_db = {
    1: {"nome": "Maria Silva", "sexo": "Feminino", "idade": 35, "condicao": "Desempregada",
        "observacao": "Precisa de ajuda com alimentação."},
    2: {"nome": "João Santos", "sexo": "Masculino", "idade": 50, "condicao": "Em situação de rua",
        "observacao": "Necessita de roupas e abrigo."},
    3: {"nome": "Ana Souza", "sexo": "Feminino", "idade": 22, "condicao": "Família de baixa renda",
        "observacao": "Procura emprego e apoio para os filhos."}
}
# Contador para gerar novos IDs
next_id = 4


# --- Rotas do Backend ---

@app.route('/')
def index():
    """
    Rota principal para exibir a página inicial e a lista de pessoas.
    Renderiza a string HTML com os dados da base de dados.
    """
    return render_template_string(HTML_TEMPLATE, people_json=json.dumps(people_db))


@app.route('/add', methods=['POST'])
def add_person():
    """
    Adiciona uma nova pessoa à base de dados.
    O ID é gerado automaticamente.
    """
    global next_id
    nome = request.form.get('nome')
    sexo = request.form.get('sexo')
    idade = int(request.form.get('idade', 0))
    condicao = request.form.get('condicao')
    observacao = request.form.get('observacao')

    if nome and idade > 0:
        people_db[next_id] = {
            "nome": nome,
            "sexo": sexo,
            "idade": idade,
            "condicao": condicao,
            "observacao": observacao
        }
        next_id += 1
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update_person():
    """
    Atualiza os dados de uma pessoa existente.
    """
    person_id = int(request.form.get('id'))
    nome = request.form.get('nome')
    sexo = request.form.get('sexo')
    idade = int(request.form.get('idade', 0))
    condicao = request.form.get('condicao')
    observacao = request.form.get('observacao')

    if person_id in people_db:
        people_db[person_id]["nome"] = nome
        people_db[person_id]["sexo"] = sexo
        people_db[person_id]["idade"] = idade
        people_db[person_id]["condicao"] = condicao
        people_db[person_id]["observacao"] = observacao
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_person():
    """
    Deleta uma pessoa da base de dados.
    """
    person_id = int(request.form.get('id'))
    if person_id in people_db:
        del people_db[person_id]
    return redirect(url_for('index'))


# --- String HTML para o Frontend ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Filantrópico</title>
    <!-- Inclui Tailwind CSS para estilização rápida -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }
    </style>
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-6xl mx-auto bg-white p-8 rounded-2xl shadow-lg">
        <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">Sistema de Gerenciamento Filantrópico</h1>

        <!-- Tabela de Pessoas -->
        <div class="mb-8">
            <h2 class="text-xl font-semibold mb-4 text-gray-700">Pessoas Cadastradas</h2>
            <div class="overflow-x-auto rounded-lg shadow-md">
                <table class="min-w-full bg-white border border-gray-200 rounded-lg">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nº</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sexo</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Idade</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Condição</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Observação</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                        </tr>
                    </thead>
                    <tbody id="people-table-body" class="bg-white divide-y divide-gray-200">
                        <!-- Itens do estoque serão injetados aqui via JavaScript -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Formulários de Gerenciamento -->
        <div class="grid lg:grid-cols-2 gap-8">
            <!-- Formulário para Adicionar Pessoa -->
            <div class="bg-gray-50 p-6 rounded-2xl shadow-inner">
                <h2 class="text-xl font-semibold mb-4 text-gray-700">Adicionar Nova Pessoa</h2>
                <form action="/add" method="post" class="space-y-4">
                    <div>
                        <label for="nome_add" class="block text-sm font-medium text-gray-700">Nome</label>
                        <input type="text" id="nome_add" name="nome" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                    </div>
                    <div>
                        <label for="sexo_add" class="block text-sm font-medium text-gray-700">Sexo</label>
                        <input type="text" id="sexo_add" name="sexo" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                    </div>
                    <div>
                        <label for="idade_add" class="block text-sm font-medium text-gray-700">Idade</label>
                        <input type="number" id="idade_add" name="idade" required min="0" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                    </div>
                    <div>
                        <label for="condicao_add" class="block text-sm font-medium text-gray-700">Condição</label>
                        <input type="text" id="condicao_add" name="condicao" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                    </div>
                    <div>
                        <label for="observacao_add" class="block text-sm font-medium text-gray-700">Observação</label>
                        <textarea id="observacao_add" name="observacao" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2"></textarea>
                    </div>
                    <button type="submit" class="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-xl shadow transition duration-300">Adicionar Pessoa</button>
                </form>
            </div>

            <!-- Formulário para Atualizar Pessoa -->
            <div class="bg-gray-50 p-6 rounded-2xl shadow-inner">
                <h2 class="text-xl font-semibold mb-4 text-gray-700">Atualizar Dados da Pessoa</h2>
                <form action="/update" method="post" class="space-y-4">
                    <div>
                        <label for="id_update" class="block text-sm font-medium text-gray-700">Nº da Pessoa</label>
                        <input type="number" id="id_update" name="id" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                    </div>
                    <div>
                        <label for="nome_update" class="block text-sm font-medium text-gray-700">Nome</label>
                        <input type="text" id="nome_update" name="nome" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                    </div>
                    <div>
                        <label for="sexo_update" class="block text-sm font-medium text-gray-700">Sexo</label>
                        <input type="text" id="sexo_update" name="sexo" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                    </div>
                    <div>
                        <label for="idade_update" class="block text-sm font-medium text-gray-700">Idade</label>
                        <input type="number" id="idade_update" name="idade" required min="0" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                    </div>
                    <div>
                        <label for="condicao_update" class="block text-sm font-medium text-gray-700">Condição</label>
                        <input type="text" id="condicao_update" name="condicao" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                    </div>
                    <div>
                        <label for="observacao_update" class="block text-sm font-medium text-gray-700">Observação</label>
                        <textarea id="observacao_update" name="observacao" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2"></textarea>
                    </div>
                    <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-xl shadow transition duration-300">Atualizar Pessoa</button>
                </form>
            </div>

        </div>

        <!-- Formulário para Deletar Pessoa -->
        <div class="bg-gray-50 p-6 rounded-2xl shadow-inner mt-8">
            <h2 class="text-xl font-semibold mb-4 text-gray-700">Deletar Pessoa</h2>
            <form action="/delete" method="post" class="space-y-4">
                <div>
                    <label for="id_delete" class="block text-sm font-medium text-gray-700">Nº da Pessoa</label>
                    <input type="number" id="id_delete" name="id" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2">
                </div>
                <button type="submit" class="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-xl shadow transition duration-300">Deletar Pessoa</button>
            </form>
        </div>
    </div>

    <script>
        // O Flask injeta o JSON da base de dados aqui
        const peopleData = JSON.parse('{{ people_json | safe }}');

        const tableBody = document.getElementById('people-table-body');

        // Função para renderizar a tabela
        function renderTable() {
            tableBody.innerHTML = ''; // Limpa a tabela
            for (const id in peopleData) {
                const person = peopleData[id];
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${person.nome}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${person.sexo}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${person.idade}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${person.condicao}</td>
                    <td class="px-6 py-4 text-sm text-gray-500 max-w-xs overflow-hidden text-ellipsis whitespace-nowrap">${person.observacao}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <button onclick="prefillUpdateForm(${id})" class="text-indigo-600 hover:text-indigo-900 font-bold mr-2">Atualizar</button>
                        <button onclick="prefillDeleteForm(${id})" class="text-red-600 hover:text-red-900 font-bold">Deletar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            }
        }

        // Função para preencher o formulário de atualização
        function prefillUpdateForm(id) {
            const person = peopleData[id];
            if (person) {
                document.getElementById('id_update').value = id;
                document.getElementById('nome_update').value = person.nome;
                document.getElementById('sexo_update').value = person.sexo;
                document.getElementById('idade_update').value = person.idade;
                document.getElementById('condicao_update').value = person.condicao;
                document.getElementById('observacao_update').value = person.observacao;
                document.getElementById('id_update').focus();
            }
        }

        // Função para preencher o formulário de deleção
        function prefillDeleteForm(id) {
            document.getElementById('id_delete').value = id;
            document.getElementById('id_delete').focus();
        }

        // Renderiza a tabela inicial
        renderTable();
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    # Obtém a porta do ambiente Heroku, ou usa 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
