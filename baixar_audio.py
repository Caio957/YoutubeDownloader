import subprocess
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading

# Mantém uma referência ao diretório base do script para downloads
DIRETORIO_BASE_SCRIPT = os.path.dirname(os.path.abspath(__file__))

def baixar_audio_youtube(url_video, diretorio_saida, log_widget):
    """
    Baixa o áudio de um vídeo do YouTube em formato MP3 de alta qualidade.
    Atualiza o log_widget com o progresso e mensagens.
    """
    def _log(message):
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, message + "\n")
        log_widget.see(tk.END) # Auto-scroll
        log_widget.config(state=tk.DISABLED)
        log_widget.update_idletasks() # Força a atualização da GUI

    try:
        caminho_completo_saida = os.path.join(diretorio_saida, "MusicasBaixadas")
        if not os.path.exists(caminho_completo_saida):
            os.makedirs(caminho_completo_saida)
            _log(f"Diretório '{caminho_completo_saida}' criado.")

        _log(f"Baixando áudio de: {url_video}")

        comando = [
            "yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "-o", os.path.join(caminho_completo_saida, "%(title)s.%(ext)s"),
            url_video
        ]
        
        # Usar startupinfo para não abrir janela de console no Windows
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                    text=True, encoding='utf-8', errors='replace', startupinfo=startupinfo)

        # Log em tempo real do stdout e stderr
        # Não é ideal para GUI porque pode ser muito verboso com yt-dlp, mas demonstra a captura
        # yt-dlp geralmente mostra progresso na mesma linha, o que é difícil de capturar bem aqui
        # para este caso, focaremos na mensagem final.
        
        stdout, stderr = processo.communicate()

        if stdout:
            _log("Saída Padrão:")
            for line in stdout.splitlines(): # yt-dlp pode dar muito output aqui
                if "[download] Destination:" in line or "[ExtractAudio] Destination:" in line or "% of" in line or "has already been downloaded" in line:
                    _log(line)
        
        if processo.returncode == 0:
            _log(f"Download e conversão para MP3 concluídos com sucesso! Salvo em: {caminho_completo_saida}")
        else:
            _log("Ocorreu um erro durante o download ou conversão.")
            if stderr:
                _log("Saída de Erro:")
                for line in stderr.splitlines():
                     _log(line)
                if "ffmpeg" in stderr.lower() or "ffprobe" in stderr.lower():
                    _log("\n--- DICA: Verifique se o ffmpeg está instalado e no PATH do sistema, ou especifique o caminho com --ffmpeg-location. ---")
        
    except FileNotFoundError:
        _log("Erro: O comando 'yt-dlp' não foi encontrado.")
        _log("Certifique-se de que o yt-dlp está instalado e no PATH do sistema.")
    except Exception as e:
        _log(f"Ocorreu um erro inesperado: {e}")
    finally:
        # Reabilita o botão de download aqui se necessário, ou usa uma flag
        if 'app_instance' in globals() and hasattr(app_instance, 'download_button'):
            app_instance.download_button.config(state=tk.NORMAL)

def iniciar_download_thread(url_video, diretorio_saida, log_widget, download_button):
    if not url_video.strip():
        messagebox.showerror("Erro", "O link do vídeo não pode estar vazio.")
        download_button.config(state=tk.NORMAL)
        return
    
    download_button.config(state=tk.DISABLED) # Desabilita o botão durante o download
    thread = threading.Thread(target=baixar_audio_youtube, args=(url_video, diretorio_saida, log_widget))
    thread.daemon = True # Permite que a GUI feche mesmo se a thread estiver rodando
    thread.start()

class App:
    def __init__(self, root):
        self.root = root
        root.title("YouTube MP3 Downloader")
        root.geometry("600x400")

        # Frame para entrada do link
        self.link_frame = tk.Frame(root, pady=10)
        self.link_frame.pack(fill=tk.X)

        self.link_label = tk.Label(self.link_frame, text="Link do Vídeo do YouTube:", padx=5)
        self.link_label.pack(side=tk.LEFT)

        self.link_entry = tk.Entry(self.link_frame, width=50)
        self.link_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.link_entry.focus()
        
        # Frame para botões
        self.button_frame = tk.Frame(root, pady=5)
        self.button_frame.pack(fill=tk.X)

        self.download_button = tk.Button(self.button_frame, text="Baixar MP3", 
                                         command=lambda: iniciar_download_thread(self.link_entry.get(), 
                                                                               DIRETORIO_BASE_SCRIPT, 
                                                                               self.log_text, self.download_button), padx=10)
        self.download_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(self.button_frame, text="Limpar Link", command=self.clear_link_entry, padx=10)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Frame para diretório de saída (opcional, por enquanto fixo)
        # Poderia adicionar um botão para mudar o DIRETORIO_BASE_SCRIPT se quisesse
        # self.output_dir_label = tk.Label(root, text=f"Salvando em: {os.path.join(DIRETORIO_BASE_SCRIPT, 'MusicasBaixadas')}")
        # self.output_dir_label.pack(pady=5)

        # Área de Log
        self.log_label = tk.Label(root, text="Log de Atividades:", pady=5)
        self.log_label.pack()
        
        self.log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, state=tk.DISABLED, padx=5, pady=5)
        self.log_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    def clear_link_entry(self):
        self.link_entry.delete(0, tk.END)
        self.link_entry.focus()

if __name__ == "__main__":
    main_window = tk.Tk()
    app_instance = App(main_window) # Armazena a instância para acesso global se necessário
    main_window.mainloop() 