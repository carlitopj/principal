from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
import os
import sys

try:
    import Tarefas
except ImportError:
    print("Erro: Módulo Tarefas não encontrado!")
    sys.exit(1)

class TarefasLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10
        
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
                else:
                    print("Erro ao adicionar tarefa")
            else:
                print("Nome da tarefa não pode estar vazio")
        except Exception as e:
            print(f"Erro ao adicionar tarefa: {e}")
            import traceback
            traceback.print_exc()

    def remover_tarefa(self):
        try:
            if Tarefas.tarefas:
                Tarefas.remover_tarefa(len(Tarefas.tarefas) - 1)
                self.atualizar_lista()
                Tarefas.salvar_tarefas()
            else:
                print("Nenhuma tarefa para remover")
        except Exception as e:
            print(f"Erro ao remover tarefa: {e}")
            import traceback
            traceback.print_exc()

    def atualizar_lista(self):
        try:
            lista_container = self.ids.get("lista_container", None)
            if lista_container is None:
                print("Erro: lista_container não encontrado")
                return
            
            lista_container.clear_widgets()
            
            for i, tarefa in enumerate(Tarefas.tarefas):
                status = Tarefas.obter_status(tarefa)
                
                # Criar label com a tarefa
                label_text = f"{i+1}. {tarefa}\n Status: {status}"
                label = Label(text=label_text, size_hint_y=None, height=60, markup=True)
                lista_container.add_widget(label)
                
                # Criar botão para remover
                btn_remover = Button(text="Remover", size_hint_y=None, height=40, size_hint_x=0.3)
                btn_remover.bind(on_press=lambda x, idx=i: self.remover_tarefa_indice(idx))
                lista_container.add_widget(btn_remover)
            
            if not Tarefas.tarefas:
                lista_container.add_widget(Label(text="Nenhuma tarefa cadastrada", size_hint_y=None, height=40))
        
        except Exception as e:
            print(f"Erro ao atualizar lista: {e}")
            import traceback
            traceback.print_exc()

    def remover_tarefa_indice(self, indice):
        try:
            if Tarefas.remover_tarefa(indice):
                self.atualizar_lista()
                Tarefas.salvar_tarefas()
        except Exception as e:
            print(f"Erro ao remover tarefa: {e}")


class TarefasApp(App):
    def build(self):
        # Carregar arquivo KV se existir, caso contrário, criar interface dinamicamente
        try:
            if os.path.exists('gestor_tarefas.kv'):
                Builder.load_file('gestor_tarefas.kv')
        except Exception as e:
            print(f"Aviso: Não foi possível carregar gestor_tarefas.kv: {e}")
        
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        # Input fields
        input_layout = GridLayout(cols=1, size_hint_y=0.4, spacing=5)
        
        self.nome_input = TextInput(hint_text="Nome da Tarefa", multiline=False, size_hint_y=None, height=40)
        input_layout.add_widget(self.nome_input)
        
        self.info_input = TextInput(hint_text="Informação", multiline=False, size_hint_y=None, height=40)
        input_layout.add_widget(self.info_input)
        
        self.data_input = TextInput(hint_text="Data (DD/MM/YYYY)", multiline=False, size_hint_y=None, height=40)
        input_layout.add_widget(self.data_input)
        
        layout.add_widget(input_layout)
        
        # Buttons
        btn_layout = GridLayout(cols=2, size_hint_y=0.15, spacing=5)
        
        btn_adicionar = Button(text="Adicionar")
        btn_adicionar.bind(on_press=self.adicionar_tarefa)
        btn_layout.add_widget(btn_adicionar)
        
        btn_remover = Button(text="Remover Última")
        btn_remover.bind(on_press=self.remover_tarefa)
        btn_layout.add_widget(btn_remover)
        
        layout.add_widget(btn_layout)
        
        # Lista de tarefas
        scroll = ScrollView(size_hint=(1, 0.45))
        self.lista_container = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.lista_container.bind(minimum_height=self.lista_container.setter('height'))
        scroll.add_widget(self.lista_container)
        layout.add_widget(scroll)
        
        # Carregar tarefas
        try:
            Tarefas.carregar_tarefas()
            self.atualizar_lista()
        except Exception as e:
            print(f"Erro ao carregar tarefas: {e}")
        
        return layout

    def adicionar_tarefa(self, instance):
        try:
            nome = self.nome_input.text
            info = self.info_input.text
            data = self.data_input.text
            
            if nome.strip():
                if Tarefas.adicionar_tarefa(nome, info, data):
                    self.atualizar_lista()
                    self.nome_input.text = ""
                    self.info_input.text = ""
                    self.data_input.text = ""
                    Tarefas.salvar_tarefas()
        except Exception as e:
            print(f"Erro ao adicionar tarefa: {e}")

    def remover_tarefa(self, instance):
        try:
            if Tarefas.tarefas:
                Tarefas.remover_tarefa(len(Tarefas.tarefas) - 1)
                self.atualizar_lista()
        except Exception as e:
            print(f"Erro ao remover tarefa: {e}")

    def atualizar_lista(self):
        try:
            self.lista_container.clear_widgets()
            
            for i, tarefa in enumerate(Tarefas.tarefas):
                status = Tarefas.obter_status(tarefa)
                label_text = f"{i+1}. {tarefa}\nStatus: {status}"
                label = Label(text=label_text, size_hint_y=None, height=70, markup=True)
                self.lista_container.add_widget(label)
            
            if not Tarefas.tarefas:
                self.lista_container.add_widget(Label(text="Nenhuma tarefa cadastrada", size_hint_y=None, height=40))
        except Exception as e:
            print(f"Erro ao atualizar lista: {e}")


if __name__ == '__main__':
    TarefasApp().run()