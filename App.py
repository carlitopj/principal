import sqlite3
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import re

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def iniciar_db():
    conn = sqlite3.connect('vendas_acabamento.db')
    cursor = conn.cursor()
    
    # Tabela fornecedores
    cursor.execute('''CREATE TABLE IF NOT EXISTS fornecedores (
                        id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT, produto TEXT, tipo_produto TEXT,
                        medida TEXT, preco TEXT)''')
                        
    # Tabela de clientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT, telefone TEXT, endereco TEXT,
                        bairro TEXT, city TEXT, cep TEXT, cpf TEXT)''')
                        
    # Tabela de vendas (pedidos)
    cursor.execute('''CREATE TABLE IF NOT EXISTS vendas (
                        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER, id_fornecedor INTEGER,
                        produto TEXT, tipo_produto TEXT, medida TEXT, 
                        qtd INTEGER, preco REAL, preco_final REAL, data_venda TEXT,
                        FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
                        FOREIGN KEY(id_fornecedor) REFERENCES fornecedores(id_fornecedor))''')
    
    conn.commit()
    conn.close()

# --- FUNÇÕES DE LÓGICA ---

def limpar_campos_vendas():
    entry_v_id_cli.delete(0, 'end')
    entry_v_id_forn.delete(0, 'end')
    entry_v_prod.delete(0, 'end')
    entry_v_tipo.delete(0, 'end')
    entry_v_medida.delete(0, 'end')
    entry_v_qtd.delete(0, 'end')
    entry_v_preco.delete(0, 'end')
    entry_v_preco_final.delete(0, 'end')

def limpar_campos_clientes():
    entry_c_nome.delete(0, 'end')
    entry_c_cpf.delete(0, 'end')
    entry_c_tel.delete(0, 'end')
    entry_c_cep.delete(0, 'end')
    entry_c_endereco.delete(0, 'end')
    entry_c_bairro.delete(0, 'end')
    entry_c_city.delete(0, 'end')

def limpar_campos_fornecedores():
    entry_f_nome.delete(0, 'end')
    entry_f_prod.delete(0, 'end')
    entry_f_tipo.delete(0, 'end')
    entry_f_medida.delete(0, 'end')
    entry_f_preco.delete(0, 'end')

def buscar_preco_venda(event=None):
    medida = entry_v_medida.get()
    tipo = entry_v_tipo.get()
    produto = entry_v_prod.get()
    id_forn = entry_v_id_forn.get()
    
    if produto and id_forn:
        conn = sqlite3.connect('vendas_acabamento.db')
        cursor = conn.cursor()
        query = "SELECT preco FROM fornecedores WHERE produto = ? AND id_fornecedor = ?"
        params = [produto, id_forn]
        if tipo:
            query += " AND tipo_produto = ?"
            params.append(tipo)
        if medida:
            query += " AND medida = ?"
            params.append(medida)
        cursor.execute(query, tuple(params))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            entry_v_preco.delete(0, 'end')
            entry_v_preco.insert(0, str(resultado[0]))

def atualizar_visores(event=None):
    termo = entry_busca.get()
    conn = sqlite3.connect('vendas_acabamento.db')
    cursor = conn.cursor()
    
    # Busca clientes e ordena para manter consistência visual
    cursor.execute("SELECT id_cliente, nome FROM clientes WHERE nome LIKE ? ORDER BY id_cliente ASC", (f'%{termo}%',))
    clientes = cursor.fetchall()
    
    # Busca fornecedores e ordena por ID
    cursor.execute('''SELECT id_fornecedor, nome, produto, tipo_produto, medida 
                      FROM fornecedores 
                      WHERE nome LIKE ? OR produto LIKE ? OR tipo_produto LIKE ?
                      ORDER BY id_fornecedor ASC''', 
                   (f'%{termo}%', f'%{termo}%', f'%{termo}%'))
    fornecedores = cursor.fetchall()
    conn.close()
    
    txt_visor.configure(state="normal")
    txt_visor.delete("1.0", "end")
    txt_visor.insert("end", "👤 CLIENTES (ID | NOME)\n" + "-"*60 + "\n")
    for c in clientes: 
        txt_visor.insert("end", f"CLIENTE_ID:{c[0]} | {c[1]}\n")
    
    txt_visor.insert("end", "\n🏭 FORNECEDORES & PRODUTOS (ID | FÁBRICA | PRODUTO | TIPO | MEDIDA)\n" + "-"*60 + "\n")
    for f in fornecedores:
        linha = f"FORNECEDOR_ID:{f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]}\n"
        txt_visor.insert("end", linha)
    txt_visor.configure(state="disabled")

def excluir_selecionado():
    """Exclui permanentemente Clientes ou Fornecedores do BD, preservando a tabela de Pedidos"""
    try:
        # Pega o conteúdo da linha atual onde o cursor está
        linha_completa = txt_visor.get("insert linestart", "insert lineend")
        
        if "CLIENTE_ID:" in linha_completa:
            tipo = "clientes"
            coluna_id = "id_cliente"
            match = re.search(r"CLIENTE_ID:(\d+)", linha_completa)
        elif "FORNECEDOR_ID:" in linha_completa:
            tipo = "fornecedores"
            coluna_id = "id_fornecedor"
            match = re.search(r"FORNECEDOR_ID:(\d+)", linha_completa)
        else:
            messagebox.showwarning("Atenção", "Selecione uma linha de Cliente ou Fornecedor no visor para excluir.")
            return

        if match:
            item_id = match.group(1)
            confirmar = messagebox.askyesno("Confirmar Exclusão", 
                                            f"Deseja excluir permanentemente o ID {item_id} de {tipo}?\n\n"
                                            "Nota: O histórico de pedidos vinculados será mantido nos relatórios.")
            
            if confirmar:
                conn = sqlite3.connect('vendas_acabamento.db')
                cursor = conn.cursor()
                
                # Desativa chaves estrangeiras para permitir excluir o mestre sem apagar os pedidos (histórico)
                cursor.execute("PRAGMA foreign_keys = OFF")
                
                # Exclui o registro da tabela selecionada
                cursor.execute(f"DELETE FROM {tipo} WHERE {coluna_id} = ?", (item_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Sucesso", f"Registro de {tipo} excluído e lista atualizada!")
                atualizar_visores() # Atualiza a caixa de listagem automaticamente
                
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao excluir registro: {e}")

def salvar_cliente():
    n, t = entry_c_nome.get(), entry_c_tel.get()
    if n and t: 
        conn = sqlite3.connect('vendas_acabamento.db'); c = conn.cursor()
        c.execute('''INSERT INTO clientes (nome, telefone, cpf, cep, endereco, bairro, city) 
                     VALUES (?,?,?,?,?,?,?)''', 
                  (n, t, entry_c_cpf.get(), entry_c_cep.get(), entry_c_endereco.get(), entry_c_bairro.get(), entry_c_city.get()))
        conn.commit(); conn.close()
        messagebox.showinfo("Sucesso", "Cliente cadastrado!")
        limpar_campos_clientes()
        atualizar_visores()
    else: messagebox.showwarning("Erro", "Nome e Telefone obrigatórios!")

def salvar_fornecedor():
    n, p = entry_f_nome.get(), entry_f_prod.get()
    if n and p:
        try:
            conn = sqlite3.connect('vendas_acabamento.db'); c = conn.cursor()
            c.execute("INSERT INTO fornecedores (nome, produto, tipo_produto, medida, preco) VALUES (?,?,?,?,?)", 
                      (n, p, entry_f_tipo.get(), entry_f_medida.get(), entry_f_preco.get().replace(',', '.')))
            conn.commit(); conn.close()
            messagebox.showinfo("Sucesso", "Cadastro realizado!")
            limpar_campos_fornecedores()
            atualizar_visores()
        except Exception as e: messagebox.showerror("Erro", str(e))
    else: messagebox.showwarning("Erro", "Fábrica e Produto são obrigatórios!")

def salvar_pedido():
    idc, idf = entry_v_id_cli.get(), entry_v_id_forn.get()
    p, q, pr = entry_v_prod.get(), entry_v_qtd.get(), entry_v_preco.get().replace(',', '.')
    pf = entry_v_preco_final.get().replace(',', '.')
    if idc and idf and p and q:
        try:
            conn = sqlite3.connect('vendas_acabamento.db'); c = conn.cursor()
            c.execute('''INSERT INTO vendas (id_cliente, id_fornecedor, produto, tipo_produto, medida, qtd, preco, preco_final, data_venda) 
                         VALUES (?,?,?,?,?,?,?,?,?)''',
                       (int(idc), int(idf), p, entry_v_tipo.get(), entry_v_medida.get(), int(q), float(pr), float(pf) if pf else 0, entry_v_data.get()))
            conn.commit(); conn.close()
            messagebox.showinfo("Sucesso", "Pedido salvo!")
            limpar_campos_vendas()
            atualizar_visores()
        except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")
    else: messagebox.showwarning("Erro", "Preencha os campos obrigatórios!")

def gerar_excel():
    conn = sqlite3.connect('vendas_acabamento.db')
    df_clientes = pd.read_sql_query("SELECT * FROM clientes", conn)
    df_fornecedores = pd.read_sql_query("SELECT * FROM fornecedores", conn)
    
    query_vendas = '''SELECT v.data_venda as Data, 
                             COALESCE(c.nome, 'CLIENTE EXCLUÍDO (ID:' || v.id_cliente || ')') as Cliente, 
                             COALESCE(f.nome, 'FORNECEDOR EXCLUÍDO (ID:' || v.id_fornecedor || ')') as Fornecedor, 
                             v.produto as Produto, v.tipo_produto as Tipo, v.medida as Medida, v.qtd as Qtd, 
                             v.preco as [Preco Custo], v.preco_final as [Preco Venda], 
                             (v.qtd*v.preco_final) as Total
                      FROM vendas v 
                      LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
                      LEFT JOIN fornecedores f ON v.id_fornecedor = f.id_fornecedor'''
    df_vendas = pd.read_sql_query(query_vendas, conn)
    conn.close()
    try:
        with pd.ExcelWriter("relatorio_completo.xlsx") as writer:
            df_vendas.to_excel(writer, sheet_name='Pedidos', index=False)
            df_clientes.to_excel(writer, sheet_name='Clientes', index=False)
            df_fornecedores.to_excel(writer, sheet_name='Fornecedores', index=False)
        messagebox.showinfo("Excel", "Arquivo 'relatorio_completo.xlsx' gerado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível gerar o Excel: {e}")

# --- INTERFACE ---
iniciar_db(); ctk.set_appearance_mode("dark")
app = ctk.CTk(); app.title("Sistema de Vendas v4.4"); app.geometry("800x650")

top_container = ctk.CTkFrame(app, fg_color="transparent")
top_container.pack(fill="x", padx=10, pady=(5, 0))
ctk.CTkLabel(top_container, text="COMAC", font=("Arial", 24, "bold"), text_color="#1E90FF").pack(side="left", padx=20, pady=10)

tabs = ctk.CTkTabview(app)
tabs.pack(padx=10, pady=(0, 10), fill="both", expand=True)
t_vendas, t_cli, t_forn = tabs.add("Fazer Pedido"), tabs.add("Clientes"), tabs.add("Fornecedores")

# ABA VENDAS (PEDIDO)
frame_v = ctk.CTkFrame(t_vendas, fg_color="transparent"); frame_v.pack(fill="both", expand=True)
col_esq = ctk.CTkFrame(frame_v, width=380); col_esq.pack(side="left", padx=5, pady=5, fill="y")

ctk.CTkLabel(col_esq, text="NOVO PEDIDO", font=("Arial", 14, "bold"), text_color="#32CD32").grid(row=0, column=0, columnspan=2, pady=5)

def criar_campo(parent, row, label_text, placeholder="", is_data=False):
    lbl = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12))
    lbl.grid(row=row, column=0, padx=(15, 5), pady=3, sticky="w")
    entry = ctk.CTkEntry(parent, placeholder_text=placeholder, height=28, width=200)
    entry.grid(row=row, column=1, padx=(5, 15), pady=3, sticky="ew")
    if is_data:
        entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
    return entry

entry_v_data = criar_campo(col_esq, 1, "Data:", is_data=True)
entry_v_id_cli = criar_campo(col_esq, 2, "ID Cliente:", "Cód. Cliente")
entry_v_id_forn = criar_campo(col_esq, 3, "ID Fornecedor:", "Cód. Fábrica")
entry_v_id_forn.bind("<KeyRelease>", buscar_preco_venda)
entry_v_prod = criar_campo(col_esq, 4, "Produto:", "Nome do produto")
entry_v_prod.bind("<KeyRelease>", buscar_preco_venda)
entry_v_tipo = criar_campo(col_esq, 5, "Tipo:", "Ex: Brilhoso, Fosco")
entry_v_tipo.bind("<KeyRelease>", buscar_preco_venda)
entry_v_medida = criar_campo(col_esq, 6, "Medida:", "Ex: 60x60")
entry_v_medida.bind("<KeyRelease>", buscar_preco_venda)
entry_v_qtd = criar_campo(col_esq, 7, "Quantidade:", "Qtd itens")
entry_v_preco = criar_campo(col_esq, 8, "Vl. Unit (Custo):", "R$ Automático")
entry_v_preco_final = criar_campo(col_esq, 9, "Vl. Unit (Venda):", "R$ Venda")

btn_frame = ctk.CTkFrame(col_esq, fg_color="transparent")
btn_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky="nsew")
ctk.CTkButton(btn_frame, text="Salvar Pedido", command=salvar_pedido, fg_color="#2E8B57", width=140).pack(side="left", padx=10)
ctk.CTkButton(btn_frame, text="Exportar Excel", command=gerar_excel, fg_color="#4682B4", width=140).pack(side="right", padx=10)

# VISOR (LADO DIREITO) - COM BOTÃO EXCLUIR
col_dir = ctk.CTkFrame(frame_v); col_dir.pack(side="right", padx=5, pady=5, fill="both", expand=True)

search_frame = ctk.CTkFrame(col_dir, fg_color="transparent")
search_frame.pack(fill="x", padx=5, pady=5)
entry_busca = ctk.CTkEntry(search_frame, placeholder_text="🔍 Buscar..."); entry_busca.pack(side="left", fill="x", expand=True, padx=(0,5))
entry_busca.bind("<KeyRelease>", atualizar_visores)

btn_excluir = ctk.CTkButton(search_frame, text="Excluir", command=excluir_selecionado, fg_color="#B22222", width=80)
btn_excluir.pack(side="right")

txt_visor = ctk.CTkTextbox(col_dir, font=("Courier New", 10), wrap="none"); txt_visor.pack(pady=5, padx=5, fill="both", expand=True)

# --- ABA CLIENTES ---
frame_cli_inputs = ctk.CTkFrame(t_cli, fg_color="transparent")
frame_cli_inputs.pack(pady=10)

def layout_campo(parent, row, label_text, placeholder):
    lbl = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12))
    lbl.grid(row=row, column=0, padx=10, pady=2, sticky="e")
    ent = ctk.CTkEntry(parent, placeholder_text=placeholder, width=300)
    ent.grid(row=row, column=1, padx=10, pady=2, sticky="w")
    return ent

entry_c_nome = layout_campo(frame_cli_inputs, 0, "Nome:", "Nome Completo")
entry_c_cpf = layout_campo(frame_cli_inputs, 1, "CPF:", "000.000.000-00")
entry_c_tel = layout_campo(frame_cli_inputs, 2, "Tel:", "(00) 00000-0000")
entry_c_cep = layout_campo(frame_cli_inputs, 3, "CEP:", "00000-000")
entry_c_endereco = layout_campo(frame_cli_inputs, 4, "End:", "Rua, Número")
entry_c_bairro = layout_campo(frame_cli_inputs, 5, "Bairro:", "Nome do Bairro")
entry_c_city = layout_campo(frame_cli_inputs, 6, "Cidade:", "Cidade - UF")

ctk.CTkButton(t_cli, text="Salvar Cliente", command=salvar_cliente).pack(pady=10)

# --- ABA FORNECEDORES ---
frame_forn_inputs = ctk.CTkFrame(t_forn, fg_color="transparent")
frame_forn_inputs.pack(pady=10)

entry_f_nome = layout_campo(frame_forn_inputs, 0, "Fábrica:", "Nome da Fábrica")
entry_f_prod = layout_campo(frame_forn_inputs, 1, "Produto:", "Nome do Produto")
entry_f_tipo = layout_campo(frame_forn_inputs, 2, "Tipo:", "Ex: Brilhoso, Fosco")
entry_f_medida = layout_campo(frame_forn_inputs, 3, "Medida:", "Ex: 60x60")
entry_f_preco = layout_campo(frame_forn_inputs, 4, "Preço:", "Valor de Custo")

ctk.CTkButton(t_forn, text="Salvar Cadastro", command=salvar_fornecedor, fg_color="#6A5ACD").pack(pady=10)

atualizar_visores(); app.mainloop()