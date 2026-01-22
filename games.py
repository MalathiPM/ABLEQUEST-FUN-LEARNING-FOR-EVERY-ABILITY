import tkinter as tk
from tkinter import messagebox
import random

class GameEngine:
    def __init__(self, app):
        self.app = app

    def add_nav(self):
        nav = tk.Frame(self.app.root, bg="#F0F4F8")
        nav.pack(side=tk.BOTTOM, pady=40)
        tk.Button(nav, text="🔙 BACK", command=self.app.dashboard, bg="#64748B", fg="white",
                 font=("Segoe UI", 16, "bold"), bd=0, width=12, height=2, cursor="hand2").pack(side=tk.LEFT, padx=10)
        tk.Button(nav, text="🏠 HOME", command=self.app.home, bg="#EF4444", fg="white",
                 font=("Segoe UI", 16, "bold"), bd=0, width=12, height=2, cursor="hand2").pack(side=tk.LEFT, padx=10)

    def hygiene_game(self):
        self.app.clear()
        self.app.create_gradient_header("🧼 Hygiene Trainer")
        f = tk.Frame(self.app.root, bg="#F0F4F8")
        f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        steps = self.app.hygiene_steps
        self.curr_h_step = 0
        label = tk.Label(f, text=f"Step 1: {steps[0]}", font=("Segoe UI", 40, "bold"), bg="#F0F4F8", fg="#3B82F6")
        label.pack(pady=40)
        def next_s():
            self.curr_h_step += 1
            if self.curr_h_step < len(steps):
                label.config(text=f"Step {self.curr_h_step+1}: {steps[self.curr_h_step]}")
            else:
                messagebox.showinfo("Success", "Hands are clean! ✨")
                self.app.save("Hygiene", 100); self.app.dashboard()
        tk.Button(f, text="DONE ✅", command=next_s, bg="#10B981", fg="white", font=("Segoe UI", 24, "bold"), width=15, height=2).pack(pady=20)
        self.add_nav()

    def time_game(self):
        self.app.clear()
        self.app.create_gradient_header("🕒 Time Teller")
        target = random.choice(self.app.clock_times)
        f = tk.Frame(self.app.root, bg="#F0F4F8")
        f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        clocks = {
    "12:00":"🕛", "12:30":"🕛", "1:00":"🕐", "1:30":"🕐",
    "2:00":"🕑", "2:30":"🕑", "3:00":"🕒", "3:30":"🕒",
    "4:00":"🕓", "4:30":"🕓", "5:00":"🕔", "5:30":"🕔",
    "6:00":"🕕", "6:30":"🕕", "7:00":"🕖", "7:30":"🕖",
    "8:00":"🕗", "8:30":"🕗", "9:00":"🕘", "9:30":"🕘",
    "10:00":"🕙", "10:30":"🕙", "11:00":"🕚", "11:30":"🕚"
}
        
        tk.Label(f, text=clocks[target], font=("Arial", 150), bg="#F0F4F8").pack()
        tk.Label(f, text="Type the time (e.g., 3 or 3:00)", font=("Segoe UI", 20), bg="#F0F4F8", fg="#64748B").pack(pady=10)
        
        entry = tk.Entry(f, font=("Segoe UI", 30), width=10, justify="center", bd=2)
        entry.pack(pady=20)
        entry.focus()
        
        def check():
            user_input = entry.get().strip()
            # This allows "3" to match "3:00" or "12" to match "12:00"
            hour_only = target.split(":")[0]
            
            if user_input == target or user_input == hour_only:
                messagebox.showinfo("Correct!", f"🌟 Great job! It is {target}")
                self.app.save("Time", 100)
                self.time_game() # This refreshes the screen with a new time
            else:
                messagebox.showwarning("Try Again", f"Not quite! Look at where the small hand is pointing.")

        def get_hint():
            entry.delete(0, tk.END)
            entry.insert(0, target.split(":")[0])

        btn_f = tk.Frame(f, bg="#F0F4F8")
        btn_f.pack(pady=10)
        
        tk.Button(btn_f, text="CHECK ✅", command=check, bg="#F59E0B", fg="white", 
                  font=("Segoe UI", 20, "bold"), width=10, cursor="hand2").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_f, text="HINT 💡", command=get_hint, bg="#64748B", fg="white", 
                  font=("Segoe UI", 20, "bold"), width=10, cursor="hand2").pack(side=tk.LEFT, padx=10)
        
        self.add_nav()
    def emotion_game(self):
        self.app.clear()
        self.app.create_gradient_header("😊 Feelings")
        emo, name = random.choice(list(self.app.emotions.items()))
        f = tk.Frame(self.app.root, bg="#F0F4F8")
        f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(f, text=emo, font=("Arial", 150), bg="#F0F4F8").pack()
        opts = random.sample(list(self.app.emotions.values()), 3)
        if name not in opts: opts[0] = name
        random.shuffle(opts)
        for o in opts:
            tk.Button(f, text=o, font=("Segoe UI", 20, "bold"), width=15, bg="#8B5CF6", fg="white",
                      command=lambda x=o: self.check_emo(x, name)).pack(pady=5)
        self.add_nav()

    def check_emo(self, guess, actual):
        if guess == actual:
            messagebox.showinfo("Yes!", f"That is {actual}!"); self.app.save("Emotions", 100); self.emotion_game()
        else: messagebox.showerror("No", f"That was {actual}")

    def greeting_game(self):
        self.app.clear()
        self.app.create_gradient_header("👋 Social Skills")
        scenario_text, target_greeting = random.choice(self.app.social_scenarios)
        f = tk.Frame(self.app.root, bg="#F0F4F8")
        f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(f, text=f"Scenario: {scenario_text}", font=("Segoe UI", 28, "italic"), bg="#F0F4F8", fg="#1E3A8A").pack(pady=10)
        tk.Label(f, text="What do you say?", font=("Segoe UI", 36, "bold"), bg="#F0F4F8").pack(pady=10)
        entry = tk.Entry(f, font=("Segoe UI", 24), width=20, justify="center")
        entry.pack(pady=20); entry.focus()
        def check():
            user_input = entry.get().strip().lower()
            clean_target = target_greeting.lower().replace("!", "").replace(".", "").replace("?", "")
            if user_input in clean_target:
                messagebox.showinfo("Nice!", f"Perfect: {target_greeting}")
                self.app.save("Greetings", 100); self.greeting_game()
            else:
                messagebox.showinfo("Tip", f"Try saying: {target_greeting}")
        def get_hint():
            entry.delete(0, tk.END); entry.insert(0, target_greeting[0])
        btn_f = tk.Frame(f, bg="#F0F4F8")
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="SPEAK 🗣️", command=check, bg="#10B981", fg="white", font=("Segoe UI", 20, "bold"), width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_f, text="HINT 💡", command=get_hint, bg="#F59E0B", fg="white", font=("Segoe UI", 20, "bold"), width=12).pack(side=tk.LEFT, padx=10)
        self.add_nav()

    def color_game(self):
        self.app.clear()
        self.app.create_gradient_header("🎨 Colors")
        target = random.choice(self.app.colors)
        f = tk.Frame(self.app.root, bg="#F0F4F8")
        f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(f, text=f"Click {target}", font=("Segoe UI", 36, "bold"), bg="#F0F4F8").pack(pady=30)
        cmap = {"RED":"#EF4444","GREEN":"#10B981","BLUE":"#3B82F6","YELLOW":"#F59E0B",
                "ORANGE":"#F97316","PURPLE":"#8B5CF6","PINK":"#EC4899","CYAN":"#06B6D4"}
        opts = random.sample(self.app.colors, 4)
        if target not in opts: opts[0] = target
        random.shuffle(opts)
        for c in opts:
            tk.Button(f, bg=cmap[c], width=10, height=4, command=lambda x=c: self.check_col(x, target)).pack(side=tk.LEFT, padx=10)
        self.add_nav()

    def check_col(self, guess, actual):
        if guess == actual: self.app.save("Colors", 100); self.color_game()
        else: messagebox.showwarning("Oops", f"That was {guess}")

    def letter_game(self):
        self.app.clear()
        self.app.create_gradient_header("🔤 Phonics")
        char, val = random.choice(list(self.app.phonics.items()))
        emoji, word = val.split()
        f = tk.Frame(self.app.root, bg="#F0F4F8")
        f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(f, text=emoji, font=("Arial", 150), bg="#F0F4F8").pack()
        entry = tk.Entry(f, font=("Segoe UI", 24), width=15, justify="center")
        entry.pack(pady=20)
        entry.focus()
        
        def check():
            user_input = entry.get().strip().lower()
            if user_input == word.lower():
                messagebox.showinfo("Correct!", f"Well done! {emoji} is for {word}!")
                self.app.save("Phonics", 100)
                self.letter_game()
            else:
                messagebox.showwarning("Try Again", f"That's not quite right. Hint: It starts with '{char}'")
        
        tk.Button(f, text="CHECK ✅", command=check, bg="#06B6D4", fg="white", 
                  font=("Segoe UI", 20, "bold"), width=12).pack(pady=10)
        self.add_nav()

    def tictactoe_game(self):
        self.app.clear()
        self.app.create_gradient_header("❌ Tic Tac Toe")
        f = tk.Frame(self.app.root, bg="#F0F4F8")
        f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.board = [""] * 9; self.btns = []
        def check_win():
            for a,b,c in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
                if self.board[a] == self.board[b] == self.board[c] != "": return True
            return False
        def click(i):
            if self.board[i] == "":
                self.board[i] = "X"; self.btns[i].config(text="❌", state="disabled")
                if check_win():
                    messagebox.showinfo("Win!", "You won! 🌟"); self.app.save("TicTacToe", 100); self.tictactoe_game()
                elif "" not in self.board:
                    messagebox.showinfo("Tie", "Draw!"); self.tictactoe_game()
                else:
                    move = random.choice([idx for idx,v in enumerate(self.board) if v==""])
                    self.board[move] = "O"; self.btns[move].config(text="⭕", state="disabled")
                    if check_win(): messagebox.showinfo("AI", "AI Won!"); self.tictactoe_game()
        for i in range(9):
            b = tk.Button(f, text="", font=("Arial", 30, "bold"), width=5, height=2, command=lambda x=i: click(x))
            b.grid(row=i//3, column=i%3, padx=5, pady=5); self.btns.append(b)
        self.add_nav()