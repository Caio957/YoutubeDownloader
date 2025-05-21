# YouTube MP3 Downloader com Interface Gráfica

Este script Python permite baixar o áudio de vídeos do YouTube em formato MP3 de alta qualidade usando uma interface gráfica simples construída com Tkinter.

## Funcionalidades

*   Interface gráfica amigável.
*   Campo para colar o link do vídeo do YouTube.
*   Botão para iniciar o download.
*   Log de atividades para acompanhar o processo.
*   Downloads e conversões para MP3 são feitos em segundo plano para não travar a interface.
*   Salva os arquivos MP3 em uma subpasta `MusicasBaixadas` no diretório do script.

## Requisitos

Para executar este script, você precisará ter o seguinte instalado:

1.  **Python 3:**
    *   Se você não tem Python instalado, baixe-o em [python.org](https://www.python.org/downloads/).
    *   Certifique-se de marcar a opção "Add Python to PATH" durante a instalação.

2.  **yt-dlp:**
    *   Esta é a ferramenta de linha de comando que o script usa para interagir com o YouTube.
    *   **Instalação (via pip - recomendado):**
        ```bash
        pip install -U yt-dlp
        ```
    *   **Alternativa (manual):** Baixe o executável `yt-dlp.exe` da [página de lançamentos do yt-dlp no GitHub](https://github.com/yt-dlp/yt-dlp/releases/latest) e coloque-o em um diretório que esteja no seu PATH do sistema (ou no mesmo diretório do script `baixar_audio.py`).

3.  **FFmpeg:**
    *   Necessário para converter o áudio para o formato MP3. `yt-dlp` usa `ffmpeg` para essa tarefa.
    *   **Download:** Baixe uma compilação para o seu sistema operacional (Windows, macOS, Linux) do site oficial: [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
        *   Para Windows, uma fonte popular de builds é [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (baixe a versão "essentials" ou "full").
    *   **Instalação:**
        1.  Extraia os arquivos baixados para uma pasta no seu computador (por exemplo, `C:\ffmpeg`).
        2.  Adicione o caminho para a subpasta `bin` (que contém `ffmpeg.exe` e `ffprobe.exe`, por exemplo, `C:\ffmpeg\bin`) à variável de ambiente PATH do seu sistema.
        3.  Após adicionar ao PATH, reinicie qualquer terminal ou prompt de comando que estiver aberto.

## Como Executar o Script

1.  **Clone o repositório ou baixe os arquivos:**
    ```bash
    git clone https://github.com/Caio957/YoutubeDownloader.git
    cd YoutubeDownloader
    ```
    Ou baixe o arquivo `baixar_audio.py` diretamente.

2.  **Certifique-se de que todas as dependências (Python 3, yt-dlp, FFmpeg com PATH configurado) estão instaladas e configuradas corretamente.**

3.  **Abra um terminal ou PowerShell, navegue até o diretório onde o `baixar_audio.py` está localizado.**
    Por exemplo:
    ```powershell
    cd C:\Caminho\Para\YoutubeDownloader
    ```

4.  **Execute o script usando Python:**
    ```bash
    python baixar_audio.py
    ```

5.  A interface gráfica será iniciada. Cole o link do vídeo do YouTube, clique em "Baixar MP3" e aguarde o processo ser concluído. Os arquivos serão salvos na pasta `MusicasBaixadas`.

## Solução de Problemas Comuns

*   **`yt-dlp not found` ou `ffmpeg not found`:**
    *   Verifique se `yt-dlp` e `ffmpeg` estão instalados.
    *   Confirme se os diretórios contendo `yt-dlp.exe` (se instalado manualmente) e `ffmpeg.exe` estão corretamente adicionados à variável de ambiente PATH do seu sistema.
    *   Lembre-se de reiniciar seu terminal (ou VS Code, se estiver usando seu terminal integrado) após modificar o PATH.
*   **Interface travada (raro com threads, mas possível):** Se a interface parecer travar, verifique se há mensagens de erro no terminal de onde você lançou o script, caso alguma informação adicional seja impressa lá (embora a maioria deva ir para o log da GUI).

---

Sinta-se à vontade para contribuir ou reportar issues! 