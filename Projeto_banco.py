import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

def obter_conexao():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=bancoaula.database.windows.net;'
        'DATABASE=bancoaula;'
        'UID=sabd;'
        'PWD=@mZfaeiou1;'
    )

def criar_entry_estilizado(janela, label_text):
    frame = ttk.Frame(janela)
    frame.pack(pady=5)

    label = ttk.Label(frame, text=label_text, style="TLabel")
    label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    entry = ttk.Entry(frame, style="TEntry")
    entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    return entry

def cadastrar_usuario():
    janela_cadastro = tk.Toplevel(janela_principal)
    janela_cadastro.title("Cadastrar Cliente")

    entry_nome = criar_entry_estilizado(janela_cadastro, "Nome:")
    entry_cpf = criar_entry_estilizado(janela_cadastro, "Cpf:")
    entry_telefone = criar_entry_estilizado(janela_cadastro, "Telefone:")

    botao_confirmar = ttk.Button(janela_cadastro, text="Confirmar", style="TButton", command=lambda: confirmar_cadastro(janela_cadastro, entry_nome.get(), entry_cpf.get(), entry_telefone.get()))
    botao_confirmar.pack(pady=10)

def confirmar_cadastro(janela, nome, cpf, telefone):
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        query = "INSERT INTO cliente (nm_cliente, cpf, telefone) VALUES (?, ?, ?)"
        parametros = (nome, cpf, telefone)

        cursor.execute(query, parametros)

        conexao.commit()
        conexao.close()

        messagebox.showinfo("Cadastro", "Cadastro Confirmado")
        
        janela.destroy()

    except Exception as e:
        messagebox.showerror("Erro no Cadastro", f"Erro ao cadastrar usuário:\n{str(e)}")

def excluir_usuario():
    janela_exclusao = tk.Toplevel(janela_principal)
    janela_exclusao.title("Excluir Cliente")

    entry_id_excluir = criar_entry_estilizado(janela_exclusao, "ID a ser excluído:")

    botao_confirmar = ttk.Button(janela_exclusao, text="Confirmar", style="TButton", command=lambda: confirmar_exclusao(janela_exclusao, entry_id_excluir.get()))
    botao_confirmar.pack(pady=10)

def confirmar_exclusao(janela, id_cliente):
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        query = "DELETE FROM cliente WHERE idcliente = ?"
        parametros = (id_cliente,)

        cursor.execute(query, parametros)

        conexao.commit()
        conexao.close()

        messagebox.showinfo("Exclusão Confirmada", f"Usuário com ID {id_cliente} excluído.")

        janela.destroy()

    except Exception as e:
        messagebox.showerror("Erro na Exclusão", f"Erro ao excluir usuário:\n{str(e)}")

def alterar_usuario():
    janela_alteracao = tk.Toplevel(janela_principal)
    janela_alteracao.title("Alterar Cliente")

    entry_id_alterar = criar_entry_estilizado(janela_alteracao, "ID do cliente a ser alterado:")
    entry_novo_nome = criar_entry_estilizado(janela_alteracao, "Novo Nome:")
    entry_novo_telefone = criar_entry_estilizado(janela_alteracao, "Novo Telefone:")

    botao_confirmar = ttk.Button(janela_alteracao, text="Confirmar", style="TButton", command=lambda: confirmar_alteracao(janela_alteracao, entry_id_alterar.get(), entry_novo_nome.get(), entry_novo_telefone.get()))
    botao_confirmar.pack(pady=10)

def confirmar_alteracao(janela, id_cliente, novo_nome, novo_telefone):
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        query = "UPDATE cliente SET nm_cliente = ?, telefone = ? WHERE idcliente = ?"
        parametros = (novo_nome, novo_telefone, id_cliente)

        cursor.execute(query, parametros)

        conexao.commit()
        conexao.close()

        messagebox.showinfo("Alteração", "Alteração Confirmada")

        janela.destroy()

    except Exception as e:
        messagebox.showerror("Erro na Alteração", f"Erro ao alterar usuário:\n{str(e)}")

def visualizar_usuarios():
    janela_visualizacao = tk.Toplevel(janela_principal)
    janela_visualizacao.title("Visualizar Clientes")

    vsb = ttk.Scrollbar(janela_visualizacao, orient="vertical")
    
    tree = ttk.Treeview(janela_visualizacao, yscrollcommand=vsb.set)
    tree["columns"] = ("ID", "Nome", "Cpf", "Telefone")

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("ID", anchor=tk.CENTER, width=50)
    tree.column("Nome", anchor=tk.CENTER, width=150)
    tree.column("Cpf", anchor=tk.CENTER, width=100)
    tree.column("Telefone", anchor=tk.CENTER, width=100)

    tree.heading("#0", text="", anchor=tk.CENTER)
    tree.heading("ID", text="ID", anchor=tk.CENTER)
    tree.heading("Nome", text="Nome", anchor=tk.CENTER)
    tree.heading("Cpf", text="Cpf", anchor=tk.CENTER)
    tree.heading("Telefone", text="Telefone", anchor=tk.CENTER)

    query = "SELECT idcliente, nm_cliente, cpf, telefone FROM cliente"
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(query)
    usuarios = cursor.fetchall()
    conexao.close()

    for usuario in usuarios:
        # Certifique-se de que o nome seja tratado como uma única coluna
        nome_completo = usuario[1]  # Índice 1 corresponde à coluna "nm_cliente"
        tree.insert("", tk.END, values=(usuario[0], nome_completo, usuario[2], usuario[3]))

    vsb.config(command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.pack(pady=10, fill="both", expand=True)


janela_principal = tk.Tk()
janela_principal.title("Menu Principal")

ttk.Style().configure("TLabel", padding=5, font=('Helvetica', 10, 'bold'))
ttk.Style().configure("TEntry", padding=5, font=('Helvetica', 10))
ttk.Style().configure("TButton", padding=5, font=('Helvetica', 10, 'bold'), background="black", foreground="black")

botao_cadastrar = ttk.Button(janela_principal, text="Cadastrar Cliente", command=cadastrar_usuario)
botao_excluir = ttk.Button(janela_principal, text="Excluir Cliente", command=excluir_usuario)
botao_alterar = ttk.Button(janela_principal, text="Alterar Cliente", command=alterar_usuario)
botao_visualizar = ttk.Button(janela_principal, text="Visualizar Clientes", command=visualizar_usuarios)

botao_cadastrar.pack(pady=10)
botao_excluir.pack(pady=10)
botao_alterar.pack(pady=10)
botao_visualizar.pack(pady=10)

janela_principal.mainloop()
