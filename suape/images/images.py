import glob
import os
from pathlib import Path
from tkinter import Button, Frame, Label, Tk, messagebox, BOTH

from PIL import Image, ImageTk


def update_images(image_frame: Frame, image_list: list, image_dir: str) -> None:
    for widget in image_frame.winfo_children():
        widget.destroy()

    patterns = ("*.jpg", "*.png", "*.jpeg")
    image_files = [f for p in patterns for f in glob.glob(os.path.join(image_dir, p))]

    columns = 3
    for idx, path in enumerate(image_files):
        img = Image.open(path)
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        image_list.append(photo)

        lbl = Label(image_frame, image=photo)
        lbl.grid(row=idx // columns, column=idx % columns, padx=5, pady=5)

    image_frame.after(2000, update_images, image_frame, image_list, image_dir)


def train_model() -> None:
    messagebox.showinfo("Treinamento", "Iniciando o treinamento do modelo...")


def start_image_viewer(image_dir: str) -> None:
    root = Tk()
    root.title("Visualizador de Imagens em Tempo Real")
    root.geometry("800x600")

    image_frame = Frame(root)
    image_frame.pack(fill=BOTH, expand=True)

    image_list: list = []

    Button(root, text="Treinar Modelo", command=train_model, font=("Arial", 14), bg="#004A2E", fg="white").pack(pady=10)

    update_images(image_frame, image_list, image_dir)
    root.mainloop()


if __name__ == "__main__":
    start_image_viewer("./images/images")
