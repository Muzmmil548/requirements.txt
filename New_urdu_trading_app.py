import tkinter as tk
from tkinter import ttk, messagebox

class UrduScalpingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("اردو اسکیلپنگ چیک لسٹ ایپ")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f2f5")
        
        # RTL سپورٹ کے لیے فونٹ سیٹنگ
        self.font = ('Nafees Nastaleeq', 14)
        
        # نیویگیشن بار
        self.create_navbar()
        
        # تمام سیکشنز بنائیں
        self.create_sections()

    def create_navbar(self):
        navbar_frame = tk.Frame(self.root, bg="#1a73e8", height=50)
        navbar_frame.pack(fill="x", padx=10, pady=10)
        
        nav_items = ["ہوم", "لائیو", "چارٹ", "ٹاپ 50", "AI سگنلز"]
        for item in nav_items:
            btn = tk.Button(navbar_frame, text=item, font=self.font, 
                           bg="#1a73e8", fg="white", relief="flat")
            btn.pack(side="right", padx=10)

    def create_section(self, parent, title, buttons):
        frame = tk.Frame(parent, bg="white", padx=20, pady=20)
        frame.pack(fill="x", padx=10, pady=5)
        
        # عنوان
        title_label = tk.Label(frame, text=title, font=self.font, 
                              bg="white", justify="right")
        title_label.pack(anchor="e")
        
        # بٹنز
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(fill="x", pady=10)
        
        for btn_text in reversed(buttons):
            btn = tk.Button(btn_frame, text=btn_text, font=self.font,
                          bg="#1a73e8", fg="white", command=lambda t=btn_text: self.button_click(t))
            btn.pack(side="right", padx=5)

    def create_sections(self):
        sections = [
            ("ٹائپ", ["ٹاپ s", "AI Signass", "تمام AI سگنلز", "پیٹرنز"]),
            ("کوین سلیکٹر", ["ٹاپ 10"]),
            ("AI اسسٹنٹ سگنلز", ["خریدیں", "رکھیں", "فروخت کریں"]),
            ("چارٹ پیٹرنز", ["ہیڈ اینڈ شولڈرز", "ٹرائی اینگل", "ڈبل ٹاپ"])
        ]
        
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill="both", expand=True)
        
        for title, buttons in sections:
            self.create_section(main_frame, title, buttons)

    def button_click(self, text):
        messagebox.showinfo("اختیار", f"منتخب ہوا: {text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UrduScalpingApp(root)
    root.mainloop()
