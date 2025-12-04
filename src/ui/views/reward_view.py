import tkinter as tk
from tkinter import ttk
import random

class RewardView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        container = ttk.Frame(self)
        container.grid(row=0, column=0)
        
        ttk.Label(container, text=self.app.loc.get("great_job"), font=("Helvetica", 18), wraplength=600).pack(pady=20)
        ttk.Label(container, text=self.app.loc.get("reward_desc"), font=("Helvetica", 12), wraplength=600).pack(pady=20)
        ttk.Label(container, text=self.app.loc.get("earned_it"), font=("Helvetica", 18), wraplength=600).pack(pady=20)
        
        ttk.Button(container, text=self.app.loc.get("ready_again"), command=self._next).pack(pady=20)

    def _next(self):
        self.app.show_focus_view()
