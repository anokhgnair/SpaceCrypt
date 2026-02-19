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
    def __init__(self, root):
        self.root = root
        self.root.title("SpaceCrypt - Whitespace Steganography")
        self.root.geometry("600x500")

        # Encode Section
        encode_frame = tk.LabelFrame(root, text="Encode Message", padx=10, pady=10)
        encode_frame.pack(pady=10, fill="x")


        tk.Label(encode_frame, text="Secret Message:").grid(row=0, column=0, sticky="nw")
        self.secret_text = scrolledtext.ScrolledText(encode_frame, width=38, height=4, wrap=tk.WORD)
        self.secret_text.grid(row=0, column=1, padx=2, pady=2, sticky="w")

        tk.Button(encode_frame, text="Encode", command=self.encode).grid(row=1, column=1, pady=10)

        tk.Label(encode_frame, text="Encoded Text:").grid(row=2, column=0, sticky="nw")
        self.encoded_output_text = scrolledtext.ScrolledText(encode_frame, width=38, height=4, wrap=tk.WORD)
        self.encoded_output_text.grid(row=2, column=1, padx=2, pady=2, sticky="w")

        # Decode Section
        decode_frame = tk.LabelFrame(root, text="Decode Message", padx=10, pady=10)
        decode_frame.pack(pady=10, fill="x")

        tk.Label(decode_frame, text="Encoded Input:").grid(row=0, column=0, sticky="nw")
        self.encoded_input_text = scrolledtext.ScrolledText(decode_frame, width=38, height=4, wrap=tk.WORD)
        self.encoded_input_text.grid(row=0, column=1, padx=2, pady=2, sticky="w")

        tk.Button(decode_frame, text="Decode", command=self.decode).grid(row=1, column=1, pady=10)

        tk.Label(decode_frame, text="Decoded Output:").grid(row=2, column=0, sticky="nw")
        self.decoded_output_text = scrolledtext.ScrolledText(decode_frame, width=38, height=4, wrap=tk.WORD)
        self.decoded_output_text.grid(row=2, column=1, padx=2, pady=2, sticky="w")


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