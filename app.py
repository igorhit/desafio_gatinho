import random
from tkinter import Tk, Button, Label, Frame
from PIL import Image, ImageTk  # Ensure ImageTk is imported
import pygame  # Para tocar o som
import threading  # Para tocar o som em uma thread separada
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Função para sortear 3 números únicos entre 1 e 188
def sortear_numeros():
    return [f"{num:03}" for num in random.sample(range(1, 117), 3)]

# Função para carregar e exibir as imagens na interface
def exibir_imagens(numeros, frame):
    # Limpa o frame antes de exibir novas imagens
    for widget in frame.winfo_children():
        widget.destroy()

    extensoes = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']  # Extensões suportadas
    for numero in numeros:
        encontrou_imagem = False
        for ext in extensoes:
            caminho_imagem = resource_path(f'imagens/{numero}{ext}')  # Caminho da imagem
            try:
                # Tenta carregar a imagem com a extensão atual
                imagem = Image.open(caminho_imagem)
                imagem = imagem.resize((300, 300), Image.Resampling.LANCZOS)  # Redimensiona a imagem
                foto = ImageTk.PhotoImage(imagem)

                # Exibe a imagem em um Label
                label_imagem = Label(frame, image=foto, bg="#2E3440")  # Cor de fundo do label
                label_imagem.image = foto  # Mantém uma referência para evitar garbage collection
                label_imagem.pack(side="left", padx=10, pady=10)
                encontrou_imagem = True
                break  # Sai do loop se a imagem for carregada com sucesso
            except FileNotFoundError:
                continue  # Tenta a próxima extensão
        
        if not encontrou_imagem:
            print(f"Imagem correspondente ao número {numero} não encontrada.")

# Função para tocar o som em uma thread separada
def tocar_som():
    try:
        pygame.mixer.init()  # Inicializa o mixer do pygame
        pygame.mixer.music.load(resource_path("som.mp3"))  # Carrega o arquivo de som
        pygame.mixer.music.play()  # Toca o som
    except Exception as e:
        print(f"Erro ao tocar o som: {e}")

# Função para iniciar a contagem regressiva
def iniciar_contagem_regressiva():
    contagem_label.config(text="3", fg="white")  # Mostra o número 3
    janela.update()
    janela.after(1000, lambda: contagem_label.config(text="2", fg="white"))  # Mostra o número 2 após 1 segundo
    janela.after(2000, lambda: contagem_label.config(text="1", fg="white"))  # Mostra o número 1 após 2 segundos
    janela.after(3000, lambda: contagem_label.config(text="Deu bom ou deu ruim?", fg="white"))  # Mostra "Sorteando..." após 3 segundos
    janela.after(3000, iniciar_sorteio)  # Inicia o sorteio após 3 segundos

# Função chamada quando o botão "Iniciar" é clicado
def iniciar_sorteio():
    # Toca o som em uma thread separada para não bloquear a interface
    threading.Thread(target=tocar_som).start()

    # Sorteia os números e exibe as imagens
    numeros_sorteados = sortear_numeros()
    exibir_imagens(numeros_sorteados, frame_imagens)
    print("Números sorteados:", numeros_sorteados)

# Configuração da interface gráfica
janela = Tk()
janela.title("Desafio do Gatinho")
janela.geometry("1000x500")  # Tamanho da janela
janela.configure(bg="#2E3440")  # Cor de fundo da janela (tons escuros)

# Botão para iniciar o sorteio
botao_iniciar = Button(janela, text="Aperte e se lasque", command=iniciar_contagem_regressiva, bg="#4C566A", fg="white", font=("Arial", 14))
botao_iniciar.pack(pady=20)

# Label para a contagem regressiva
contagem_label = Label(janela, text="", bg="#2E3440", fg="white", font=("Arial", 24))
contagem_label.pack(pady=10)

# Frame para exibir as imagens
frame_imagens = Frame(janela, bg="#2E3440")
frame_imagens.pack()

# Update the path to "icone.ico"
icone_path = resource_path("icone.ico")

# Update the iconbitmap and iconphoto with the new path
try:
    janela.iconbitmap(icone_path)  # Use iconbitmap for .ico files
except Exception as e:
    print(f"Erro ao carregar o ícone: {e}")

# Inicia a interface gráfica
janela.mainloop()

