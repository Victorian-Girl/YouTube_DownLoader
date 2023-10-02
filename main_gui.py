from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
import os
import ffmpeg


root = Tk()
root.title("YouTube Downloader")
root.geometry("625x530")
root.resizable(True, True)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

my_sizegrip = ttk.Sizegrip(root)
my_sizegrip.grid(row=5, column=3, sticky=SE)

urls = []  # liste des urls
urls_termine = []  # liste des urls terminé
contents = StringVar()  # variable de texte pour le text_box de la sauvegarde
BASE_YOUTUBE_URL = ("https://www.youtube.com", "https://youtu.be", "https://youtu")
selected = False
default_directory_save = os.path.expanduser("~/Downloads")
contents.set(default_directory_save)


"""------------------------------------------------------------------------------------------"""


# Creation des fonctions
def add_to_list():
    while True:  # tant que c'est True
        try:
            url = url_entry_box.get()  # récupère l'url
            if url == "":
                messagebox.showerror("Error", "Please enter a URL")
                break
            if not url.startswith(BASE_YOUTUBE_URL):
                messagebox.showerror("Error", "Please enter a valid URL")
                url_entry_box.delete(0, END)
                break
            if url in urls:
                messagebox.showerror("Error", "URL already in the list")
                url_entry_box.delete(0, END)
                break
            urls.append(url)
            url_entry_box.delete(0, END)
            # print(urls)
            youtube_video = YouTube(url)
            my_text.insert(END, f"{youtube_video.title}\n")
            break
        except Exception as e:
            messagebox.showerror("Error", "Please enter a valid URL")
            url_entry_box.delete(0, END)
            break


def clear_urls_list():
    my_text.delete("1.0", END)  # supprime tout le text du text box
    status_bar.config(text="Ready...")  # remet le  message dans la barre de statut
    progress_bar["value"] = 0
    urls.clear()  # supprime tout les éléments de la liste des urls


def setting_directory_save():
    directory = filedialog.askdirectory(initialdir="C:/",
                                        title="Select a directory for the download File")  # ouvre la fenêtre de selection de dossier
    contents.set(directory)  # set la variable de texte pour le text box
    save_entry_box.config(textvariable=contents)  # affiche le dossier selectionné dans le text box
    # print(directory)


def download():
    for url in urls:
        download_video(url)


def on_download_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = round((bytes_downloaded / total_size) * 100, 2)
    progress_bar["value"] = progress
    progress_bar.update()
    status_bar.config(text=f"Téléchargement en cours...{progress}%")
    # percent = (100 * (stream.filesize - bytes_remaining)) / stream.filesize
    # progress_bar["value"] = percent
    # progress_bar.update_idletasks()
    # root.update_idletasks()


def download_video(url):
    while True:
        youtube_video = YouTube(url)
        youtube_video.register_on_progress_callback(on_download_progress)
        # print("STREAMS")
        status_bar.config(text="Aquisition du lien demandé..." + youtube_video.title)
        streams = youtube_video.streams.filter(progressive=False, file_extension="mp4",
                                               type="video").order_by("resolution").desc()
        video_stream = streams[0]
        streams = youtube_video.streams.filter(progressive=False, file_extension="mp4",
                                               type="audio").order_by("abr").desc()
        audio_stream = streams[0]

        status_bar.config(
            text="Téléchargement en cours..." + youtube_video.title)  # affiche le message dans la barre de statut
        # print(f"Téléchargement: {youtube_video.title}...")
        video_stream.download("video")
        audio_stream.download("audio")

        audio_filename = os.path.join("audio", video_stream.default_filename)
        video_filename = os.path.join("video", video_stream.default_filename)
        output_filrname = os.path.join(contents.get(), video_stream.default_filename)

        ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename),
                      output_filrname, vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)

        status_bar.config(text="Téléchargement terminé")  # affiche le message dans la barre de statut
        # print("Téléchargement terminé")
        os.remove(video_filename)
        os.remove(audio_filename)
        os.rmdir("video")
        os.rmdir("audio")
        urls_termine.append(url)
        progress_bar.update_idletasks()
        status_bar.update_idletasks()
        root.update_idletasks()
        # print(f"Url terminer", urls_termine, {youtube_video.title})
        # print(f"Liste de depart", urls, {youtube_video.title})
        break

    # affiche une boite de message, efface la liste des urls et efface le text box, une fois le téléchargement terminé
    if urls_termine == urls:
        messagebox.showinfo("Téléchargement terminé", "Téléchargenent de(s) " + str(len(urls)) + " vidéos terminé")
        clear_urls_list()
        urls_termine.clear()
        root.update()


