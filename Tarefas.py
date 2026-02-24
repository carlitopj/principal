import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime, timedelta

ARQUIVO_TAREFAS = "tarefas.txt"
tarefas = []
tarefa_em_edicao = None

def ordenar_e_atualizar_lista():
    global tarefas
    hoje = datetime.now().date()
    
    def extrair_data(item):
        try:
            # Pega o último elemento após o separador |
            data_str = item.split(" | ")[-1]
            return datetime.strptime(data_str, "%d/%m/%Y").date()
        except:
            return datetime.max.date()

    tarefas.sort(key=extrair_data)
    lista.delete(0, tk.END)
    
    for i, t in enumerate(tarefas):
        # Na lista principal, mostramos apenas Nome e Data para não poluir
        partes = t.split(" | ")
        exibicao = f"{partes[0]} - {partes[-1]}"
        lista.insert(tk.END, exibicao)
        
        data_tarefa = extrair_data(t)
        if data_tarefa < hoje:
            lista.itemconfig(i, {'fg': 'red'})
        elif data_tarefa == hoje:
            lista.itemconfig(i, {'fg': '#d97706'})
        else:
            lista.itemconfig(i, {'fg': 'black'})

def mostrar_detalhes(event=None):
    selecionada = lista.curselection()
    if selecionada:
        indice = selecionada[0]
        # Pegamos a string original da nossa lista de dados, não da exibição da Listbox
        # pois a Listbox agora está resumida.
        texto_original = tarefas[indice]
        
        try:
            nome, informacao, data_str = texto_original.split(" | ")
            data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
            hoje = datetime.now().date()
            
            if data_obj < hoje:
                status, cor = "Atrasada ⚠️", "red"
            elif data_obj == hoje:
                status, cor = "Vence Hoje 🔔", "#d97706"
            else:
                status, cor = f"Em dia (Faltam {(data_obj - hoje).days} dias)", "green"

            lbl_detalhe_nome.config(text=f"📌 Tarefa: {nome}")
            lbl_detalhe_cat.config(text=f"📂 Informação: {informacao}")
            lbl_detalhe_data.config(text=f"📅 Data: {data_str}")
            lbl_detalhe_status.config(text=f"Status: {status}", fg=cor)
        except:
            pass

def adicionar_tarefa(event=None):
    global tarefa_em_edicao
    nome = entrada.get()
    cat = entrada_cat.get()
    data = entrada_data.get()
    
    if nome and cat and data:
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Aviso", "Data inválida!")
            return

        nova_tarefa = f"{nome} | {cat} | {data}"

        if tarefa_em_edicao is not None:
            if tarefa_em_edicao in tarefas:
                tarefas.remove(tarefa_em_edicao)
            tarefa_em_edicao = None
            btn_add.config(text="Adicionar", bg="#10b981")

        tarefas.append(nova_tarefa)
        ordenar_e_atualizar_lista()
        
        # Limpar campos
        for e in [entrada, entrada_cat, entrada_data]: e.delete(0, tk.END)
        entrada.focus_set()
        salvar_tarefas()
    else:
        messagebox.showwarning("Aviso", "Preencha Nome, Informação e Data!")

def carregar_tarefas():
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            for linha in f:
                if " | " in linha:
                    tarefas.append(linha.strip())
        ordenar_e_atualizar_lista()

def salvar_tarefas():
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        for t in tarefas: f.write(t + "\n")

def preparar_edicao():
    global tarefa_em_edicao
    sel = lista.curselection()
    if sel:
        tarefa_em_edicao = tarefas[sel[0]]
        partes = tarefa_em_edicao.split(" | ")
        entrada.delete(0, tk.END); entrada.insert(0, partes[0])
        entrada_cat.delete(0, tk.END); entrada_cat.insert(0, partes[1])
        entrada_data.delete(0, tk.END); entrada_data.insert(0, partes[2])
        btn_add.config(text="Salvar Edição", bg="#3b82f6")
    else:
        messagebox.showwarning("Aviso", "Selecione uma tarefa!")

def remover_tarefa():
    sel = lista.curselection()
    if sel:
        tarefas.pop(sel[0])
        ordenar_e_atualizar_lista()
        salvar_tarefas()
    else:
        messagebox.showwarning("Aviso", "Selecione uma tarefa!")

# --- Interface ---
janela = tk.Tk()
janela.title("Gestor de Tarefas Plus")
janela.geometry("400x520")
janela.configure(bg="#f3f4f6")

# Formulário
tk.Label(janela, text="Nome da Tarefa:", bg="#f3f4f6", font=("Arial", 9, "bold")).pack(pady=(10,0))
entrada = tk.Entry(janela, width=45)
entrada.pack()

tk.Label(janela, text="Informação:", bg="#f3f4f6").pack(pady=(5,0))
entrada_cat = tk.Entry(janela, width=45)
entrada_cat.pack()

tk.Label(janela, text="Data (DD/MM/AAAA):", bg="#f3f4f6").pack(pady=(5,0))
entrada_data = tk.Entry(janela, width=45)
entrada_data.pack()

# Botões
frame_botoes = tk.Frame(janela, bg="#f3f4f6")
frame_botoes.pack(pady=15)

btn_add = tk.Button(frame_botoes, text="Adicionar", command=adicionar_tarefa, bg="#10b981", fg="white", width=12)
btn_add.pack(side=tk.LEFT, padx=2)

btn_edit = tk.Button(frame_botoes, text="Editar", command=preparar_edicao, bg="#f59e0b", fg="white", width=8)
btn_edit.pack(side=tk.LEFT, padx=2)

btn_remove = tk.Button(frame_botoes, text="Remover", command=remover_tarefa, width=8)
btn_remove.pack(side=tk.LEFT, padx=2)

# Novo botão Fechar
btn_fechar = tk.Button(frame_botoes, text="Fechar", command=janela.destroy, bg="#ef4444", fg="white", width=8)
btn_fechar.pack(side=tk.LEFT, padx=2)

# Lista
lista = tk.Listbox(janela, font=("Arial", 10), height=8)
lista.pack(fill=tk.BOTH, expand=True, padx=20)
lista.bind("<<ListboxSelect>>", mostrar_detalhes)

# Quadro de Detalhes
detalhes = tk.LabelFrame(janela, text=" Informações Completas ", bg="white", padx=15, pady=15)
detalhes.pack(fill=tk.X, padx=20, pady=20)

lbl_detalhe_nome = tk.Label(detalhes, text="📌 Tarefa: -", bg="white", anchor="w")
lbl_detalhe_nome.pack(fill=tk.X)

lbl_detalhe_cat = tk.Label(detalhes, text="📂 Informação: -", bg="white", anchor="w")
lbl_detalhe_cat.pack(fill=tk.X)

lbl_detalhe_data = tk.Label(detalhes, text="📅 Data: -", bg="white", anchor="w")
lbl_detalhe_data.pack(fill=tk.X)

lbl_detalhe_status = tk.Label(detalhes, text="Status: -", bg="white", anchor="w", font=("Arial", 9, "bold"))
lbl_detalhe_status.pack(fill=tk.X)

carregar_tarefas()
entrada.focus_set()
janela.mainloop()