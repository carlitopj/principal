import os
from datetime import datetime

ARQUIVO_TAREFAS = "tarefas.txt"
tarefas = []
tarefa_em_edicao = None

def carregar_tarefas():
    """Carrega tarefas do arquivo para a lista global"""
    global tarefas
    tarefas.clear()
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            for linha in f:
                if " | " in linha:
                    tarefas.append(linha.strip())

def salvar_tarefas():
    """Salva todas as tarefas no arquivo"""
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        for t in tarefas:
            f.write(t + "\n")

def adicionar_tarefa(nome, info, data):
    """Adiciona ou edita uma tarefa"""
    global tarefa_em_edicao
    if not nome or not info or not data:
        return False
    try:
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        return False

    nova = f"{nome} | {info} | {data}"

    if tarefa_em_edicao is not None:
        if tarefa_em_edicao in tarefas:
            tarefas.remove(tarefa_em_edicao)
        tarefa_em_edicao = None

    tarefas.append(nova)
    salvar_tarefas()
    return True

def remover_tarefa(indice):
    """Remove tarefa pelo índice"""
    if 0 <= indice < len(tarefas):
        tarefas.pop(indice)
        salvar_tarefas()
        return True
    return False

def preparar_edicao(indice):
    """Marca tarefa para edição"""
    global tarefa_em_edicao
    if 0 <= indice < len(tarefas):
        tarefa_em_edicao = tarefas[indice]
        return tarefa_em_edicao.split(" | ")
    return None

def obter_status(tarefa):
    """Retorna status da tarefa (atrasada, vence hoje, em dia)"""
    try:
        partes = tarefa.split(" | ")
        data_str = partes[-1]
        data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
        hoje = datetime.now().date()

        if data_obj < hoje:
            return "Atrasada ⚠️"
        elif data_obj == hoje:
            return "Vence Hoje 🔔"
        else:
            return f"Em dia (faltam {(data_obj - hoje).days} dias)"
    except:
        return "-"
