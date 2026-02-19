import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

def encode_message(secret_file, output_file):
    try:
        # secret_file is now the secret message directly
        secret_message = secret_file
        binary_message = ' '.join(format(x, '08b') for x in bytearray(secret_message, 'utf-8'))

        encoded_message = ""
        for c in binary_message:
            if c == '0':
                encoded_message += " "
            elif c == '1':
                encoded_message += "\t"
            elif c == " ":
                encoded_message += "\n"

        return True, encoded_message
    except Exception as e:
        return False, str(e)

def decode_message(encoded_file, output_file):
    try:
        encoded_message = encoded_file  # now direct text
        decoded_binary = ""
        for c in encoded_message:
            if c == " ":
                decoded_binary += "0"
            elif c == "\t":
                decoded_binary += "1"
            elif c == "\n":
                decoded_binary += " "

        bin_words = decoded_binary.split()
        decoded_message = ""
        for bin_word in bin_words:
            if len(bin_word) == 8:
                decoded_message += chr(int(bin_word, 2))

        return True, decoded_message
    except Exception as e:
        return False, str(e)

class SpaceCryptApp:
    def copy_encoded_text(self):
        encoded = self.encoded_output_text.get("1.0", tk.END).rstrip("\n")
        if encoded:
            self.root.clipboard_clear()
            self.root.clipboard_append(encoded)
            self.root.update()  # Keeps clipboard after window closes
            tk.messagebox.showinfo("Copied", "Encoded text copied to clipboard!")

    def __init__(self, root):
        self.root = root
        self.root.title("SpaceCrypt")
        self.root.geometry("540x650")
        self.root.configure(bg="#f7f7fa")
        self.root.resizable(False, False)

        # Set a modern, clean font
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.title_font = (self.font_family, 20, "bold")
        self.label_font = (self.font_family, 12, "bold")
        self.text_font = (self.font_family, 12)

        self.container = None
        self.show_welcome_screen()

    def show_welcome_screen(self):
        if self.container:
            self.container.destroy()
        self.container = tk.Frame(self.root, bg="#ffffff", bd=0, highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96, relheight=0.96)
        self.container.grid_propagate(False)

        title = tk.Label(self.container, text="SpaceCrypt", font=self.title_font, bg="#ffffff", fg="#222222")
        title.pack(pady=(60, 10))

        subtitle = tk.Label(self.container, text="Choose an action to begin", font=(self.font_family, 13), bg="#ffffff", fg="#666")
        subtitle.pack(pady=(0, 40))

        btn_frame = tk.Frame(self.container, bg="#ffffff")
        btn_frame.pack(pady=(0, 0))

        encode_btn = tk.Button(btn_frame, text="Encode", font=self.label_font, bg="#e0e0e0", fg="#222", activebackground="#d1d1d6", activeforeground="#222", bd=0, relief=tk.FLAT, cursor="hand2", width=14, height=2, command=self.show_encode_screen)
        encode_btn.grid(row=0, column=0, padx=18)

        decode_btn = tk.Button(btn_frame, text="Decode", font=self.label_font, bg="#e0e0e0", fg="#222", activebackground="#d1d1d6", activeforeground="#222", bd=0, relief=tk.FLAT, cursor="hand2", width=14, height=2, command=self.show_decode_screen)
        decode_btn.grid(row=0, column=1, padx=18)

    def show_encode_screen(self):
        if self.container:
            self.container.destroy()
        self.container = tk.Frame(self.root, bg="#ffffff", bd=0, highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96, relheight=0.96)
        self.container.grid_propagate(False)

        title = tk.Label(self.container, text="Encode", font=self.title_font, bg="#ffffff", fg="#222222")
        title.grid(row=0, column=0, columnspan=3, pady=(18, 8), sticky="n")

        self.secret_text = scrolledtext.ScrolledText(self.container, width=38, height=4, font=self.text_font, wrap=tk.WORD, bg="#f5f6fa", fg="#222", bd=0, relief=tk.FLAT, highlightthickness=1, highlightbackground="#e0e0e0")
        self.secret_text.grid(row=1, column=0, columnspan=3, padx=2, pady=(0, 8), sticky="ew")

        encode_btn = tk.Button(self.container, text="Encode", font=self.label_font, bg="#e0e0e0", fg="#222", activebackground="#d1d1d6", activeforeground="#222", bd=0, relief=tk.FLAT, cursor="hand2", command=self.encode, height=1)
        encode_btn.grid(row=2, column=2, pady=(0, 10), sticky="e", ipadx=12, ipady=2)

        encoded_label_frame = tk.Frame(self.container, bg="#ffffff")
        encoded_label_frame.grid(row=3, column=0, sticky="w", pady=(0, 0))
        tk.Label(encoded_label_frame, text="Encoded Text", font=self.label_font, bg="#ffffff", fg="#4a4a4a").pack(side=tk.LEFT)
        copy_icon = tk.Button(encoded_label_frame, text="📋", font=("Segoe UI Emoji", 16), command=self.copy_encoded_text, relief=tk.FLAT, cursor="hand2", bg="#ffffff", bd=0, activebackground="#e0e0e0")
        copy_icon.pack(side=tk.LEFT, padx=(8,0))

        self.encoded_output_text = scrolledtext.ScrolledText(self.container, width=38, height=4, font=self.text_font, wrap=tk.WORD, bg="#f5f6fa", fg="#222", bd=0, relief=tk.FLAT, highlightthickness=1, highlightbackground="#e0e0e0")
        self.encoded_output_text.grid(row=4, column=0, columnspan=3, padx=2, pady=(0, 18), sticky="ew")

        back_btn = tk.Button(self.container, text="← Back", font=(self.font_family, 11), bg="#f7f7fa", fg="#666", activebackground="#e0e0e0", activeforeground="#222", bd=0, relief=tk.FLAT, cursor="hand2", command=self.show_welcome_screen)
        back_btn.grid(row=5, column=0, pady=(0, 0), sticky="w", ipadx=8, ipady=1)

        for btn in [encode_btn, copy_icon, back_btn]:
            btn.bind("<FocusIn>", lambda e: e.widget.configure(highlightthickness=0))

        for i in range(6):
            self.container.grid_rowconfigure(i, pad=2)
        for i in range(3):
            self.container.grid_columnconfigure(i, weight=1)

    def show_decode_screen(self):
        if self.container:
            self.container.destroy()
        self.container = tk.Frame(self.root, bg="#ffffff", bd=0, highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96, relheight=0.96)
        self.container.grid_propagate(False)

        title = tk.Label(self.container, text="Decode", font=self.title_font, bg="#ffffff", fg="#222222")
        title.grid(row=0, column=0, columnspan=3, pady=(18, 8), sticky="n")

        self.encoded_input_text = scrolledtext.ScrolledText(self.container, width=38, height=4, font=self.text_font, wrap=tk.WORD, bg="#f5f6fa", fg="#222", bd=0, relief=tk.FLAT, highlightthickness=1, highlightbackground="#e0e0e0")
        self.encoded_input_text.grid(row=1, column=0, columnspan=3, padx=2, pady=(0, 8), sticky="ew")

        decode_btn = tk.Button(self.container, text="Decode", font=self.label_font, bg="#e0e0e0", fg="#222", activebackground="#d1d1d6", activeforeground="#222", bd=0, relief=tk.FLAT, cursor="hand2", command=self.decode, height=1)
        decode_btn.grid(row=2, column=2, pady=(0, 10), sticky="e", ipadx=12, ipady=2)

        decoded_label = tk.Label(self.container, text="Decoded Output", font=self.label_font, bg="#ffffff", fg="#4a4a4a")
        decoded_label.grid(row=3, column=0, columnspan=3, sticky="w")

        self.decoded_output_text = scrolledtext.ScrolledText(self.container, width=38, height=4, font=self.text_font, wrap=tk.WORD, bg="#f5f6fa", fg="#222", bd=0, relief=tk.FLAT, highlightthickness=1, highlightbackground="#e0e0e0")
        self.decoded_output_text.grid(row=4, column=0, columnspan=3, padx=2, pady=(0, 0), sticky="ew")

        back_btn = tk.Button(self.container, text="← Back", font=(self.font_family, 11), bg="#f7f7fa", fg="#666", activebackground="#e0e0e0", activeforeground="#222", bd=0, relief=tk.FLAT, cursor="hand2", command=self.show_welcome_screen)
        back_btn.grid(row=5, column=0, pady=(0, 0), sticky="w", ipadx=8, ipady=1)

        for btn in [decode_btn, back_btn]:
            btn.bind("<FocusIn>", lambda e: e.widget.configure(highlightthickness=0))

        for i in range(6):
            self.container.grid_rowconfigure(i, pad=2)
        for i in range(3):
            self.container.grid_columnconfigure(i, weight=1)


    # Removed select_secret, not needed anymore


    # Removed select_encode_output, not needed anymore


    # Removed select_encoded and select_decode_output, not needed anymore

    def encode(self):
        secret = self.secret_text.get("1.0", tk.END).rstrip("\n")
        if not secret:
            messagebox.showerror("Error", "Please enter a secret message to encode.")
            return
        success, encoded = encode_message(secret, None)
        if success:
            self.encoded_output_text.delete("1.0", tk.END)
            self.encoded_output_text.insert(tk.END, encoded)
            messagebox.showinfo("Success", "Encoding successful! Encoded message is ready to copy.")
        else:
            messagebox.showerror("Error", encoded)

    def decode(self):
        encoded = self.encoded_input_text.get("1.0", tk.END).rstrip("\n")
        if not encoded:
            messagebox.showerror("Error", "Please enter the encoded message to decode.")
            return
        success, decoded = decode_message(encoded, None)
        if success:
            self.decoded_output_text.delete("1.0", tk.END)
            self.decoded_output_text.insert(tk.END, decoded)
            messagebox.showinfo("Success", "Decoding successful! Decoded message is ready to copy.")
        else:
            messagebox.showerror("Error", decoded)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceCryptApp(root)
    root.mainloop()