from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import os

class IMG_Stegno:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Steganography')
        self.root.geometry('600x700')
        self.root.configure(bg='#2C3E50')
        self.main_menu()

    def main_menu(self):
        frame = Frame(self.root, bg='#2C3E50')
        frame.pack(fill='both', expand=True)

        title = Label(frame, text='Image Steganography', font=('Arial', 30, 'bold'), bg='#2C3E50', fg='#ECF0F1')
        title.pack(pady=30)

        encode_btn = Button(
            frame, text="Encode Message", command=lambda: self.encode_menu(frame),
            font=('Arial', 16, 'bold'), bg='#3498DB', fg='white', relief=GROOVE, padx=10, pady=5
        )
        encode_btn.pack(pady=20)

        decode_btn = Button(
            frame, text="Decode Message", command=lambda: self.decode_menu(frame),
            font=('Arial', 16, 'bold'), bg='#1ABC9C', fg='white', relief=GROOVE, padx=10, pady=5
        )
        decode_btn.pack(pady=20)

        quit_btn = Button(
            frame, text="Quit", command=self.root.quit,
            font=('Arial', 16, 'bold'), bg='#E74C3C', fg='white', relief=GROOVE, padx=10, pady=5
        )
        quit_btn.pack(pady=20)

    def back(self, frame):
        frame.destroy()
        self.main_menu()

    def encode_menu(self, parent_frame):
        parent_frame.destroy()
        frame = Frame(self.root, bg='#2C3E50')
        frame.pack(fill='both', expand=True)

        title = Label(frame, text='Encode Message', font=('Arial', 24, 'bold'), bg='#2C3E50', fg='#ECF0F1')
        title.pack(pady=20)

        select_btn = Button(
            frame, text="Select Image", command=lambda: self.select_image_for_encoding(frame),
            font=('Arial', 16, 'bold'), bg='#3498DB', fg='white', relief=GROOVE, padx=10, pady=5
        )
        select_btn.pack(pady=20)

        back_btn = Button(
            frame, text="Back", command=lambda: self.back(frame),
            font=('Arial', 16, 'bold'), bg='#E74C3C', fg='white', relief=GROOVE, padx=10, pady=5
        )
        back_btn.pack(pady=20)

    def decode_menu(self, parent_frame):
        parent_frame.destroy()
        frame = Frame(self.root, bg='#2C3E50')
        frame.pack(fill='both', expand=True)

        title = Label(frame, text='Decode Message', font=('Arial', 24, 'bold'), bg='#2C3E50', fg='#ECF0F1')
        title.pack(pady=20)

        select_btn = Button(
            frame, text="Select Image", command=lambda: self.select_image_for_decoding(frame),
            font=('Arial', 16, 'bold'), bg='#1ABC9C', fg='white', relief=GROOVE, padx=10, pady=5
        )
        select_btn.pack(pady=20)

        back_btn = Button(
            frame, text="Back", command=lambda: self.back(frame),
            font=('Arial', 16, 'bold'), bg='#E74C3C', fg='white', relief=GROOVE, padx=10, pady=5
        )
        back_btn.pack(pady=20)

    def select_image_for_encoding(self, frame):
        file_path = tkinter.filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            self.display_encode_frame(file_path, frame)

    def display_encode_frame(self, image_path, parent_frame):
        parent_frame.destroy()
        frame = Frame(self.root, bg='#2C3E50')
        frame.pack(fill='both', expand=True)

        img = Image.open(image_path)
        img_resized = img.resize((300, 200))
        img = ImageTk.PhotoImage(img_resized)

        img_label = Label(frame, image=img, bg='#2C3E50')
        img_label.image = img
        img_label.pack(pady=20)

        text_label = Label(frame, text="Enter your secret message:", font=('Arial', 16), bg='#2C3E50', fg='#ECF0F1')
        text_label.pack(pady=10)

        text_box = Text(frame, width=50, height=10, font=('Arial', 12))
        text_box.pack(pady=10)

        save_btn = Button(
            frame, text="Save Encoded Image", command=lambda: self.encode_message(img, text_box.get("1.0", END).strip(), image_path),
            font=('Arial', 16, 'bold'), bg='#3498DB', fg='white', relief=GROOVE, padx=10, pady=5
        )
        save_btn.pack(pady=10)

        back_btn = Button(
            frame, text="Back", command=lambda: self.back(frame),
            font=('Arial', 16, 'bold'), bg='#E74C3C', fg='white', relief=GROOVE, padx=10, pady=5
        )
        back_btn.pack(pady=10)

    def encode_message(self, img, message, image_path):
        if not message:
            messagebox.showerror("Error", "Please enter a message to encode.")
            return

        new_img = Image.open(image_path)
        self.encode_data(new_img, message)
        save_path = tkinter.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            new_img.save(save_path)
            messagebox.showinfo("Success", f"Image saved successfully at {save_path}")

    def encode_data(self, img, data):
        binary_data = ''.join(format(ord(char), '08b') for char in data)
        pixels = list(img.getdata())
        data_index = 0

        for i in range(len(pixels)):
            pixel = list(pixels[i])
            for j in range(3):
                if data_index < len(binary_data):
                    pixel[j] = pixel[j] & ~1 | int(binary_data[data_index])
                    data_index += 1
            pixels[i] = tuple(pixel)

        img.putdata(pixels)

    def select_image_for_decoding(self, frame):
        file_path = tkinter.filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            self.decode_message(file_path)

    def decode_message(self, image_path):
        img = Image.open(image_path)
        binary_data = ''
        pixels = list(img.getdata())

        for pixel in pixels:
            for color in pixel[:3]:
                binary_data += str(color & 1)

        data = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
        messagebox.showinfo("Hidden Message", f"Decoded Message: {data}")

if __name__ == "__main__":
    root = Tk()
    app = IMG_Stegno(root)
    root.mainloop()