def instructions():
    messagebox.showinfo("Instruction", "                Select a folder to download your Video."
                                       "\n            Then paste a YouTbue Url into the text box,"
                                       "\nclick the Add URL to download list button to add it to the list. "
                                       "\n                   Add as many urls as you want. "
                                       "\n    Then click the Download button to start the download."
                                       "\n                                       ANJOY!")


def about():
    messagebox.showinfo("About", "            Youtube Video Downloader"
                                 "\n                      Version 1.0.0.1"
                                 "\n                    Created by: M_CH"
                                 "\n                             2022")


# select_text function
def select_text(e):
    # grab the text widget
    global selected
    try:
        selected = url_entry_box.selection_get()
    except:
        pass


# paste text function
def paste_text(e):
    global selected

    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = url_entry_box.index(INSERT)
            url_entry_box.insert(position, str(selected))


def m_paste_text(e):
    global selected

    selected = root.clipboard_get()
    file_menu.tk_popup(e.x_root, e.y_root)


"""------------------------------------------------------------------------------------------"""


# Creation des modes d'affichage


# Default mode
def default_moda():
    main_color = "SystemButtonFace"  # basic color of window
    second_color = "SystemButtonFace"
    text_color = "black"
    text_color2 = "black"

    root.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_color)
    my_text.config(bg="white")
    url_text_label.config(bg=main_color, fg=text_color2)
    url_entry_box.config(bg=second_color, fg=text_color2)
    add_url_button.config(bg=second_color, fg=text_color2)
    save_label.config(bg=main_color, fg=text_color2)
    save_entry_box.config(bg=second_color, fg=text_color2)
    browse_button.config(bg=second_color, fg=text_color2)
    download_button.config(bg=second_color, fg=text_color2)
    progress_label.config(bg=main_color, fg=text_color2)

    # file munu colors
    file_menu.config(bg=second_color, fg=text_color2)
    options_menu.config(bg=second_color, fg=text_color2)
    help_menu.config(bg=second_color, fg=text_color2)


# Turn on night mode
def night_on():
    main_color = "#000000"  # black
    second_color = "#373737"  # dark gray
    text_color = "light blue"
    text_color2 = "light blue"

    root.config(bg=main_color)  # config du root du gui
    status_bar.config(bg=main_color, fg=text_color)  # config status bar
    my_text.config(bg=second_color)
    url_text_label.config(bg=main_color, fg=text_color2)
    url_entry_box.config(bg=second_color, fg=text_color2)
    add_url_button.config(bg=second_color, fg=text_color2)
    save_label.config(bg=main_color, fg=text_color2)
    save_entry_box.config(bg=second_color, fg=text_color2)
    browse_button.config(bg=second_color, fg=text_color2)
    download_button.config(bg=second_color, fg=text_color2)
    progress_label.config(bg=main_color, fg=text_color2)

    # file munu colors
    file_menu.config(bg=second_color, fg=text_color2)  # menu bar dropdown menue confing
    options_menu.config(bg=second_color, fg=text_color2)
    help_menu.config(bg=second_color, fg=text_color2)


