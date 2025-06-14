# Jogo da Forca Profissional em Python 🐍

![Status do Projeto](https://img.shields.io/badge/status-concluído-brightgreen)

Um Jogo da Forca completo e funcional desenvolvido em Python, com uma interface gráfica moderna e interativa construída com a biblioteca Tkinter.

![Screenshot do Jogo](https://i.imgur.com/link_para_sua_imagem.png)
*(Dica: Tire um screenshot do seu jogo funcionando e substitua o link acima para exibi-lo aqui!)*

---

### Sobre o Projeto

Este projeto foi criado como um estudo aprofundado de desenvolvimento de aplicações de desktop com Python. Ele evoluiu de um script simples para um jogo robusto, com foco em uma interface de usuário profissional, uma experiência de jogo agradável e uma base de código organizada e orientada a objetos.

### ✨ Funcionalidades

- **Interface Gráfica Moderna:** Design limpo com tema escuro, layout organizado em duas colunas e fontes legíveis.
- **Forca Desenhada Dinamicamente:** A forca e o boneco são desenhados em tempo real na tela a cada erro, usando o widget Canvas do Tkinter.
- **Vasta Biblioteca de Palavras:** Carrega uma lista com milhares de palavras em português a partir de um arquivo externo, garantindo grande rejogabilidade.
- **Sistema de Dificuldade:** Permite ao jogador escolher entre os níveis Fácil, Médio e Difícil, que ajustam o número de tentativas.
- **Feedback Visual e Animações:**
  - Animação de "tremor" na janela ao errar uma letra.
  - Feedback de texto colorido para acertos, erros e letras repetidas.
  - Destaque na caixa de entrada de texto quando selecionada.
- **Recursos de Jogo:** Sistema de pontuação e botão de dica funcional.
- **Código Robusto:** O script é autossuficiente e utiliza caminhos de arquivo absolutos para encontrar seus recursos, funcionando de forma confiável.

### 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Interface Gráfica:** Tkinter
- **Manipulação de Imagens:** Pillow (PIL)
- **Versionamento:** Git e GitHub

### 🚀 Como Rodar o Projeto Localmente

Para executar este projeto, siga os passos abaixo:

1. **Pré-requisitos:**
   - Ter o [Python 3](https://www.python.org/downloads/) instalado.
   - Ter o [Git](https://git-scm.com/downloads/) instalado.

2. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Krsoliveira/Jogo-da-forca-python.git](https://github.com/Krsoliveira/Jogo-da-forca-python.git)
   ```

3. **Navegue até a pasta do projeto:**
   ```bash
   cd Jogo-da-forca-python
   ```

4. **Instale as dependências:**
   A única biblioteca externa necessária é a `Pillow`.
   ```bash
   pip install Pillow
   ```

5. **Execute o jogo:**
   ```bash
   python jogo_da_forca_gui.py
   ```

---
*Este projeto foi desenvolvido com a assistência e orientação da IA do Google.*
