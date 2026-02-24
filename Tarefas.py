import os
import sys
from datetime import datetime
from pathlib import Path

# --- LÓGICA DE CAMINHO SEGURO ---
ARQUIVO_TAREFAS = None
tarefas = []
tarefa_em_edicao = None

def obter_caminho_arquivo():
    """Obtém o caminho seguro para salvar tarefas"""
    global ARQUIVO_TAREFAS
    
    # Se já foi configurado, usar esse
    if ARQUIVO_TAREFAS is not None:
        return ARQUIVO_TAREFAS
    
    nome_arquivo = "tarefas.txt"
    
    try:
        # Tentar usar Kivy App (só funciona em runtime)
        from kivy.app import App
        from kivy.utils import platform
        
        app = App.get_running_app()
        
        if app and platform == 'android':
            diretorio = app.user_data_dir
            if diretorio:
                caminho = os.path.join(diretorio, nome_arquivo)
                print(f"Usando diretório Android: {diretorio}")
                return caminho
    except Exception as e:
        print(f"Aviso ao tentar usar App.user_data_dir: {e}")
    
    # Fallback: usar diretório home ou atual
    try:
        diretorio = str(Path.home())
    except:
        diretorio = os.getcwd()
    
    caminho = os.path.join(diretorio, ".gestor_tarefas", nome_arquivo)
    print(f"Usando diretório fallback: {diretorio}")
    return caminho

def configurar_caminho(novo_caminho):
    """Permite configurar o caminho de salvamento manualmente"""
    global ARQUIVO_TAREFAS
    
    if novo_caminho:
        # Criar diretório se não existir
        diretorio = os.path.dirname(novo_caminho)
        Path(diretorio).mkdir(parents=True, exist_ok=True)
        
        ARQUIVO_TAREFAS = novo_caminho
        print(f"Caminho de tarefas configurado: {ARQUIVO_TAREFAS}")
        return True
    
    return False

def _garantir_caminho():
    """Garante que o caminho está configurado e o diretório existe"""
    global ARQUIVO_TAREFAS
    
    if ARQUIVO_TAREFAS is None:
        ARQUIVO_TAREFAS = obter_caminho_arquivo()
    
    # Criar diretório se não existir
    diretorio = os.path.dirname(ARQUIVO_TAREFAS)
    if diretorio:
        Path(diretorio).mkdir(parents=True, exist_ok=True)

def carregar_tarefas():
    """Carrega tarefas do arquivo para a lista global"""
    global tarefas
    
    try:
        _garantir_caminho()
        
        tarefas.clear()
        
        if os.path.exists(ARQUIVO_TAREFAS):
            try:
                with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
                    for linha in f:
                        linha = linha.strip()
                        if linha and " | " in linha:
                            tarefas.append(linha)
                print(f"✅ {len(tarefas)} tarefa(s) carregada(s)")
            except IOError as e:
                print(f"❌ Erro ao ler arquivo: {e}")
        else:
            print(f"📝 Arquivo não existe ainda: {ARQUIVO_TAREFAS}")
    
    except Exception as e:
        print(f"❌ Erro crítico ao carregar tarefas: {e}")
        import traceback
        traceback.print_exc()

def salvar_tarefas():
    """Salva todas as tarefas no arquivo"""
    try:
        _garantir_caminho()
        
        # Criar diretório se não existir
        diretorio = os.path.dirname(ARQUIVO_TAREFAS)
        if diretorio:
            Path(diretorio).mkdir(parents=True, exist_ok=True)
        
        with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
            for t in tarefas:
                f.write(t + "\n")
        
        print(f"✅ {len(tarefas)} tarefa(s) salva(s) em {ARQUIVO_TAREFAS}")
    
    except IOError as e:
        print(f"❌ Erro ao salvar arquivo: {e}")
    except Exception as e:
        print(f"❌ Erro crítico ao salvar tarefas: {e}")
        import traceback
        traceback.print_exc()

def adicionar_tarefa(nome, info, data):
    """Adiciona ou edita uma tarefa"""
    global tarefa_em_edicao
    
    try:
        # Validação básica
        if not nome or not info or not data:
            print("❌ Nome, info e data são obrigatórios")
            return False
        
        # Validar formato de data
        try:
            datetime.strptime(data.strip(), "%d/%m/%Y")
        except ValueError:
            print(f"❌ Data inválida: {data}. Use o formato DD/MM/YYYY")
            return False
        
        nova = f"{nome.strip()} | {info.strip()} | {data.strip()}"
        
        # Se há tarefa em edição, remover a antiga
        if tarefa_em_edicao is not None:
            if tarefa_em_edicao in tarefas:
                tarefas.remove(tarefa_em_edicao)
            tarefa_em_edicao = None
        
        tarefas.append(nova)
        salvar_tarefas()
        print(f"✅ Tarefa adicionada: {nova}")
        return True
    
    except Exception as e:
        print(f"❌ Erro ao adicionar tarefa: {e}")
        import traceback
        traceback.print_exc()
        return False

def remover_tarefa(indice):
    """Remove tarefa pelo índice"""
    try:
        if 0 <= indice < len(tarefas):
            tarefa = tarefas.pop(indice)
            salvar_tarefas()
            print(f"✅ Tarefa removida: {tarefa}")
            return True
        else:
            print(f"❌ Índice inválido: {indice}")
            return False
    except Exception as e:
        print(f"❌ Erro ao remover tarefa: {e}")
        import traceback
        traceback.print_exc()
        return False

def preparar_edicao(indice):
    """Marca tarefa para edição e retorna seus dados"""
    global tarefa_em_edicao
    
    try:
        if 0 <= indice < len(tarefas):
            tarefa_em_edicao = tarefas[indice]
            partes = tarefa_em_edicao.split(" | ")
            print(f"✅ Tarefa marcada para edição: {tarefa_em_edicao}")
            return partes if len(partes) == 3 else None
        else:
            print(f"❌ Índice inválido: {indice}")
            return None
    except Exception as e:
        print(f"❌ Erro ao preparar edição: {e}")
        import traceback
        traceback.print_exc()
        return None

def obter_status(tarefa):
    """Retorna status formatado da tarefa"""
    try:
        partes = tarefa.split(" | ")
        
        if len(partes) < 3:
            return "-"
        
        data_str = partes[2].strip()
        data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
        hoje = datetime.now().date()
        
        if data_obj < hoje:
            return "Atrasada ⚠️"
        elif data_obj == hoje:
            return "Vence Hoje 🔔"
        else:
            dias = (data_obj - hoje).days
            if dias == 1:
                return "Vence Amanhã ⏰"
            return f"Em dia ({dias} dias)"
    
    except Exception as e:
        print(f"Aviso ao obter status: {e}")
        return "-"

# Função auxiliar para debug
def listar_tarefas():
    """Lista todas as tarefas (útil para debug)"""
    if not tarefas:
        print("📋 Nenhuma tarefa cadastrada")
        return
    
    print("\n📋 === TAREFAS ===")
    for i, t in enumerate(tarefas):
        print(f"{i+1}. {t} [{obter_status(t)}]")
    print("================\n")