from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.lang import Builder
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
