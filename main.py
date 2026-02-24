from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform  # Importante para detectar Android
import os
import Tarefas

class TarefasLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Tenta carregar as tarefas ao iniciar
        try:
            Tarefas.carregar_tarefas()
            self.atualizar_lista()
        except Exception as e:
            print(f"Erro ao carregar: {e}")

    def adicionar_tarefa(self):
        nome = self.ids.nome.text
        info = self.ids.info.text
        data = self.ids.data.text
        # Trim de espaços para evitar entradas vazias
        if nome.strip() and Tarefas.adicionar_tarefa(nome, info, data):
            self.atualizar_lista()
            self.ids.nome.text = ""
            self.ids.info.text = ""
            self.ids.data.text = ""

    def remover_tarefa(self):
        # Evita erro se a lista estiver vazia
        if Tarefas.tarefas:
            if Tarefas.remover_tarefa(len(Tarefas.tarefas) - 1):
                self.atualizar_lista()

    def atualizar_lista(self):
        # Garante que o RecycleView (ids.lista) receba os dados corretamente
        self.ids.lista.data = [{"text": f"{t} - {Tarefas.obter_status(t)}"} for t in Tarefas.tarefas]

class TarefasApp(App):
    def build(self):
        # Definindo o caminho de salvamento para Android vs Desktop
        if platform == 'android':
            caminho = self.user_data_dir
        else:
            caminho = os.getcwd()
            
        print(f"Os dados serão salvos em: {caminho}")
        # Se o seu Tarefas.py aceitar um caminho, passe aqui:
        # Tarefas.configurar_caminho(caminho) 
        
        return TarefasLayout()

    def on_pause(self):
        # Salva os dados quando o usuário minimiza o app
        # Tarefas.salvar_tarefas()
        return True

    def on_stop(self):
        # Salva os dados quando o app é fechado
        # Tarefas.salvar_tarefas()
        pass

if __name__ == "__main__":
    TarefasApp().run()