# Turn on violet mode
def violet_on():
    main_color = "purple2"
    second_color = "maroon3"
    text_color = "lightskyblue3"
    text_color2 = "slategray2"

    root.config(bg=main_color)  # config du root du gui
    status_bar.config(bg=main_color, fg=text_color)  # config status bar
    my_text.config(bg=second_color)
    url_text_label.config(bg=main_color, fg=text_color2)
    url_entry_box.config(bg=second_color, fg=text_color2)
    add_url_button.config(bg=second_color, fg=text_color2)
    save_label.config(bg=main_color, fg=text_color2)
    save_entry_box.config(bg=second_color, fg=text_color2)
    browse_button.config(bg=second_color, fg=text_color2)
    download_button.config(bg=second_color, fg=text_color2)
    progress_label.config(bg=main_color, fg=text_color2)

    # file munu colors
    file_menu.config(bg=second_color, fg=text_color2)  # menu bar dropdown menue confing
    options_menu.config(bg=second_color, fg=text_color2)
    help_menu.config(bg=second_color, fg=text_color2)


# Turn on light brown mode
def light_brown_on():
    main_color = "salmon3"
    second_color = "darkorange4"
    text_color = "navajowhite2"
    text_color2 = "lavender"

    root.config(bg=main_color)  # config du root du gui
    status_bar.config(bg=main_color, fg=text_color)  # config status bar
    my_text.config(bg=second_color)
    url_text_label.config(bg=main_color, fg=text_color2)
    url_entry_box.config(bg=second_color, fg=text_color2)
    add_url_button.config(bg=second_color, fg=text_color2)
    save_label.config(bg=main_color, fg=text_color2)
    save_entry_box.config(bg=second_color, fg=text_color2)
    browse_button.config(bg=second_color, fg=text_color2)
    download_button.config(bg=second_color, fg=text_color2)
    progress_label.config(bg=main_color, fg=text_color2)

    # file munu colors
    file_menu.config(bg=second_color, fg=text_color2)  # menu bar dropdown menue confing
    options_menu.config(bg=second_color, fg=text_color2)
    help_menu.config(bg=second_color, fg=text_color2)


# Turn on vampire mode
def vampire_on():
    main_color = "red4"
    second_color = "gray29"
    text_color = "slate gray"
    text_color2 = "light gray"

    root.config(bg=main_color)  # config du root du gui
    status_bar.config(bg=main_color, fg=text_color)  # config status bar
    my_text.config(bg=second_color)
    url_text_label.config(bg=main_color, fg=text_color2)
    url_entry_box.config(bg=second_color, fg=text_color2)
    add_url_button.config(bg=second_color, fg=text_color2)
    save_label.config(bg=main_color, fg=text_color2)
    save_entry_box.config(bg=second_color, fg=text_color2)
    browse_button.config(bg=second_color, fg=text_color2)
    download_button.config(bg=second_color, fg=text_color2)
    progress_label.config(bg=main_color, fg=text_color2)

    # file munu colors
    file_menu.config(bg=second_color, fg=text_color2)  # menu bar dropdown menue confing
    options_menu.config(bg=second_color, fg=text_color2)
    help_menu.config(bg=second_color, fg=text_color2)


# Turn on Orc mode
def orc_on():
    main_color = "dark green"
    second_color = "palegreen4"
    text_color = "goldenrod4"
    text_color2 = "lemon chiffon"

    root.config(bg=main_color)  # config du root du gui
    status_bar.config(bg=main_color, fg=text_color)  # config status bar
    my_text.config(bg=second_color)
    url_text_label.config(bg=main_color, fg=text_color2)
    url_entry_box.config(bg=second_color, fg=text_color2)
    add_url_button.config(bg=second_color, fg=text_color2)
    save_label.config(bg=main_color, fg=text_color2)
    save_entry_box.config(bg=second_color, fg=text_color2)
    browse_button.config(bg=second_color, fg=text_color2)
    download_button.config(bg=second_color, fg=text_color2)
    progress_label.config(bg=main_color, fg=text_color2)

    # file munu colors
    file_menu.config(bg=second_color, fg=text_color2)  # menu bar dropdown menue confing
    options_menu.config(bg=second_color, fg=text_color2)
    help_menu.config(bg=second_color, fg=text_color2)


