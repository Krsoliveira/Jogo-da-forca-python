# arquivo: jogo_da_forca_gui.py (versão final com Canvas e design profissional)

import tkinter as tk
from tkinter import messagebox
import random
import unicodedata
import os

# Determina o caminho absoluto para o diretório onde o script está
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Paleta de cores profissional, moderna e coesa
CORES = {
    "FUNDO": "#2d2d2d",          # Cinza muito escuro
    "FUNDO_SECUNDARIO": "#393939",# Cinza escuro
    "TEXTO": "#f5f5f5",          # Branco suave
    "DESTAQUE": "#00a8e8",        # Azul ciano vibrante
    "SUCESSO": "#90ee90",         # Verde claro
    "ERRO": "#ff6b6b",           # Vermelho suave
    "AVISO": "#ffd166"           # Amarelo/Laranja suave
}

# Fontes limpas e modernas
FONTES = {
    "TITULO": ("Calibri", 30, "bold"),
    "PALAVRA": ("Consolas", 48, "bold"),
    "NORMAL": ("Calibri", 14),
    "FEEDBACK": ("Calibri", 14, "italic"),
    "PONTUACAO": ("Calibri", 16, "bold")
}

# Função para carregar todas as palavras (sem alterações)
def carregar_palavras():
    dicionario_final = {}
    try:
        from palavras import PALAVRAS_CURADAS_COM_DICAS
        dicionario_final.update(PALAVRAS_CURADAS_COM_DICAS)
    except ImportError:
        print("Aviso: Arquivo 'palavras.py' não encontrado.")

    dicas_genericas = ("É uma palavra comum da língua portuguesa.", "Pode ser um substantivo, verbo ou adjetivo.")
    caminho_palavras_br = os.path.join(DIRETORIO_ATUAL, 'palavras_br.txt')
    try:
        with open(caminho_palavras_br, 'r', encoding='utf-8') as file:
            for palavra in file:
                palavra_limpa = palavra.strip().lower()
                if len(palavra_limpa) > 3 and palavra_limpa.isalpha() and palavra_limpa not in dicionario_final:
                    palavra_sem_acento = ''.join(c for c in unicodedata.normalize('NFD', palavra_limpa) if unicodedata.category(c) != 'Mn')
                    dicionario_final[palavra_sem_acento] = dicas_genericas
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{caminho_palavras_br}' não encontrado.")
    
    if not dicionario_final:
        print("ERRO CRÍTICO: Nenhuma lista de palavras encontrada. Usando palavras padrão.")
        dicionario_final = {"python": ("Linguagem de programação", "Popular em ciência de dados")}

    return dicionario_final

PALAVRAS_COM_DICAS = carregar_palavras()
CONFIG_DIFICULDADE = {"Fácil": 10, "Médio": 7, "Difícil": 5}

class JogoDaForcaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JOGO DA FORCA")
        self.root.geometry("900x600")
        self.root.configure(bg=CORES["FUNDO"])
        self.root.resizable(False, False)

        self.pontuacao = 0
        self.dificuldade = None
        self.criar_interface()

    def criar_interface(self):
        self.frame_dificuldade = tk.Frame(self.root, bg=CORES["FUNDO"])
        self.frame_jogo = tk.Frame(self.root, bg=CORES["FUNDO"])

        # --- TELA DE DIFICULDADE ---
        tk.Label(self.frame_dificuldade, text="JOGO DA FORCA", font=FONTES["TITULO"], bg=CORES["FUNDO"], fg=CORES["TEXTO"]).pack(pady=(120, 20))
        tk.Label(self.frame_dificuldade, text="Escolha a dificuldade para começar:", font=("Calibri", 18), bg=CORES["FUNDO"], fg=CORES["TEXTO"]).pack(pady=20)
        botoes_dificuldade_frame = tk.Frame(self.frame_dificuldade, bg=CORES["FUNDO"])
        botoes_dificuldade_frame.pack(pady=40)
        for nivel in CONFIG_DIFICULDADE.keys():
            tk.Button(botoes_dificuldade_frame, text=nivel, font=("Calibri", 16, "bold"), command=lambda n=nivel: self.escolher_dificuldade(n), cursor="hand2", bg=CORES["DESTAQUE"], fg=CORES["FUNDO"], activebackground=CORES["FUNDO_SECUNDARIO"], activeforeground=CORES["TEXTO"], relief="flat", bd=0, padx=25, pady=15).pack(side=tk.LEFT, padx=15)

        # --- TELA DE JOGO ---
        # <<< NOVO: Layout principal com duas colunas
        frame_canvas = tk.Frame(self.frame_jogo, bg=CORES["FUNDO"])
        frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        frame_controles = tk.Frame(self.frame_jogo, bg=CORES["FUNDO"])
        frame_controles.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # <<< NOVO: Canvas para desenhar a forca
        self.canvas_forca = tk.Canvas(frame_canvas, width=300, height=400, bg=CORES["FUNDO"], highlightthickness=0)
        self.canvas_forca.pack(anchor=tk.CENTER, expand=True)

        # Elementos da coluna da direita (controles)
        self.palavra_label = tk.Label(frame_controles, text="", font=FONTES["PALAVRA"], bg=CORES["FUNDO"], fg=CORES["TEXTO"], wraplength=400, justify='center')
        self.palavra_label.pack(pady=(40, 20))
        
        self.feedback_label = tk.Label(frame_controles, text="", font=FONTES["FEEDBACK"], bg=CORES["FUNDO"])
        self.feedback_label.pack(pady=10, fill=tk.X)

        entrada_frame = tk.Frame(frame_controles, bg=CORES["FUNDO"])
        entrada_frame.pack(pady=20)
        self.entrada = tk.Entry(entrada_frame, font=("Consolas", 24, "bold"), width=3, justify='center', bg=CORES["FUNDO_SECUNDARIO"], fg=CORES["TEXTO"], insertbackground=CORES["TEXTO"], relief="flat", bd=10)
        self.entrada.pack(side=tk.LEFT, padx=10)
        self.entrada.bind("<FocusIn>", lambda e: e.widget.config(bg=CORES["DESTAQUE"]))
        self.entrada.bind("<FocusOut>", lambda e: e.widget.config(bg=CORES["FUNDO_SECUNDARIO"]))
        self.btn_enviar = tk.Button(entrada_frame, text="Tentar", font=FONTES["NORMAL"], command=self.verificar_tentativa, bg=CORES["DESTAQUE"], fg=CORES["FUNDO"], relief="flat", bd=0, padx=20, pady=5, cursor="hand2")
        self.btn_enviar.pack(side=tk.LEFT)
        self.root.bind('<Return>', lambda event: self.verificar_tentativa())
        
        self.btn_dica = tk.Button(frame_controles, text="Pedir Dica (-1 Tentativa)", font=FONTES["NORMAL"], command=self.pedir_dica, cursor="hand2", bg=CORES["AVISO"], fg=CORES["FUNDO"], relief="flat", bd=0, padx=15, pady=8)
        self.btn_dica.pack(pady=15)
        
        self.letras_usadas_label = tk.Label(frame_controles, text="", font=FONTES["NORMAL"], bg=CORES["FUNDO"], fg=CORES["AVISO"], wraplength=400)
        self.letras_usadas_label.pack(pady=10)
        
        status_frame = tk.Frame(self.root, bg=CORES["FUNDO_SECUNDARIO"])
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.tentativa_label = tk.Label(status_frame, text="", font=FONTES["NORMAL"], bg=CORES["FUNDO_SECUNDARIO"], fg=CORES["TEXTO"])
        self.tentativa_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.pontuacao_label = tk.Label(status_frame, text=f"Pontuação: 0", font=FONTES["PONTUACAO"], bg=CORES["FUNDO_SECUNDARIO"], fg=CORES["TEXTO"])
        self.pontuacao_label.pack(side=tk.RIGHT, padx=20, pady=10)

        self.frame_dificuldade.pack(expand=True, fill=tk.BOTH)
        
    def desenhar_forca(self, erros):
        self.canvas_forca.delete("all")
        # Desenha a base da forca
        self.canvas_forca.create_line(50, 350, 250, 350, width=4, fill=CORES["TEXTO"]) # base
        self.canvas_forca.create_line(100, 350, 100, 50, width=4, fill=CORES["TEXTO"])  # poste
        self.canvas_forca.create_line(100, 50, 200, 50, width=4, fill=CORES["TEXTO"])   # viga
        self.canvas_forca.create_line(200, 50, 200, 100, width=4, fill=CORES["TEXTO"])  # corda

        partes = [
            lambda: self.canvas_forca.create_oval(175, 100, 225, 150, width=3, outline=CORES["TEXTO"]), # cabeça
            lambda: self.canvas_forca.create_line(200, 150, 200, 250, width=3, fill=CORES["TEXTO"]),   # corpo
            lambda: self.canvas_forca.create_line(200, 175, 150, 225, width=3, fill=CORES["TEXTO"]),   # braço esquerdo
            lambda: self.canvas_forca.create_line(200, 175, 250, 225, width=3, fill=CORES["TEXTO"]),   # braço direito
            lambda: self.canvas_forca.create_line(200, 250, 150, 300, width=3, fill=CORES["TEXTO"]),   # perna esquerda
            lambda: self.canvas_forca.create_line(200, 250, 250, 300, width=3, fill=CORES["TEXTO"])    # perna direita
        ]
        
        # Desenha as partes do corpo de acordo com o número de erros
        for i in range(erros):
            if i < len(partes):
                partes[i]()
                
    def mostrar_feedback(self, mensagem, cor):
        self.feedback_label.config(text=mensagem, fg=cor)
        self.root.after(2000, lambda: self.feedback_label.config(text=""))
        
    def escolher_dificuldade(self, nivel):
        self.dificuldade = nivel
        self.frame_dificuldade.pack_forget()
        self.frame_jogo.pack(expand=True, fill=tk.BOTH)
        self.reiniciar_rodada()
        
    def reiniciar_rodada(self):
        self.entrada.focus_set()
        self.letras_tentadas = set()
        self.tentativas_restantes = CONFIG_DIFICULDADE[self.dificuldade]
        if not PALAVRAS_COM_DICAS: self.root.quit()
        self.palavra_atual = random.choice(list(PALAVRAS_COM_DICAS.keys()))
        self.palavra_oculta = ["_" if c.isalpha() else c for c in self.palavra_atual]
        self.atualizar_interface()
        
    def verificar_tentativa(self):
        palpite = self.entrada.get().lower()
        self.entrada.delete(0, tk.END)
        if not palpite.isalpha() or len(palpite) != 1: return
        if palpite in self.letras_tentadas:
            self.mostrar_feedback("Letra já utilizada!", CORES["AVISO"])
            return
            
        self.letras_tentadas.add(palpite)
        
        if palpite in self.palavra_atual:
            self.mostrar_feedback("Letra Correta!", CORES["SUCESSO"])
            for i, letra in enumerate(self.palavra_atual):
                if letra == palpite: self.palavra_oculta[i] = palpite
            self.pontuacao += 1
        else:
            self.mostrar_feedback("Letra Incorreta!", CORES["ERRO"])
            self.tentativas_restantes -= 1
            self.pontuacao -= 2
            
        self.verificar_fim_de_jogo()
        self.atualizar_interface()
        
    def pedir_dica(self):
        if self.tentativas_restantes > 1:
            self.tentativas_restantes -= 1
            dica = random.choice(PALAVRAS_COM_DICAS[self.palavra_atual])
            messagebox.showinfo("Dica", f"A dica é:\n\n{dica}")
            self.verificar_fim_de_jogo()
            self.atualizar_interface()
        else:
            messagebox.showwarning("Sem Tentativas", "Você precisa de mais de 1 tentativa restante para pedir uma dica.")
            
    def verificar_fim_de_jogo(self):
        venceu = "_" not in self.palavra_oculta
        perdeu = self.tentativas_restantes <= 0
        
        if venceu or perdeu:
            msg_final = f"Você venceu! A palavra era '{self.palavra_atual.upper()}'." if venceu else f"Você perdeu! A palavra era '{self.palavra_atual.upper()}'."
            if venceu: self.pontuacao += 10
            
            self.entrada.config(state=tk.DISABLED)
            self.btn_enviar.config(state=tk.DISABLED)
            
            jogar_novamente = messagebox.askyesno("Fim da Rodada", f"{msg_final}\n\nDeseja jogar outra rodada?")
            
            self.entrada.config(state=tk.NORMAL)
            self.btn_enviar.config(state=tk.NORMAL)
            
            if jogar_novamente: self.reiniciar_rodada()
            else: self.root.quit()
            
    def atualizar_interface(self):
        self.palavra_label.config(text=" ".join(self.palavra_oculta).upper())
        self.tentativa_label.config(text=f"Tentativas: {self.tentativas_restantes}")
        self.pontuacao_label.config(text=f"Pontuação: {self.pontuacao}")
        letras_str = ", ".join(sorted(list(self.letras_tentadas)))
        self.letras_usadas_label.config(text=f"Letras Usadas: {letras_str}")
        
        # Desenha a forca com base no número de erros
        erros = CONFIG_DIFICULDADE[self.dificuldade] - self.tentativas_restantes
        self.desenhar_forca(erros)

if __name__ == "__main__":
    root = tk.Tk()
    app = JogoDaForcaGUI(root)
    root.mainloop()