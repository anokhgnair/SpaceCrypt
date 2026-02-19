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
    def add_placeholder(self, widget, text):
        # Add placeholder text to a scrolledtext widget
        def on_focus_in(event):
            if widget.get("1.0", tk.END).strip() == text:
                widget.delete("1.0", tk.END)
                widget.config(fg="#222")
        def on_focus_out(event):
            if not widget.get("1.0", tk.END).strip():
                widget.insert("1.0", text)
                widget.config(fg="#b0b0b0")
        widget.insert("1.0", text)
        widget.config(fg="#b0b0b0")
        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)
        # Remove placeholder if user pastes or types
        def on_key(event):
            if widget.get("1.0", tk.END).strip() == text:
                widget.delete("1.0", tk.END)
                widget.config(fg="#222")
        widget.bind("<Key>", on_key)

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
        self.root.configure(bg="#F5F5F7")  # Apple-like soft neutral
        self.root.resizable(False, False)

        # Apple/iOS-inspired font stack
        self.font_family = "SF Pro Display, Helvetica Neue, Arial, Helvetica, sans-serif"
        self.heading_font = ("Helvetica Neue", 18, "bold")
        self.label_font = ("Helvetica Neue", 13, "bold")
        self.text_font = ("Helvetica Neue", 13)

        self.primary_color = "#007AFF"  # iOS blue
        self.secondary_bg = "#E5E5EA"
        self.border_color = "#D1D1D6"
        self.neutral_bg = "#F5F5F7"

        self.container = None
        self.show_welcome_screen()

    def show_welcome_screen(self):
        if self.container:
            self.container.destroy()
        self.container = tk.Frame(self.root, bg=self.neutral_bg, bd=0, highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96, relheight=0.96)
        self.container.grid_propagate(False)

        # Main card frame with more premium look (rounded corners, shadow effect)
        card = tk.Frame(self.container, bg="#fff", bd=0, highlightthickness=1, highlightbackground=self.border_color)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.82)

        # Simulate shadow by stacking a slightly larger frame behind
        shadow = tk.Frame(self.container, bg="#E5E5EA", bd=0, highlightthickness=0)
        shadow.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.94, relheight=0.84)
        card.lift()

        # Center all text in the card
        title = tk.Label(card, text="SpaceCrypt", font=self.heading_font, bg="#fff", fg="#222", anchor="center", justify="center")
        title.grid(row=0, column=0, columnspan=2, pady=(48, 10), padx=15, sticky="nsew")

        subtitle = tk.Label(card, text="Choose an action to begin", font=self.text_font, bg="#fff", fg="#666", anchor="center", justify="center")
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 36), padx=15, sticky="nsew")

        btn_frame = tk.Frame(card, bg="#fff")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(0, 0), padx=15, sticky="nsew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        def style_btn(btn, color):
            btn.config(bg=color, fg="#fff", activebackground="#005BBB", activeforeground="#fff", bd=0, relief=tk.FLAT, cursor="hand2", font=self.label_font, highlightthickness=0)
            def on_enter(e): btn.config(bg="#005BBB")
            def on_leave(e): btn.config(bg=color)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        encode_btn = tk.Button(btn_frame, text="Encode", command=self.show_encode_screen)
        style_btn(encode_btn, self.primary_color)
        encode_btn.grid(row=0, column=0, padx=(0, 10), pady=0, ipadx=18, ipady=7, sticky="ew")

        decode_btn = tk.Button(btn_frame, text="Decode", command=self.show_decode_screen)
        style_btn(decode_btn, self.primary_color)
        decode_btn.grid(row=0, column=1, padx=(10, 0), pady=0, ipadx=18, ipady=7, sticky="ew")

        # Center all rows/columns
        for i in range(3):
            card.grid_rowconfigure(i, weight=1)
        for i in range(2):
            card.grid_columnconfigure(i, weight=1)

    def show_encode_screen(self):
        if self.container:
            self.container.destroy()
        self.container = tk.Frame(self.root, bg=self.neutral_bg, bd=0, highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96, relheight=0.96)
        self.container.grid_propagate(False)

        card = tk.Frame(self.container, bg="#fff", bd=0, highlightthickness=1, highlightbackground=self.border_color)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.88)

        title = tk.Label(card, text="Encode", font=self.heading_font, bg="#fff", fg="#222")
        title.grid(row=0, column=0, columnspan=2, pady=(30, 8), padx=15, sticky="n")

        # Secret message input
        input_frame = tk.Frame(card, bg="#fff")
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)

        self.secret_text = scrolledtext.ScrolledText(
            input_frame, width=38, height=4, font=self.text_font, wrap=tk.WORD,
            bg=self.neutral_bg, fg="#222", bd=0, relief=tk.FLAT,
            highlightthickness=1, highlightbackground=self.border_color, padx=8, pady=6
        )
        self.secret_text.grid(row=0, column=0, sticky="ew")
        self.add_placeholder(self.secret_text, "Type the text you want to encode here.")

        # Encode button
        encode_btn = tk.Button(card, text="Encode", command=self.encode)
        encode_btn.grid(row=2, column=1, sticky="e", padx=(0, 15), pady=(0, 10), ipadx=18, ipady=7)
        encode_btn.config(bg=self.primary_color, fg="#fff", activebackground="#005BBB", activeforeground="#fff", bd=0, relief=tk.FLAT, cursor="hand2", font=self.label_font, highlightthickness=0)
        def on_enter(e): encode_btn.config(bg="#005BBB")
        def on_leave(e): encode_btn.config(bg=self.primary_color)
        encode_btn.bind("<Enter>", on_enter)
        encode_btn.bind("<Leave>", on_leave)

        # Encoded output label
        encoded_label = tk.Label(card, text="Encoded Text", font=self.label_font, bg="#fff", fg="#4a4a4a")
        encoded_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 0))

        # Encoded output + copy icon in a frame
        encoded_output_frame = tk.Frame(card, bg="#fff")
        encoded_output_frame.grid(row=4, column=0, columnspan=2, padx=15, pady=(0, 18), sticky="ew")
        encoded_output_frame.grid_columnconfigure(0, weight=1)
        encoded_output_frame.grid_columnconfigure(1, weight=0)

        self.encoded_output_text = scrolledtext.ScrolledText(
            encoded_output_frame, width=38, height=4, font=self.text_font, wrap=tk.WORD,
            bg=self.neutral_bg, fg="#222", bd=0, relief=tk.FLAT,
            highlightthickness=1, highlightbackground=self.border_color, padx=8, pady=6
        )
        self.encoded_output_text.grid(row=0, column=0, sticky="ewns", padx=(0, 8))

        # Clipboard icon button
        copy_icon_btn = tk.Button(
            encoded_output_frame,
            text="\U0001F4CB",  # Unicode clipboard
            font=("Segoe UI Emoji", 18),
            command=self.copy_encoded_text,
            relief=tk.FLAT,
            cursor="hand2",
            bg=self.neutral_bg,
            bd=0,
            activebackground=self.secondary_bg,
            highlightthickness=0,
            width=2,
            height=1
        )
        copy_icon_btn.grid(row=0, column=1, sticky="ns", padx=(2, 0), pady=2)
        def on_enter_copy(e): copy_icon_btn.config(bg="#E5E5EA")
        def on_leave_copy(e): copy_icon_btn.config(bg=self.neutral_bg)
        copy_icon_btn.bind("<Enter>", on_enter_copy)
        copy_icon_btn.bind("<Leave>", on_leave_copy)
        copy_icon_btn.bind("<FocusIn>", lambda e: copy_icon_btn.configure(highlightthickness=0))

        # Back button
        back_btn = tk.Button(card, text="\u2190 Back", font=self.text_font, bg=self.secondary_bg, fg="#666", activebackground="#D1D1D6", activeforeground="#222", bd=0, relief=tk.FLAT, cursor="hand2", command=self.show_welcome_screen, highlightthickness=0)
        back_btn.grid(row=5, column=0, pady=(0, 0), sticky="w", ipadx=10, ipady=3, padx=(15, 0))
        def on_enter_back(e): back_btn.config(bg="#D1D1D6")
        def on_leave_back(e): back_btn.config(bg=self.secondary_bg)
        back_btn.bind("<Enter>", on_enter_back)
        back_btn.bind("<Leave>", on_leave_back)

    def show_decode_screen(self):
        if self.container:
            self.container.destroy()
        self.container = tk.Frame(self.root, bg=self.neutral_bg, bd=0, highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96, relheight=0.96)
        self.container.grid_propagate(False)

        card = tk.Frame(self.container, bg="#fff", bd=0, highlightthickness=1, highlightbackground=self.border_color)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.88)

        title = tk.Label(card, text="Decode", font=self.heading_font, bg="#fff", fg="#222")
        title.grid(row=0, column=0, columnspan=2, pady=(30, 8), padx=15, sticky="n")

        # Encoded input
        input_frame = tk.Frame(card, bg="#fff")
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)

        self.encoded_input_text = scrolledtext.ScrolledText(
            input_frame, width=38, height=4, font=self.text_font, wrap=tk.WORD,
            bg=self.neutral_bg, fg="#222", bd=0, relief=tk.FLAT,
            highlightthickness=1, highlightbackground=self.border_color, padx=8, pady=6
        )
        self.encoded_input_text.grid(row=0, column=0, sticky="ew")
        self.add_placeholder(self.encoded_input_text, "Paste the text you want to decode here.")

        # Decode button
        decode_btn = tk.Button(card, text="Decode", command=self.decode)
        decode_btn.grid(row=2, column=1, sticky="e", padx=(0, 15), pady=(0, 10), ipadx=18, ipady=7)
        decode_btn.config(bg=self.primary_color, fg="#fff", activebackground="#005BBB", activeforeground="#fff", bd=0, relief=tk.FLAT, cursor="hand2", font=self.label_font, highlightthickness=0)
        def on_enter(e): decode_btn.config(bg="#005BBB")
        def on_leave(e): decode_btn.config(bg=self.primary_color)
        decode_btn.bind("<Enter>", on_enter)
        decode_btn.bind("<Leave>", on_leave)

        # Decoded output label
        decoded_label = tk.Label(card, text="Decoded Output", font=self.label_font, bg="#fff", fg="#4a4a4a")
        decoded_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 0))

        self.decoded_output_text = scrolledtext.ScrolledText(
            card, width=38, height=4, font=self.text_font, wrap=tk.WORD,
            bg=self.neutral_bg, fg="#222", bd=0, relief=tk.FLAT,
            highlightthickness=1, highlightbackground=self.border_color, padx=8, pady=6
        )
        self.decoded_output_text.grid(row=4, column=0, columnspan=2, padx=15, pady=(0, 0), sticky="ew")

        # Back button
        back_btn = tk.Button(card, text="\u2190 Back", font=self.text_font, bg=self.secondary_bg, fg="#666", activebackground="#D1D1D6", activeforeground="#222", bd=0, relief=tk.FLAT, cursor="hand2", command=self.show_welcome_screen, highlightthickness=0)
        back_btn.grid(row=5, column=0, pady=(0, 0), sticky="w", ipadx=10, ipady=3, padx=(15, 0))
        def on_enter_back(e): back_btn.config(bg="#D1D1D6")
        def on_leave_back(e): back_btn.config(bg=self.secondary_bg)
        back_btn.bind("<Enter>", on_enter_back)
        back_btn.bind("<Leave>", on_leave_back)


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