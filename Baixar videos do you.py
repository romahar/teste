from plyer import notification
from pytube import YouTube
from customtkinter import CTk, CTkEntry, CTkButton, CTkLabel, CTkRadioButton, CTkFrame, StringVar
from tkinter import filedialog, ttk

# Inicializar a janela principal
tela = CTk()
tela.geometry("500x500")
tela.title("YouTube Video Downloader")

progress_var = StringVar()
progress_var.set("Progresso: 0%")
resolution_var = StringVar(value="720p")

def download_video():
    link = linked.get()
    path = pt.get()
    resolution = resolution_var.get()
    
    if not link or not path:
        notification.notify(title="Erro", message="Link ou caminho não pode estar vazio.", timeout=10)
        return

    try:
        yt = YouTube(link, on_progress_callback=progress_function)
        stream = yt.streams.filter(res=resolution).first()
        if not stream:
            stream = yt.streams.get_highest_resolution()
        stream.download(output_path=path)
        notification.notify(title="Anúncio", message="O download do seu vídeo está completo!", timeout=10)
        reset_fields()
    except Exception as e:
        notification.notify(title="Erro", message=str(e), timeout=10)

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        pt.delete(0, 'end')
        pt.insert(0, folder_selected)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar['value'] = percentage_of_completion
    progress_var.set(f"Progresso: {int(percentage_of_completion)}%")
    tela.update_idletasks()

def reset_fields():
    linked.delete(0, 'end')
    pt.delete(0, 'end')
    progress_bar['value'] = 0
    progress_var.set("Progresso: 0%")
    resolution_var.set("720p")

# Criar componentes da GUI
linked = CTkEntry(tela, placeholder_text="Link...", width=200)
linked.pack(pady=20)

pt = CTkEntry(tela, placeholder_text="Local...", width=200)
pt.pack(pady=5)

browse_button = CTkButton(tela, text="Procurar Pasta...", width=90, command=browse_folder)
browse_button.pack(pady=5)

# Adicionar label e botões de rádio para seleção de resolução
resolution_label = CTkLabel(tela, text="Selecione a Resolução:")
resolution_label.pack(pady=10)

# Adicionar CTkFrame para organizar os botões de rádio horizontalmente
resolution_frame = CTkFrame(tela)
resolution_frame.pack(pady=5)

resolution_options = ["720p", "480p", "360p", "240p"]
for option in resolution_options:
    radio_button = CTkRadioButton(resolution_frame, text=option, variable=resolution_var, value=option)
    radio_button.pack(side="left", padx=2)

download_button = CTkButton(tela, text="Baixar", width=100, hover_color="#87fe2c", fg_color="#C850C0", command=download_video)
download_button.pack(pady=20)

progress_bar = ttk.Progressbar(tela, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(pady=20)

progress_label = CTkLabel(tela, textvariable=progress_var, width=300)
progress_label.pack(pady=10)

# Executar o loop principal
tela.mainloop()
