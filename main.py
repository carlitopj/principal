from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import Tarefas

class TarefasLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Tarefas.carregar_tarefas()
        self.atualizar_lista()

    def adicionar_tarefa(self):
        nome = self.ids.nome.text
        info = self.ids.info.text
        data = self.ids.data.text
        if Tarefas.adicionar_tarefa(nome, info, data):
            self.atualizar_lista()
            self.ids.nome.text = ""
            self.ids.info.text = ""
            self.ids.data.text = ""

    def remover_tarefa(self):
        if Tarefas.remover_tarefa(len(Tarefas.tarefas) - 1):
            self.atualizar_lista()

    def atualizar_lista(self):
        self.ids.lista.data = [{"text": f"{t} - {Tarefas.obter_status(t)}"} for t in Tarefas.tarefas]

class TarefasApp(App):
    def build(self):
        return TarefasLayout()

if __name__ == "__main__":
    TarefasApp().run()
