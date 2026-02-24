import os
from datetime import datetime
from kivy.utils import platform

# --- LÓGICA DE CAMINHO SEGURO ---
def obter_caminho_arquivo():
    nome_arquivo = "tarefas.txt"
    if platform == 'android':
        from android.storage import app_storage_path # Opcional, mas usaremos App.user_data_dir
        # No Kivy, o jeito mais seguro é pegar o diretório de dados do App
        from kivy.app import App
        diretorio = App.get_running_app().user_data_dir
        return os.path.join(diretorio, nome_arquivo)
    return nome_arquivo # No PC, salva na pasta do script

ARQUIVO_TAREFAS = None # Será definido na primeira chamada
tarefas = []
tarefa_em_edicao = None

def carregar_tarefas():
    """Carrega tarefas do arquivo para a lista global"""
    global tarefas, ARQUIVO_TAREFAS
    if ARQUIVO_TAREFAS is None:
        ARQUIVO_TAREFAS = obter_caminho_arquivo()
        
    tarefas.clear()
    if os.path.exists(ARQUIVO_TAREFAS):
        try:
            with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
                for linha in f:
                    if " | " in linha:
                        tarefas.append(linha.strip())
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")

def salvar_tarefas():
    """Salva todas as tarefas no arquivo"""
    global ARQUIVO_TAREFAS
    if ARQUIVO_TAREFAS is None:
        ARQUIVO_TAREFAS = obter_caminho_arquivo()
        
    try:
        with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
            for t in tarefas:
                f.write(t + "\n")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")

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
            # Encontra o índice para manter a posição se preferir, 
            # ou apenas remove como você fez:
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
    """Retorna status da tarefa"""
    try:
        partes = tarefa.split(" | ")
        data_str = partes[-1]
        data_obj = datetime.strptime(data_str.strip(), "%d/%m/%Y").date()
        hoje = datetime.now().date()

        if data_obj < hoje:
            return "Atrasada ⚠️"
        elif data_obj == hoje:
            return "Vence Hoje 🔔"
        else:
            dias = (data_obj - hoje).days
            return f"Em dia ({dias} dias)"
    except:
        return "-"
