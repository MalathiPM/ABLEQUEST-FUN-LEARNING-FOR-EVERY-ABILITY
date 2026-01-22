import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, random
from datetime import datetime
from games import GameEngine

TEACHER_PASSWORD = "admin"

class AbleQuest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AbleQuest")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#F0F4F8") 
        
        self.current_student = ""
        
        self.init_db()
        self.games = GameEngine(self)
        
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0, bg="#F0F4F8")
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.stars = []
        self.init_particles()
        
        self.colors = ["RED", "GREEN", "BLUE", "YELLOW", "ORANGE", "PURPLE", "PINK", "CYAN"]
        self.phonics = {
        "A": "🍎 Apple", "B": "🐻 Bear", "C": "🐱 Cat", "D": "🐶 Dog",
        "E": "🥚 Egg", "F": "🐟 Fish", "G": "🍇 Grapes", "H": "🏠 House",
        "I": "🍦 Ice-Cream", "J": "🏺 Jar", "K": "🪁 Kite", "L": "🦁 Lion",
        "M": "🐒 Monkey", "N": "☁️ Nose", "O": "🐙 Octopus", "P": "🐧 Penguin",
        "Q": "👑 Queen", "R": "🚀 Rocket", "S": "☀️ Sun", "T": "🐯 Tiger",
        "U": "☂️ Umbrella", "V": "🎻 Violin", "W": "🐳 Whale", "X": "🎷 Xylophone",
        "Y": "🧶 Yo-Yo", "Z": "🦓 Zebra"
}
        self.emotions = {
            "😊": "Happy", "😢": "Sad", "😠": "Angry", "😯": "Surprised",
            "😴": "Sleepy", "😨": "Scared", "😘": "Love"
        }
        self.hygiene_steps = ["Wet Hands", "Apply Soap", "Scrub", "Rinse", "Dry"]
        self.clock_times = [
        "12:00", "12:30", "1:00", "1:30", "2:00", "2:30", 
        "3:00", "3:30", "4:00", "4:30", "5:00", "5:30", 
        "6:00", "6:30", "7:00", "7:30", "8:00", "8:30", 
        "9:00", "9:30", "10:00", "10:30", "11:00", "11:30"]
        
        self.social_scenarios = [
            ("Meeting a friend", "Hello!"),
            ("It is the morning", "Good morning!"),
            ("Someone gives you a gift", "Thank you!"),
            ("Asking for help", "Please!"),
            ("Leaving the classroom", "Goodbye!"),
            ("It is the afternoon", "Good afternoon!"),
            ("It is night time", "Goodnight!"),
            ("You bumped into someone", "Sorry!"),
            ("Someone says 'How are you?'", "I am fine!"),
            ("Sharing a toy", "You're welcome!"),
            ("Someone asks for your name", "My name is..."),
            ("Meeting a new teacher", "Nice to meet you!")
        ]
        
        self.home()
        self.animate_particles()

    def init_db(self):
        self.conn = sqlite3.connect("ablequest.db")
        self.conn.execute("CREATE TABLE IF NOT EXISTS progress(student TEXT, activity TEXT, score INTEGER, timestamp TEXT)")
        self.conn.commit()

    def save(self, activity, score):
        if self.current_student:
            self.conn.execute("INSERT INTO progress VALUES (?, ?, ?, ?)",
                (self.current_student, activity, score, datetime.now().strftime("%Y-%m-%d %H:%M")))
            self.conn.commit()

    def init_particles(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        for _ in range(30):
            x, y = random.randint(0, screen_w), random.randint(0, screen_h)
            size = random.randint(12, 24)
            star = self.bg_canvas.create_text(x, y, text="✨", font=("Arial", size), fill="#CBD5E1")
            speed = random.uniform(0.4, 1.2)
            self.stars.append([star, speed, y])

    def animate_particles(self):
        screen_w = self.root.winfo_screenwidth()
        for s_data in self.stars:
            self.bg_canvas.move(s_data[0], s_data[1], 0)
            coords = self.bg_canvas.coords(s_data[0])
            if coords and coords[0] > screen_w:
                self.bg_canvas.coords(s_data[0], -20, s_data[2])
        self.root.after(50, self.animate_particles)

    def clear(self):
        for w in self.root.winfo_children():
            if w != self.bg_canvas: w.destroy()

    def create_gradient_header(self, title, subtitle=""):
        f = tk.Frame(self.root, bg="#1E3A8A", height=180)
        f.pack(fill=tk.X)
        tk.Label(f, text=title, font=("Segoe UI", 48, "bold"), bg="#1E3A8A", fg="white").pack(pady=(30, 0))
        if subtitle:
            tk.Label(f, text=subtitle, font=("Segoe UI", 16), bg="#1E3A8A", fg="#BFDBFE").pack(pady=(0, 20))

    def create_btn(self, parent, text, command, color="#3B82F6", width=22):
        btn = tk.Button(parent, text=text, command=command, font=("Segoe UI", 18, "bold"),
                        bg=color, fg="white", relief=tk.FLAT, bd=0, width=width, height=2, cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.config(bg="#E10D0D"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    def home(self):
        self.current_student = ""
        self.clear()
        self.create_gradient_header("ABLEQUEST", "Fun Learning for Every Ability")
        f = tk.Frame(self.root, bg="#F0F4F8")
        f.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.create_btn(f, "👦 STUDENT PORTAL", self.student_select, "#3B82F6", 25).pack(pady=20)
        self.create_btn(f, "👩‍🏫 TEACHER PORTAL", self.password_prompt, "#10B981", 25).pack(pady=20)

    def student_select(self):
        self.clear()
        self.create_gradient_header("Select the Student")
        f = tk.Frame(self.root, bg="#F0F4F8")
        f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        for n, c in [("Madhava", "#4DA47E"), ("Arjun", "#C8D428"), ("Nakul", "#1C1D5F")]:
            self.create_btn(f, f"👤 {n}", lambda name=n: self.open_student(name), c, 20).pack(pady=15)
        self.create_btn(self.root, "🏠 BACK", self.home, "#EF4444", 15).pack(side=tk.BOTTOM, pady=50)

    def open_student(self, name):
        self.current_student = name
        self.dashboard()

    def dashboard(self):
        self.clear()
        self.create_gradient_header(f"🌟 Let's Learn with Fun", f"Welcome back, {self.current_student}!")
        main_f = tk.Frame(self.root, bg="#F0F4F8")
        main_f.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        
        grid = tk.Frame(main_f, bg="#F0F4F8")
        grid.pack()
        activities = [
            ("🧼 Hygiene", self.games.hygiene_game, "#DD27F5", 0, 0),
            ("🕒 Time", self.games.time_game, "#F59E0B", 0, 1),
            ("😊 Emotions", self.games.emotion_game, "#10B981", 1, 0),
            ("👋 Greetings", self.games.greeting_game, "#9F7CF1", 1, 1),
            ("🎨 Colors", self.games.color_game, "#156DFA", 2, 0),
            ("🔤 Phonics", self.games.letter_game, "#06B6D4", 2, 1)
        ]
        for text, cmd, clr, r, c in activities:
            self.create_btn(grid, text, cmd, clr, 18).grid(row=r, column=c, padx=15, pady=10)
        self.create_btn(grid, "❌ Tic Tac Toe", self.games.tictactoe_game, "#4D895C", 38).grid(row=3, column=0, columnspan=2, pady=15)
        self.create_btn(self.root, "🚪 LOGOUT", self.home, "#64748B", 18).pack(side=tk.BOTTOM, pady=40)

    def password_prompt(self):
        win = tk.Toplevel(self.root)
        win.geometry("400x300")
        win.configure(bg="white")
        tk.Label(win, text="🔐 Teacher Access", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=20)
        e = tk.Entry(win, show="*", font=("Arial", 18), width=15, justify="center")
        e.pack(pady=10)
        e.focus()
        def check():
            if e.get() == TEACHER_PASSWORD:
                win.destroy()
                self.teacher_dashboard()
            else: messagebox.showerror("Denied", "Incorrect Password")
        self.create_btn(win, "LOGIN", check, "#10B981", 15).pack(pady=20)

    def teacher_dashboard(self):
        self.clear()
        self.create_gradient_header("📊 Student Progress Logs")
        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        cols = ("student", "activity", "score", "time")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col.upper()); tree.column(col, anchor=tk.CENTER)
        cursor = self.conn.execute("SELECT * FROM progress ORDER BY timestamp DESC")
        for row in cursor.fetchall(): tree.insert("", tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True)
        nav = tk.Frame(self.root, bg="#F0F4F8")
        nav.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        self.create_btn(nav, "🗑️ CLEAR DATA", self.reset_db, "#F59E0B", 20).pack(side=tk.LEFT, padx=100)
        self.create_btn(nav, "🏠 HOME", self.home, "#EF4444", 20).pack(side=tk.RIGHT, padx=100)

    def reset_db(self):
        if messagebox.askyesno("Reset", "Delete all records?"):
            self.conn.execute("DELETE FROM progress"); self.conn.commit(); self.teacher_dashboard()

    def run(self):
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.mainloop()

if __name__ == "__main__":
    app = AbleQuest(); app.run()