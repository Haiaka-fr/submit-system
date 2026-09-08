import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import requests
import webbrowser
import ipaddress

THEME = {
    "bg": "#F5F7FA",
    "card_bg": "#FFFFFF",
    "primary": "#825799",
    "text": "#333333",
    "font_family": "Century Gothic",
}

def open_problem_page():
    webbrowser.open_new("https://drive.google.com/file/d/13tzIYNo1PmOkVc3wgRv2dpp6UtqXOwOp/view?usp=drive_link")

def is_valid_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

class upload_app:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("檔案繳交")
        self.root.geometry("1280x720")

        self.amount_of_problems = 3
        self.url = ""
        
        self.fiels = {
            1: None,
            2: None,
            3: None
        }

        self.file_name_labels = {}
        self.code_texts = {}

        while True:
            ask_url = simpledialog.askstring("資料庫", "請輸入資料庫IP：", parent=self.root)
            if not is_valid_ip(ask_url):
                messagebox.showerror("錯誤", "無法辨識的IP")
                self.root.destroy()
                return
            try:
                check = requests.get(f"http://{ask_url}:80")
                if check.status_code == 200:
                    pass
                else:
                    messagebox.showerror("錯誤", "該主機無法連線！")
                    self.root.destroy()
                    return
            except Exception as e:
                messagebox.showerror(f"錯誤", "該主機無法連線！\n{e}")
                self.root.destroy()
                return

            self.url = "http://{}:80/upload".format(ask_url)
            break

        self._setup_ui()

    def _setup_ui(self):
        title_label = tk.Label(
            self.root,
            text="長億高中程式設計研究社 - 程式設計競賽",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["primary"],
            fg="white",
            pady=15,
        )
        title_label.pack(fill=tk.X)

        content_frame = tk.Frame(self.root, bg=THEME["bg"], padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        top_bar = tk.Frame(content_frame, bg=THEME["bg"])
        top_bar.pack(fill=tk.X, pady=(0, 10))

        self.problem_link_label = tk.Button(
            top_bar,
            text="開啟題目",
            font=(THEME["font_family"], 11, "bold"),
            bg="#2F84C1",
            fg="white",
            relief=tk.FLAT,
            pady=8,
            command=open_problem_page
        )
        self.problem_link_label.pack(side=tk.LEFT)

        self.submit_btn = tk.Button(
            top_bar,
            text="繳交",
            font=(THEME["font_family"], 11, "bold"),
            bg="#228B22",
            fg="white",
            relief=tk.FLAT,
            pady=8,
            padx=15,
            command=self._submit
        )
        self.submit_btn.pack(side=tk.RIGHT)

        problems_container = tk.Frame(content_frame, bg=THEME["bg"])
        problems_container.pack(fill=tk.BOTH, expand=True)

        problems_container.grid_rowconfigure(0, weight=1)

        for i in range(1, self.amount_of_problems + 1):
            col_index = i - 1
            problems_container.grid_columnconfigure(col_index, weight=1, uniform="problem_cols")

            card = tk.Frame(problems_container, bg=THEME["card_bg"], padx=10, pady=10, bd=1, relief=tk.SOLID)
            card.grid(row=0, column=col_index, sticky="nsew", padx=5, pady=5)

            top_frame = tk.Frame(card, bg=THEME["card_bg"])
            top_frame.pack(fill=tk.X, pady=(0, 5))

            prob_label = tk.Label(
                top_frame, 
                text=f"第 {i} 題", 
                font=(THEME["font_family"], 12, "bold"), 
                bg=THEME["card_bg"], 
                fg=THEME["text"]
            )
            prob_label.pack(side=tk.LEFT)

            btn = tk.Button(
                top_frame,
                text="選擇檔案",
                font=(THEME["font_family"], 9),
                command=lambda p=i: self._select_file(p)
            )
            btn.pack(side=tk.RIGHT)

            file_label = tk.Label(
                card, 
                text="未選擇檔案", 
                font=(THEME["font_family"], 9), 
                bg=THEME["card_bg"], 
                fg="gray",
                anchor="w"
            )
            file_label.pack(fill=tk.X, pady=(0, 5))
            self.file_name_labels[i] = file_label

            code_text = tk.Text(card, font=("Consolas", 9), wrap=tk.NONE)
            code_text.pack(fill=tk.BOTH, expand=True)
            code_text.config(state="disabled")
            self.code_texts[i] = code_text

    def _select_file(self, problem_id):
        filetypes = [
            ("Python files", "*.py"),
        ]

        try:
            selected = filedialog.askopenfilename(
                title=f"選擇第 {problem_id} 題檔案", filetypes=filetypes
            )
            if selected:
                self.fiels[problem_id] = selected
                filename = selected.split("/")[-1]
                self.file_name_labels[problem_id].config(text=f"檔案: {filename}", fg=THEME["text"])
                
                with open(selected, "r", encoding="utf-8") as f:
                    content = f.read()
                
                self.code_texts[problem_id].config(state="normal")
                self.code_texts[problem_id].delete("1.0", tk.END)
                self.code_texts[problem_id].insert(tk.END, content)
                self.code_texts[problem_id].config(state="disabled")

        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")
            return
        except Exception as e:
            messagebox.showerror("Error", f"無法讀取檔案: {e}")
            return

    def _submit(self):
        student_class = simpledialog.askstring("學生資訊", "請輸入班級(ex: 607)：", parent=self.root)
        if not student_class:
            return

        student_name = simpledialog.askstring("學生資訊", "請輸入姓名(ex: OOO)：", parent=self.root)
        if not student_name:
            return

        confirm = messagebox.askyesno("確認繳交？", "按下確認繳交後，就會送出檔案，送出後不得修改。")

        if confirm:
            try:
                data = {
                    "student_class": student_class,
                    "student_name": student_name,
                }

                files = {}
                opened_files = []
                
                for prob_id, filepath in self.fiels.items():
                    if filepath:
                        f = open(filepath, "rb")
                        opened_files.append(f)
                        files[f"prob_{prob_id}"] = (filepath.split("/")[-1], f, "text/plain")

                if not files:
                    messagebox.showwarning("警告", "請至少選擇一個檔案再繳交！")
                    return

                response = requests.post(self.url, data=data, files=files)
                
                for f in opened_files:
                    f.close()

                if response.status_code == 200:
                    print("上傳成功：", response.json())
                    messagebox.showinfo("成功", f"檔案已成功送至資料庫！\n班級：{data['student_class']}\n姓名：{data['student_name']}")
                else:
                    messagebox.showerror("錯誤", f"伺服器回應錯誤（代碼：{response.status_code}）\n>> {response.json()['message']}")
            except Exception as e:
                messagebox.showerror("錯誤", f"連線或上傳失敗：{e}")

        else:
            messagebox.showinfo("已取消", "準備好即可再次繳交！")
            return

if __name__ == "__main__":
    app = upload_app()
    app.root.mainloop()
