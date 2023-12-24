import subprocess
import tkinter as tk
from tkinter import messagebox
import threading
import time

class ShutdownApp:
    def __init__(self, master):
        self.master = master
        master.title("Desligar o computador")

        self.label_tempo = tk.Label(master, text="Tempo até o desligamento automático (minutos):")
        self.label_tempo.grid(row=0, column=0, padx=10, pady=10)
        self.entry_tempo = tk.Entry(master)
        self.entry_tempo.grid(row=0, column=1, padx=10, pady=10)

        self.desligar_button = tk.Button(master, text="Desligar", command=self.desligar_windows)
        self.desligar_button.grid(row=1, column=0, padx=10, pady=10)

        self.cancelar_button = tk.Button(master, text="Cancelar Desligamento", command=self.cancelar_desligamento)
        self.cancelar_button.grid(row=1, column=1, padx=10, pady=10)
        self.cancelar_button.configure(state=tk.DISABLED)

        self.processo_desligamento = None
        self.verificar_cancelamento_thread = None
        self.is_cancelado = False

    def desligar_windows(self):
        tempo_str = self.entry_tempo.get()

        if not tempo_str:
            messagebox.showwarning("Erro", "Especifique o tempo antes de agendar o desligamento.")
            return

        try:
            tempo = int(tempo_str) * 60
        except ValueError:
            messagebox.showwarning("Erro", "Tempo inválido. Insira um número inteiro.")
            return

        subprocess.call(["shutdown", "/a"])  # Cancela quaisquer agendamentos de desligamento pendentes

        comando = ["shutdown", "-s", "-f", "-t", str(tempo)]
        self.processo_desligamento = subprocess.Popen(comando)

        self.is_cancelado = False  # Reinicia a flag de cancelamento

        # Inicia uma thread para verificar o cancelamento
        self.verificar_cancelamento_thread = threading.Thread(target=self.verificar_cancelamento)
        self.verificar_cancelamento_thread.start()

        # Habilita o botão de cancelamento
        self.cancelar_button.configure(state=tk.NORMAL)

    def verificar_cancelamento(self):
        while True:
            if self.is_cancelado:
                subprocess.call(["shutdown", "/a"])  # Cancela o desligamento se foi solicitado
                self.is_cancelado = False  # Reinicia a flag de cancelamento
            time.sleep(5)  # Verifica a cada 5 segundos

    def cancelar_desligamento(self):
        if self.processo_desligamento:
            self.processo_desligamento.terminate()
            self.processo_desligamento = None
            messagebox.showinfo("Cancelamento", "O desligamento automático foi cancelado com sucesso.")
            
            # Desabilita o botão de cancelamento
            self.cancelar_button.configure(state=tk.DISABLED)
            self.is_cancelado = True  # Marca que o desligamento foi cancelado

root = tk.Tk()
shutdown_app = ShutdownApp(root)
root.mainloop()
