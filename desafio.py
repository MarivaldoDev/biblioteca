from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3


class Primeiro:
    def __init__(self):
        self.tela = Tk()
        self.tela.geometry('700x600')
        self.tela.title('Livraria')
        self.tela.resizable(width=False, height=False)
        self.tela.configure(background='black')
        self.tela.iconbitmap('icone\pilha-de-livros.ico')
        self.imagem = Image.open('img\LIVRARIABanner.png')
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        self.principio()
        self.frame_configurado()
        self.conectar_banco()
        self.ver_livros()
        self.tela.mainloop()

    def principio(self):
        self.label_imagem = Label(self.tela, image=self.imagem_tk).place(x=80, y=10)
        self.id = Label(self.tela, text='ID', background='black', foreground='white', font=30).place(x=40, y=140)
        self.entrada_id = Entry(self.tela, width=10, border=2.5)
        self.entrada_id.place(x=40, y=170)
        self.titulo = Label(self.tela, text='Título', background='black', foreground='white', font=30).place(x=40, y=210)
        self.entrada_titulo = Entry(self.tela, width=40, border=2.5)
        self.entrada_titulo.place(x=40, y=240)
        self.ano = Label(self.tela, text='Ano', background='black', foreground='white', font=30).place(x=150, y=140)
        self.entrada_ano = Entry(self.tela, width=10, border=2.5)
        self.entrada_ano.place(x=150, y=170)
        self.autor = Label(self.tela, text='Autor', background='black', foreground='white', font=30).place(x=350, y=210)
        self.entrada_autor = Entry(self.tela, width=25, border=2.5)
        self.entrada_autor.place(x=350, y=240)
        
        self.bt_adicionar = Button(self.tela,
        text='Adicionar Livro',
        background='green', 
        foreground='white',
        font=('arial', 12, 'bold'),
        border=8,
        command=self.adicionar).place(x=250, y=90)

        self.bt_apagar = Button(self.tela,
        text='Deletar Livro',
        background='red', 
        foreground='white',
        font=('arial', 12, 'bold'),
        border=8,
        command=self.apagar).place(x=410, y=90)

        self.bt_atualizar = Button(self.tela,
        text='Atualizar Livro',
        background='blue', 
        foreground='white',
        font=('arial', 12, 'bold'),
        border=8,
        command=self.atualizar).place(x=550, y=90)

        self.frame = Frame(self.tela, bd=4, bg='black', highlightbackground='#759feb', highlightthickness=3)
        self.frame.place(relx=0.02, y=315, relwidth=0.96, relheight=0.46)

    def frame_configurado(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))
        style.theme_use('clam')

        self.lista_livros = ttk.Treeview(self.frame, height=3, columns=("col1", "col2", "col3", "col4"))
        self.lista_livros.heading("#0", text="")
        self.lista_livros.heading("#1", text="ID")
        self.lista_livros.heading("#2", text="Título")
        self.lista_livros.heading("#3", text="Autor")
        self.lista_livros.heading("#4", text="Ano")
        self.lista_livros.tag_configure("Treeview.Heading")

        self.lista_livros.bind('<Double-1>', self.clique_duplo)

        self.lista_livros.column("#0", width=1)
        self.lista_livros.column("#1", width=40)
        self.lista_livros.column("#2", width=200)
        self.lista_livros.column("#3", width=145)
        self.lista_livros.column("#4", width=115)

        self.lista_livros.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.97)

    def clique_duplo(self, event):
        self.clique = self.lista_livros.focus()
        self.aaa = self.lista_livros.item(self.clique, 'values')
        
        self.entrada_id.delete(0, END)
        self.entrada_titulo.delete(0, END)
        self.entrada_autor.delete(0, END)
        self.entrada_ano.delete(0, END)
        
        self.entrada_id.insert(0, self.aaa[0])
        self.entrada_titulo.insert(0, self.aaa[1])
        self.entrada_autor.insert(0, self.aaa[2])
        self.entrada_ano.insert(0, self.aaa[3])
    
    def limpar_tela(self):
        self.entrada_id.delete(0, END)
        self.entrada_titulo.delete(0, END)
        self.entrada_autor.delete(0, END)
        self.entrada_ano.delete(0, END)

    def conectar_banco(self):
        self.conexao = sqlite3.connect('livraria.db')
        self.cursor = self.conexao.cursor()

    def ver_livros(self):
        self.lista_livros.delete(*self.lista_livros.get_children())
        self.conectar_banco()
        self.cursor.execute('SELECT * FROM livros')
        resultados = self.cursor.fetchall()

        for i in resultados:
            self.lista_livros.insert("", END, values=i)
        self.conexao.close()
    
    def adicionar(self):
        if self.entrada_titulo.get() != '' and self.entrada_autor.get() != '' and self.entrada_ano.get() != '':
            self.conectar_banco()

            comando_inserir = '''
            INSERT INTO livros (titulo, autor, ano_publicacao)
            VALUES (?, ?, ?)
            '''
            self.cursor.execute(comando_inserir, (self.entrada_titulo.get(), self.entrada_autor.get(), self.entrada_ano.get()))
            self.conexao.commit()
            self.conexao.close()
            self.limpar_tela()
            self.ver_livros()
        else:
            messagebox.showerror('Erro', 'Os campos TÍTULO, AUTOR e ANO precisam ser preenchidos!')

    def apagar(self):
        if self.entrada_id.get() != '':
            self.conectar_banco()
            comando_deletar = 'DELETE FROM livros WHERE id = ?'
            self.cursor.execute(comando_deletar, (self.entrada_id.get(),))
            self.conexao.commit()
            self.conexao.close()
            self.limpar_tela()
            self.ver_livros()
        else:
            messagebox.showerror('Erro', 'Precisamos do ID do livro para apagar!')

    def atualizar(self):
        if self.entrada_id.get() and self.entrada_titulo.get() and self.entrada_autor.get() and self.entrada_ano.get() != '':
            self.conectar_banco()
            
            comando_atualizar = '''
            UPDATE livros
            SET titulo = ?, autor = ?, ano_publicacao = ?
            WHERE id = ?
            '''
            self.cursor.execute(comando_atualizar, (self.entrada_titulo.get(), self.entrada_autor.get(), self.entrada_ano.get(), self.entrada_id.get()))
            self.conexao.commit()
            self.conexao.close()
            self.limpar_tela()
            self.ver_livros()
        else:
             messagebox.showerror('Erro', 'Todos os campos precisam estar preenchidos!')


Primeiro()