import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import os


def init_db():
    conn = sqlite3.connect('home_vault.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, budget REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses 
                 (username TEXT, item TEXT, cost REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, task TEXT, assigned_to TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

class EliteHomeManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Elite Vault | Terminal")
        self.geometry("1100x650")
        self.resizable(False, False)
        
        self.current_user = None
        self.user_budget = 0.0
        
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.show_login_page()

    def on_closing(self):
        try:
            plt.close('all')
            self.quit()
            self.destroy()
        except:
            pass

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    
    def show_login_page(self):
        self.clear_screen()
        
        
        possible_names = ["background.png"]
        bg_path = None
        for name in possible_names:
            p = os.path.join(os.path.dirname(__file__), name)
            if os.path.exists(p):
                bg_path = p
                break
        
        if bg_path:
            img = Image.open(bg_path)
            self.bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(1100, 650))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.configure(fg_color="#0a0a0a")
            self.bg_label = self 

        
        
    
        ctk.CTkLabel(self.bg_label, text="💎", font=("Arial", 100), fg_color="transparent").place(relx=0.28, rely=0.35, anchor="center")
        ctk.CTkLabel(self.bg_label, text="ELITE VAULT", font=("Century Gothic", 42, "bold"), text_color="#d4af37", fg_color="transparent").place(relx=0.28, rely=0.52, anchor="center")
        ctk.CTkLabel(self.bg_label, text="SYSTEM SECURED", font=("Century Gothic", 14, "bold"), text_color="#ffffff", fg_color="transparent").place(relx=0.28, rely=0.60, anchor="center")
        
        
        ctk.CTkLabel(self.bg_label, text="AUTHORIZED ACCESS", font=("Century Gothic", 28, "bold"), text_color="white", fg_color="transparent").place(relx=0.72, rely=0.20, anchor="center")
        
        
        self.u_entry = ctk.CTkEntry(self.bg_label, placeholder_text="Username", width=320, height=50, 
                                    border_color="#d4af37", fg_color="#121212", text_color="white", corner_radius=10)
        self.u_entry.place(relx=0.72, rely=0.38, anchor="center")
        
        self.p_entry = ctk.CTkEntry(self.bg_label, placeholder_text="Password", show="*", width=320, height=50, 
                                    border_color="#d4af37", fg_color="#121212", text_color="white", corner_radius=10)
        self.p_entry.place(relx=0.72, rely=0.51, anchor="center")
        
        btn_login = ctk.CTkButton(self.bg_label, text="INITIALIZE LOGIN", command=self.login_logic, width=320, height=55, 
                                  fg_color="#d4af37", text_color="black", font=("Century Gothic", 16, "bold"), 
                                  hover_color="#b8962e", corner_radius=10)
        btn_login.place(relx=0.72, rely=0.70, anchor="center")
        
        ctk.CTkButton(self.bg_label, text="Request New Account", font=("Century Gothic", 13), fg_color="transparent", 
                      text_color="#d4af37", command=self.show_register_page, hover=False).place(relx=0.72, rely=0.84, anchor="center")

    def show_register_page(self):
        self.clear_screen()
        self.configure(fg_color="#0a0a0a")
        reg_container = ctk.CTkFrame(self, width=500, height=550, corner_radius=20, fg_color="#1a1a1a", border_width=1, border_color="#d4af37")
        reg_container.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(reg_container, text="Registration Suite", font=("Century Gothic", 24, "bold"), text_color="#d4af37").pack(pady=30)
        u_reg = ctk.CTkEntry(reg_container, placeholder_text="Set Username", width=350, height=45)
        u_reg.pack(pady=10)
        p_reg = ctk.CTkEntry(reg_container, placeholder_text="Set Password", show="*", width=350, height=45)
        p_reg.pack(pady=10)
        b_reg = ctk.CTkEntry(reg_container, placeholder_text="Weekly Budget ($)", width=350, height=45)
        b_reg.pack(pady=10)

        def save_user():
            try:
                conn = sqlite3.connect('home_vault.db')
                c = conn.cursor()
                c.execute("INSERT INTO users VALUES (?, ?, ?)", (u_reg.get(), p_reg.get(), float(b_reg.get())))
                conn.commit()
                conn.close()
                self.show_login_page()
            except: messagebox.showerror("Error", "Username exists.")

        ctk.CTkButton(reg_container, text="ACTIVATE ACCOUNT", command=save_user, fg_color="#d4af37", text_color="black", width=350, height=45).pack(pady=20)
        ctk.CTkButton(reg_container, text="Back to Login", command=self.show_login_page, fg_color="transparent").pack()

    def show_dashboard(self):
        self.clear_screen()
        self.configure(fg_color="#0a0a0a")
        
        conn = sqlite3.connect('home_vault.db')
        c = conn.cursor()
        c.execute("SELECT SUM(cost) FROM expenses WHERE username=?", (self.current_user,))
        total_spent = c.fetchone()[0] or 0
        c.execute("SELECT COUNT(*) FROM tasks WHERE username=? AND status='Pending'", (self.current_user,))
        pending_count = c.fetchone()[0] or 0
        c.execute("SELECT COUNT(*) FROM tasks WHERE username=? AND status='Done'", (self.current_user,))
        completed_count = c.fetchone()[0] or 0
        conn.close()

        status_color = "#2b0000" if total_spent > self.user_budget else "#0f0f0f"

        side_panel = ctk.CTkScrollableFrame(self, width=320, corner_radius=0, fg_color="#070707")
        side_panel.pack(side="left", fill="y", padx=5, pady=5)

        ctk.CTkLabel(side_panel, text="FINANCE MODULE", font=("Century Gothic", 16, "bold"), text_color="#d4af37").pack(pady=20)
        e_item = ctk.CTkEntry(side_panel, placeholder_text="Expense Item")
        e_item.pack(pady=5)
        e_cost = ctk.CTkEntry(side_panel, placeholder_text="Amount ($)")
        e_cost.pack(pady=5)
        
        def add_e():
            conn = sqlite3.connect('home_vault.db')
            c = conn.cursor()
            c.execute("INSERT INTO expenses VALUES (?, ?, ?)", (self.current_user, e_item.get(), float(e_cost.get())))
            conn.commit()
            self.show_dashboard()

        ctk.CTkButton(side_panel, text="Register Expense", command=add_e, fg_color="#d4af37", text_color="black").pack(pady=10)
        
        def reset_e():
            if messagebox.askyesno("Confirm", "Purge all weekly records?"):
                conn = sqlite3.connect('home_vault.db')
                c = conn.cursor()
                c.execute("DELETE FROM expenses WHERE username=?", (self.current_user,))
                conn.commit()
                self.show_dashboard()
        
        ctk.CTkButton(side_panel, text="Reset Financials", command=reset_e, fg_color="#e74c3c").pack(pady=5)

        ctk.CTkLabel(side_panel, text="────────────────", text_color="#222222").pack(pady=15)
        
        ctk.CTkLabel(side_panel, text="TASK MODULE", font=("Century Gothic", 16, "bold"), text_color="#3498db").pack(pady=10)
        t_desc = ctk.CTkEntry(side_panel, placeholder_text="Task Detail")
        t_desc.pack(pady=5)
        t_assign = ctk.CTkEntry(side_panel, placeholder_text="Assigned User")
        t_assign.pack(pady=5)

        def add_t():
            conn = sqlite3.connect('home_vault.db')
            c = conn.cursor()
            c.execute("INSERT INTO tasks (username, task, assigned_to, status) VALUES (?, ?, ?, 'Pending')", (self.current_user, t_desc.get(), t_assign.get()))
            conn.commit()
            self.show_dashboard()

        ctk.CTkButton(side_panel, text="Deploy Task", command=add_t, fg_color="#3498db").pack(pady=10)
        ctk.CTkButton(side_panel, text="SECURE LOGOUT", command=self.show_login_page, fg_color="transparent", border_width=1, border_color="#333333").pack(pady=30)

        display_area = ctk.CTkFrame(self, fg_color=status_color, corner_radius=15)
        display_area.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        stats_frame = ctk.CTkFrame(display_area, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20, padx=20)

        for text, clr in [(f"Active\n{pending_count}", "#3498db"), (f"Resolved\n{completed_count}", "#8e44ad"), (f"Spent\n${total_spent}", "#27ae60")]:
            card = ctk.CTkFrame(stats_frame, fg_color="#141414", width=200, height=110, border_width=1, border_color=clr)
            card.pack(side="left", padx=10, expand=True)
            ctk.CTkLabel(card, text=text, font=("Century Gothic", 18, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        task_list_frame = ctk.CTkScrollableFrame(display_area, label_text="System Log", height=280, fg_color="#0a0a0a")
        task_list_frame.pack(fill="x", padx=20, pady=10)

        conn = sqlite3.connect('home_vault.db')
        c = conn.cursor()
        c.execute("SELECT id, task, assigned_to, status FROM tasks WHERE username=?", (self.current_user,))
        for tid, tname, tto, tstat in c.fetchall():
            row = ctk.CTkFrame(task_list_frame, fg_color="#181818")
            row.pack(fill="x", pady=3)
            lbl = f"» {tname} — Target: {tto}"
            ctk.CTkLabel(row, text=lbl, width=400, anchor="w", font=("Century Gothic", 13), text_color="white" if tstat=="Pending" else "gray").pack(side="left", padx=15)
            
            def del_t(id=tid):
                conn = sqlite3.connect('home_vault.db')
                c = conn.cursor()
                c.execute("DELETE FROM tasks WHERE id=?", (id,))
                conn.commit()
                self.show_dashboard()
            ctk.CTkButton(row, text="🗑", width=35, fg_color="#c0392b", command=del_t).pack(side="right", padx=5)

            if tstat == "Pending":
                def set_done(id=tid):
                    conn = sqlite3.connect('home_vault.db')
                    c = conn.cursor()
                    c.execute("UPDATE tasks SET status='Done' WHERE id=?", (id,))
                    conn.commit()
                    self.show_dashboard()
                ctk.CTkButton(row, text="RESOLVE", width=80, command=set_done, fg_color="#27ae60", font=("Century Gothic", 11, "bold")).pack(side="right", padx=5)

        chart_frame = ctk.CTkFrame(display_area, corner_radius=15, fg_color="#141414")
        chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.render_pie_chart(chart_frame)

    def render_pie_chart(self, frame):
        conn = sqlite3.connect('home_vault.db')
        c = conn.cursor()
        c.execute("SELECT item, cost FROM expenses WHERE username=?", (self.current_user,))
        data = c.fetchall()
        if not data: return
        labels, costs = [r[0] for r in data], [r[1] for r in data]
        fig, ax = plt.subplots(figsize=(4, 3), dpi=80)
        fig.patch.set_facecolor('#141414')
        ax.pie(costs, labels=labels, autopct='%1.1f%%', textprops={'color':"w"})
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def login_logic(self):
        conn = sqlite3.connect('home_vault.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (self.u_entry.get(), self.p_entry.get()))
        user = c.fetchone()
        if user:
            self.current_user, self.user_budget = user[0], user[2]
            self.show_dashboard()
        else: messagebox.showerror("Denied", "Identity Verification Failed.")

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = EliteHomeManager()
    app.mainloop()