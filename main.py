import tkinter as tk
from src.ui.app import FrontalLobeApp
from src.ui.styles import apply_styles

def main():
    root = tk.Tk()
    root.title("Frontal Lobe Prosthetics")
    root.geometry("800x600")
    
    apply_styles(root)
    
    app = FrontalLobeApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
