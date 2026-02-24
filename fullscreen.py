import tkinter as tk

def make_fullscreen(window):
    try:
        window.state('zoomed')   # Windows mate
    except:
        pass

    # Mac fallback
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
