import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

def encode_message(secret_file, output_file):
    try:
        with open(secret_file, 'r', encoding='utf-8') as f:
            secret_message = f.read()
        binary_message = ' '.join(format(x, '08b') for x in bytearray(secret_message, 'utf-8'))

        encoded_message = ""
        for c in binary_message:
            if c == '0':
                encoded_message += " "
            elif c == '1':
                encoded_message += "\t"
            elif c == " ":
                encoded_message += "\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encoded_message)
        return True, "Encoding successful!"
    except Exception as e:
        return False, str(e)

def decode_message(encoded_file, output_file):
    try:
        with open(encoded_file, 'r', encoding='utf-8') as f:
            encoded_message = f.read()
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

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decoded_message)
        return True, decoded_message
    except Exception as e:
        return False, str(e)

class SpaceCryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SpaceCrypt - Whitespace Steganography")
        self.root.geometry("600x500")

        # Encode Section
        encode_frame = tk.LabelFrame(root, text="Encode Message", padx=10, pady=10)
        encode_frame.pack(pady=10, fill="x")

        tk.Label(encode_frame, text="Secret Message File:").grid(row=0, column=0, sticky="w")
        self.secret_entry = tk.Entry(encode_frame, width=50)
        self.secret_entry.grid(row=0, column=1)
        tk.Button(encode_frame, text="Browse", command=self.select_secret).grid(row=0, column=2)

        tk.Label(encode_frame, text="Output Encoded File:").grid(row=1, column=0, sticky="w")
        self.encode_output_entry = tk.Entry(encode_frame, width=50)
        self.encode_output_entry.grid(row=1, column=1)
        tk.Button(encode_frame, text="Browse", command=self.select_encode_output).grid(row=1, column=2)

        tk.Button(encode_frame, text="Encode", command=self.encode).grid(row=2, column=1, pady=10)

        # Decode Section
        decode_frame = tk.LabelFrame(root, text="Decode Message", padx=10, pady=10)
        decode_frame.pack(pady=10, fill="x")

        tk.Label(decode_frame, text="Encoded File:").grid(row=0, column=0, sticky="w")
        self.encoded_entry = tk.Entry(decode_frame, width=50)
        self.encoded_entry.grid(row=0, column=1)
        tk.Button(decode_frame, text="Browse", command=self.select_encoded).grid(row=0, column=2)

        tk.Label(decode_frame, text="Output Decoded File:").grid(row=1, column=0, sticky="w")
        self.decode_output_entry = tk.Entry(decode_frame, width=50)
        self.decode_output_entry.grid(row=1, column=1)
        tk.Button(decode_frame, text="Browse", command=self.select_decode_output).grid(row=1, column=2)

        tk.Button(decode_frame, text="Decode", command=self.decode).grid(row=2, column=1, pady=10)

        # Decoded Message Display
        self.result_text = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
        self.result_text.pack(pady=10, fill="both", expand=True)

    def select_secret(self):
        file = filedialog.askopenfilename(title="Select Secret Message File", filetypes=[("Text Files", "*.txt")])
        if file:
            self.secret_entry.delete(0, tk.END)
            self.secret_entry.insert(0, file)

    def select_encode_output(self):
        file = filedialog.asksaveasfilename(title="Save Encoded File", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file:
            self.encode_output_entry.delete(0, tk.END)
            self.encode_output_entry.insert(0, file)

    def select_encoded(self):
        file = filedialog.askopenfilename(title="Select Encoded File", filetypes=[("Text Files", "*.txt")])
        if file:
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.insert(0, file)

    def select_decode_output(self):
        file = filedialog.asksaveasfilename(title="Save Decoded File", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file:
            self.decode_output_entry.delete(0, tk.END)
            self.decode_output_entry.insert(0, file)

    def encode(self):
        secret = self.secret_entry.get()
        output = self.encode_output_entry.get()
        if not secret or not output:
            messagebox.showerror("Error", "Please select secret file and output file for encoding.")
            return
        success, msg = encode_message(secret, output)
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def decode(self):
        encoded = self.encoded_entry.get()
        output = self.decode_output_entry.get()
        if not encoded or not output:
            messagebox.showerror("Error", "Please select all files for decoding.")
            return
        success, msg = decode_message(encoded, output)
        if success:
            messagebox.showinfo("Success", "Decoding successful!")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, msg)
        else:
            messagebox.showerror("Error", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceCryptApp(root)
    root.mainloop()