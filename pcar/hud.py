# hud.py
import tkinter as tk
import threading
import time

_hud_thread = None
_hud_label = None
_hud_win = None
_running = False


def _hud_loop(text, x, y, w, h):
    global _hud_label, _hud_win, _running

    root = tk.Tk()
    root.withdraw()

    _hud_win = tk.Toplevel(root)
    _hud_win.overrideredirect(True)
    _hud_win.attributes("-topmost", True)
    _hud_win.attributes("-alpha", 0.9)
    _hud_win.configure(bg="#222222")
    _hud_win.geometry(f"{w}x{h}+{x}+{y}")

    _hud_label = tk.Label(
        _hud_win,
        text=text,
        fg="white",
        bg="#222222",
        font=("Segoe UI", 12, "bold")
    )
    _hud_label.pack(expand=True, fill="both")

    # Make draggable
    def start(event):
        _hud_win.x = event.x
        _hud_win.y = event.y

    def drag(event):
        _hud_win.geometry(f"+{event.x_root - _hud_win.x}+{event.y_root - _hud_win.y}")

    _hud_win.bind("<Button-1>", start)
    _hud_win.bind("<B1-Motion>", drag)

    _running = True
    root.mainloop()
    _running = False


def show(text="HUD", x=100, y=100, w=180, h=60):
    global _hud_thread

    if _hud_thread and _hud_thread.is_alive():
        update(text)
        return

    _hud_thread = threading.Thread(
        target=_hud_loop,
        args=(text, x, y, w, h),
        daemon=True
    )
    _hud_thread.start()

    # Give Tk time to initialize
    time.sleep(0.1)


def update(text):
    if _hud_label:
        _hud_label.config(text=text)


def close():
    global _hud_win
    if _hud_win:
        _hud_win.destroy()
        _hud_win = None