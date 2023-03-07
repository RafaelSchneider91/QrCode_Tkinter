import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Cria a barra de progresso
progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress.pack()

# Função para atualizar a barra de progresso
def update_progress():
    progress['value'] += 10
    if progress['value'] >= 100:
        root.after_cancel(update_progress) # Para o loop após 100%
    else:
        root.after(1000, update_progress) # Atualiza após 1 segundo

# Inicia a atualização da barra de progresso
update_progress()

root.mainloop()
