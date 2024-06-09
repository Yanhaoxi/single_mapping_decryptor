import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import sys
sys.path.insert(0,'.')
from tokenizer.all_tokenizer import t5_tokenizer
from decrypt_core import *
import logging


class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)


class SubstitutionCipherGUI:
    def __init__(self, master):
        # Set up logging
        self.logger = logging.getLogger('SubstitutionCipherLogger')
        self.logger.setLevel(logging.DEBUG)  # 设置日志级别为 DEBUG
        # file_handler = logging.FileHandler('substitution_cipher.log')
        # file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # file_handler.setFormatter(formatter)
        # self.logger.addHandler(file_handler)

        self.master = master
        master.title("Substitution Cipher GUI")

        # Left frame for alphabet and substitutions
        self.frame_left = tk.Frame(master)
        self.frame_left.pack(side=tk.LEFT, padx=20, pady=20)

        self.entries = {}
        vc = (master.register(self.on_validate), '%P')  # Validation command

        for i in range(26):
            letter = chr(i + 65)  # ASCII code for uppercase letters
            label = tk.Label(self.frame_left, text=letter, font=("Arial", 14))
            label.grid(row=i, column=0, sticky='e', padx=5, pady=2)
            
            entry = tk.Entry(self.frame_left, width=2, font=("Arial", 14), validate="key", validatecommand=vc)
            entry.grid(row=i, column=1, sticky='w', padx=5, pady=2)
            self.entries[letter] = entry

        # Right frame for text input/output and logs
        self.frame_right = tk.Frame(master)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Input text area
        tk.Label(self.frame_right, text="Input Text:", font=("Arial", 12)).pack(fill=tk.X)
        self.input_text = scrolledtext.ScrolledText(self.frame_right, width=50, height=15, font=("Arial", 12))
        self.input_text.pack(pady=5, fill=tk.BOTH, expand=True)

        # Output text area
        tk.Label(self.frame_right, text="Output Text:", font=("Arial", 12)).pack(fill=tk.X)
        self.output_text = scrolledtext.ScrolledText(self.frame_right, width=50, height=15, font=("Arial", 12))
        self.output_text.pack(pady=5, fill=tk.BOTH, expand=True)

        # Log display area
        tk.Label(self.frame_right, text="Logs:", font=("Arial", 12)).pack(fill=tk.X)
        self.log = scrolledtext.ScrolledText(self.frame_right, height=5, width=50, font=("Arial", 12))
        self.log.pack(pady=10, fill=tk.BOTH, expand=True)
        self.log.config(state=tk.DISABLED)


        # Add a text handler to display log messages in the log area
        text_handler = TextHandler(self.log)
        text_handler.setFormatter(formatter)
        self.logger.addHandler(text_handler)

        # Buttons
        self.button_frame = tk.Frame(self.frame_right)
        self.button_frame.pack()
        self.decrypt_button = tk.Button(self.button_frame, text="Decrypt", font=("Arial", 12), command=self.decrypt_it)
        self.decrypt_button.grid(row=0, column=0, padx=10, pady=20)
        self.tokenize_button = tk.Button(self.button_frame, text="Tokenize", font=("Arial", 12), command=self.tokenize_it)
        self.tokenize_button.grid(row=0, column=1, padx=10, pady=20)
        self.clear_input_button = tk.Button(self.button_frame, text="Clear Input char", font=("Arial", 12), command=self.clear_input)
        self.clear_input_button.grid(row=1, column=0, padx=10, pady=20)
        self.clear_output_button = tk.Button(self.button_frame, text="Clear Output", font=("Arial", 12), command=self.clear_output)
        self.clear_output_button.grid(row=1, column=1, padx=10, pady=20)

    def clear_input(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def clear_output(self):
        self.output_text.delete("1.0", tk.END)


    def on_validate(self, P):
        if len(P) > 1 or (P and not P.isalpha()):
            messagebox.showwarning("Invalid Input", "Please enter a single alphabetic character.")
            return False
        return True

    def read_entries(self):
        result = {}
        for letter, entry in self.entries.items():
            value = entry.get().lower()  # Force uppercase to standardize
            result[letter] = value
        return result
    
    def set_entries(self, mapping):
        # 对传入的mapping解析并修改
        for letter, entry in self.entries.items():
            if letter.lower() in mapping:
                entry.delete(0, tk.END)
                entry.insert(0, mapping[letter.lower()])

    def log_message(self, message):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, message + '\n')
        self.log.config(state=tk.DISABLED)

    def process_input(self)->str:
        user_input = self.input_text.get("1.0", tk.END)
        filtered_input = ''.join([char.lower() for char in user_input if char.isalpha()])
        return filtered_input


    def decrypt_it(self):
        chipher = self.process_input()
        # 检查输入是否构成了闭包
        #不构成闭包的话，直接解密
        check_dict:dict[str:str] = self.read_entries()#大写字母：小写字母|空
        flag = True
        for k,v in check_dict.items():
            if check_dict[k] != '':
                if check_dict[check_dict[k].upper()] == '':
                    flag = False
        if flag==False:
            self.log_message("Warning: The input can't form a Closure, they will be ignored.")
            vector = tuple('abcdefghijklmnopqrstuvwxyz')
        # 获取未设置目标的闭包，并将构成闭包的对密文进行替换
        else:
            vector = []
            sub_dict={}
            for k,v in check_dict.items():
                if check_dict[k] == '':
                    vector.append(k.lower())
                else:
                    sub_dict[k.lower()]=check_dict[k]
            chipher = "".join(sub_dict.get(c, c) for c in chipher)
            vector = tuple(vector)
        # 开始解密
        
        model_para_1 = Model_Para("Order_Token_Model",10, slice(0, 500))
        model_para_2 = Model_Para("Random_Quadgrams_Model", 2, slice(0, 500))
        model_para_3 = Model_Para("Shuffle_Model", 0, slice(0, 500))
        key = decrypt(
            chipher,
            vector,
            10,
            [model_para_2,model_para_1],
        {model_para_2,model_para_1, model_para_3},
            Token_Score,
            logger=self.logger,
        )
        key_mapping = {v: k for v, k in zip(key, vector)}
        self.set_entries(key_mapping)
        chipher = "".join(key_mapping.get(c, c) for c in chipher)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, chipher)


    def tokenize_it(self):
        messsage=self.output_text.get("1.0", tk.END)
        token=t5_tokenizer.tokenize(messsage)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, token)


# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SubstitutionCipherGUI(root)
    root.mainloop()




