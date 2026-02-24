from kivy.app import App
from kivy.uix.label import Label
import Tarefas  # importa seu código existente

class TarefasApp(App):
    def build(self):
        # Exemplo simples: mostrar texto vindo do seu módulo
        return Label(text="App de Tarefas rodando no Android!")

if __name__ == "__main__":
    TarefasApp().run()
