import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


def caesar_cipher(text, shift, alphabet):
    result_text = ""
    for char in text:
        if char in alphabet:
            idx = alphabet.index(char)
            new_idx = (idx + shift) % len(alphabet)
            result_text += alphabet[new_idx]
        else:
            result_text += char
    return result_text


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[
        ("Все текстовые файлы", "*.txt *.md *.csv *.log"),
        ("Текстовые файлы", "*.txt"),
        ("Markdown файлы", "*.md"),
        ("CSV файлы", "*.csv"),
        ("Лог-файлы", "*.log"),
        ("Все файлы", "*.*")
    ])
    if file_path:
        selected_file_label.configure(text=f"Выбран файл: {os.path.basename(file_path)}")
        app_data['selected_file'] = file_path


def save_file(content):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
        ("Все текстовые файлы", "*.txt *.md *.csv *.log"),
        ("Текстовые файлы", "*.txt"),
        ("Markdown файлы", "*.md"),
        ("CSV файлы", "*.csv"),
        ("Лог-файлы", "*.log"),
        ("Все файлы", "*.*")
    ])
    if save_path:
        try:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Успех", "Файл успешно сохранен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения файла: {e}")


def process_file(action, alphabet):
    file_path = app_data.get('selected_file')
    if not file_path:
        messagebox.showwarning("Внимание", "Сначала выберите файл!")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        shift = 3
        if action == "encrypt":
            processed_text = caesar_cipher(text, shift, alphabet)
        elif action == "decrypt":
            processed_text = caesar_cipher(text, -shift, alphabet)
        else:
            raise ValueError("Неизвестное действие")

        save_file(processed_text)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка обработки файла: {e}")


def center_window(app, width, height):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    app.geometry(f"{width}x{height}+{x}+{y}")


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

app_data = {}
app = ctk.CTk()
app.title("Шифрование текста")

window_width = 1000
window_height = 600
center_window(app, window_width, window_height)

icon_path = "icon.ico"
if os.path.exists(icon_path):
    icon_image = Image.open(icon_path).resize((64, 64))
    photo = ImageTk.PhotoImage(icon_image)
    app.iconphoto(True, photo)

HEADER_FONT = ctk.CTkFont(size=24, weight="bold")
TEXT_FONT = ctk.CTkFont(size=16)

alphabet = ''.join(chr(i) for i in range(32, 0x110000))

main_frame = ctk.CTkFrame(app, corner_radius=10)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

welcome_label = ctk.CTkLabel(main_frame, text="Добро пожаловать в приложение \"Шифрование текста\"!",
                             font=HEADER_FONT)
welcome_label.pack(pady=30)

start_button = ctk.CTkButton(main_frame, text="Начать", font=TEXT_FONT, height=50, width=200,
                             command=lambda: switch_frame(panel_frame))
start_button.pack(pady=30)

instructions_button = ctk.CTkButton(main_frame, text="Инструкция", font=TEXT_FONT, height=50, width=200,
                                    command=lambda: switch_frame(instruction_frame))
instructions_button.pack(pady=15)

panel_frame = ctk.CTkFrame(app, corner_radius=10)

panel_title = ctk.CTkLabel(panel_frame, text="Панель управления", font=HEADER_FONT)
panel_title.pack(pady=20)

selected_file_label = ctk.CTkLabel(panel_frame, text="Файл не выбран", font=TEXT_FONT)
selected_file_label.pack(pady=15)

select_file_button = ctk.CTkButton(panel_frame, text="Выбрать файл", font=TEXT_FONT, height=50, width=200,
                                   command=select_file)
select_file_button.pack(pady=15)

encrypt_button = ctk.CTkButton(panel_frame, text="Шифровать", font=TEXT_FONT, height=50, width=200,
                               command=lambda: process_file("encrypt", alphabet))
encrypt_button.pack(pady=15)

decrypt_button = ctk.CTkButton(panel_frame, text="Расшифровать", font=TEXT_FONT, height=50, width=200,
                               command=lambda: process_file("decrypt", alphabet))
decrypt_button.pack(pady=15)

back_button = ctk.CTkButton(panel_frame, text="Назад", font=TEXT_FONT, height=50, width=200, fg_color="red",
                            command=lambda: switch_frame(main_frame))
back_button.pack(pady=30)

instruction_frame = ctk.CTkFrame(app, corner_radius=10)

instruction_title = ctk.CTkLabel(instruction_frame, text="Как пользоваться приложением", font=HEADER_FONT)
instruction_title.pack(pady=20)

instruction_text = ctk.CTkLabel(instruction_frame, text=(
    "1. Нажмите 'Начать' для перехода к панели управления.\n"
    "2. Выберите файл, который хотите зашифровать или расшифровать, нажав 'Выбрать файл'.\n"
    "3. После выбора файла нажмите 'Шифровать' или 'Расшифровать', чтобы выполнить соответствующее действие.\n"
    "4. Когда операция завершена, выберите, куда сохранить результат.\n"
    "5. В любой момент можно вернуться на главный экран, нажав 'Назад'.\n"
), font=TEXT_FONT, justify="left")
instruction_text.pack(padx=20, pady=10)

back_button_instructions = ctk.CTkButton(instruction_frame, text="Назад", font=TEXT_FONT, height=50, width=200,
                                         fg_color="red", command=lambda: switch_frame(main_frame))
back_button_instructions.pack(pady=30)


def switch_frame(frame):
    main_frame.pack_forget()
    panel_frame.pack_forget()
    instruction_frame.pack_forget()
    frame.pack(padx=20, pady=20, fill="both", expand=True)


switch_frame(main_frame)
app.mainloop()