# Turn on ocean breeze mode
def ocean_on():
    main_color = "blue2"
    second_color = "deep sky blue"
    text_color = "slate gray"
    text_color2 = "black"

    root.config(bg=main_color)  # config du root du gui
    status_bar.config(bg=main_color, fg=text_color)  # config status bar
    my_text.config(bg=text_color)
    url_text_label.config(bg=main_color, fg=text_color)
    url_entry_box.config(bg=second_color, fg=text_color)
    add_url_button.config(bg=second_color, fg=text_color2)
    save_label.config(bg=main_color, fg=text_color)
    save_entry_box.config(bg=second_color, fg=text_color)
    browse_button.config(bg=second_color, fg=text_color2)
    download_button.config(bg=second_color, fg=text_color2)
    progress_label.config(bg=main_color, fg=text_color)

    # file munu colors
    file_menu.config(bg=second_color, fg=text_color2)  # menu bar dropdown menue confing
    options_menu.config(bg=second_color, fg=text_color2)
    help_menu.config(bg=second_color, fg=text_color2)


"""------------------------------------------------------------------------------------------------"""
# Creation de la fenetre principale

# text label for the entry box
url_text_label = Label(root, text="Enter Video URL", font=("Helvetica", 10))
url_text_label.grid(row=1, column=0, pady=5, padx=0)

# create the entry box for url
url_entry_box = Entry(root, width=40)
url_entry_box.grid(row=1, column=1, pady=5, padx=0)

# create an add url button to the list
add_url_button = Button(root, text="Add URL to download list", command=add_to_list)
add_url_button.grid(row=1, column=2, pady=5, padx=0)

# create text box where the url will be displayed (the title of the video)
my_text = Text(root, width=62, height=20, font=("Helvetica", 12), selectbackground="yellow",
               selectforeground="black", undo=True)
my_text.grid(row=2, column=0, columnspan=3, pady=10, padx=30)

# save label for the browse button
save_label = Label(root, text="Save to", font=("Helvetica", 10))
save_label.grid(row=3, column=0, pady=5, padx=0)

# create save location entry box
save_entry_box = Entry(root, textvariable=contents, width=50)
save_entry_box.grid(row=3, column=1, pady=5, padx=0)

# browse button
browse_button = Button(root, text="Browse", command=setting_directory_save)
browse_button.grid(row=3, column=2, pady=5, padx=0)

# label for the pregressbar
progress_label = Label(root, text="Progress", font=("Helvetica", 10))
progress_label.grid(row=4, column=0, pady=5, padx=0)
# add a progressbar
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="determinate")
progress_bar.grid(row=4, column=1, pady=10, padx=30)

# create a button for downloading
download_button = Button(root, text="Download", command=download)
download_button.grid(row=4, column=2, pady=5, padx=0)

# add status bar to bottom of app
status_bar = Label(root, text="Ready...", font=("Helvetica", 8), anchor=E, bd=1, relief=SUNKEN, width=90)
status_bar.grid(row=5, column=0, columnspan=3)

root.bind("<Control-v>", paste_text)
root.bind("<Button-1>", select_text)
root.bind("<Button-3>", m_paste_text)

"""------------------------------------------------------------------------------------------------"""
# Creation du menu

# Menu Bar
my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Paste", command=lambda: paste_text(False), accelerator="Ctrl+V")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Default mode", command=default_moda)
options_menu.add_separator()
options_menu.add_command(label="Night Mode On", command=night_on)
options_menu.add_command(label="Vampire Mode On", command=vampire_on)
options_menu.add_command(label="Ocean Breeze Mode On", command=ocean_on)
options_menu.add_command(label="Orc Mode On", command=orc_on)
options_menu.add_command(label="Light Brown Mode On", command=light_brown_on)
options_menu.add_command(label="Violet Mode On", command=violet_on)


help_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Instruction", command=instructions)
help_menu.add_command(label="About", command=about)


root.mainloop()
