from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
import os
import sys
from pathlib import Path

try:
    import Tarefas
except ImportError:
    print("Erro: Módulo Tarefas não encontrado!")
    sys.exit(1)

class TarefasLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Tenta carregar as tarefas ao iniciar
        try:
            Tarefas.carregar_tarefas()
            self.atualizar_lista()
        except Exception as e:
            print(f"Erro ao carregar tarefas: {e}")
            import traceback
            traceback.print_exc()

    def adicionar_tarefa(self):
        try:
            nome = self.ids.nome.text
            info = self.ids.info.text
            data = self.ids.data.text
            
            # Trim de espaços para evitar entradas vazias
            if nome.strip():
                if Tarefas.adicionar_tarefa(nome, info, data):
                    self.atualizar_lista()
                    self.ids.nome.text = ""
                    self.ids.info.text = ""
                    self.ids.data.text = ""
                    # Salva após adicionar
                    Tarefas.salvar_tarefas()
        except Exception as e:
            print(f"Erro ao adicionar tarefa: {e}")
            import traceback
            traceback.print_exc()

    def remover_tarefa(self):
        try:
            # Evita erro se a lista estiver vazia
            if Tarefas.tarefas:
                if Tarefas.remover_tarefa(len(Tarefas.tarefas) - 1):
                    self.atualizar_lista()
                    # Salva após remover
                    Tarefas.salvar_tarefas()
        except Exception as e:
            print(f"Erro ao remover tarefa: {e}")
            import traceback
            traceback.print_exc()

    def atualizar_lista(self):
        try:
            # Garante que o RecycleView (ids.lista) receba os dados corretamente
            self.ids.lista.data = [
                {"text": f"{t} - {Tarefas.obter_status(t)}"} 
                for t in Tarefas.tarefas
            ]
        except Exception as e:
            print(f"Erro ao atualizar lista: {e}")
            import traceback
            traceback.print_exc()

class TarefasApp(App):
    def build(self):
        # Definindo o caminho de salvamento para Android vs Desktop
        try:
            if platform == 'android':
                # No Android, usar o diretório de dados da aplicação
                caminho = self.user_data_dir
                if not caminho:
                    print("Aviso: user_data_dir retornou None, usando fallback")
                    caminho = str(Path.home() / ".gestor_tarefas")
            else:
                # Desktop: usar diretório atual ou home
                caminho = os.path.join(os.getcwd(), ".gestor_tarefas")
            
            # Criar diretório se não existir
            Path(caminho).mkdir(parents=True, exist_ok=True)
            
            print(f"Os dados serão salvos em: {caminho}")
            print(f"Platform detectada: {platform}")
            
            # Configurar caminho no módulo Tarefas
            if hasattr(Tarefas, 'configurar_caminho'):
                Tarefas.configurar_caminho(caminho)
            
            return TarefasLayout()
        
        except Exception as e:
            print(f"Erro crítico ao iniciar app: {e}")
            import traceback
            traceback.print_exc()
            # Retornar layout vazio em caso de erro
            return BoxLayout()

    def on_pause(self):
        """Salva os dados quando o usuário minimiza o app"""
        try:
            if hasattr(Tarefas, 'salvar_tarefas'):
                Tarefas.salvar_tarefas()
                print("Tarefas salvas (on_pause)")
        except Exception as e:
            print(f"Erro ao salvar tarefas em on_pause: {e}")
        return True

    def on_stop(self):
        """Salva os dados quando o app é fechado"""
        try:
            if hasattr(Tarefas, 'salvar_tarefas'):
                Tarefas.salvar_tarefas()
                print("Tarefas salvas (on_stop)")
        except Exception as e:
            print(f"Erro ao salvar tarefas em on_stop: {e}")

if __name__ == "__main__":
    try:
        TarefasApp().run()
    except Exception as e:
        print(f"Erro crítico na execução: {e}")
        import traceback
        traceback.print_exc()