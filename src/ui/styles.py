from tkinter import ttk

def apply_styles(root):
    style = ttk.Style(root)
    style.theme_use('clam') # 'clam' is usually a good base for custom styling
    
    # Colors
    bg_color = "#2E3440"
    fg_color = "#D8DEE9"
    accent_color = "#88C0D0"
    button_bg = "#4C566A"
    button_fg = "#ECEFF4"
    
    root.configure(bg=bg_color)
    
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Helvetica", 12))
    style.configure("TButton", background=button_bg, foreground=button_fg, font=("Helvetica", 11), padding=10, borderwidth=0)
    style.map("TButton", background=[('active', accent_color)])
    
    # Custom classes
    style.configure("Title.TLabel", font=("Helvetica", 24, "bold"), foreground=accent_color)
    style.configure("Reward.TLabel", font=("Helvetica", 18, "italic"), foreground="#A3BE8C")
