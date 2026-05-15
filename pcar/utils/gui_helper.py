import os
import threading
import time

import tkinter as tk
from tkinter import messagebox, simpledialog

_root_win = None

_hud_thread = None
_hud_label = None
_hud_exit_button = None
_hud_win = None
_hud_shutting_down = False
_running = False


def _get_root():
    global _root_win
    if _root_win is None:
        _root_win = tk.Tk()
        _root_win.withdraw()
        _root_win.attributes("-topmost", True)
    return _root_win


def info(title, message):
    _get_root()
    messagebox.showinfo(title, message)


def ask_string(title, prompt):
    _get_root()
    return simpledialog.askstring(title, prompt)


def ask_yes_no(title, question):
    _get_root()
    return messagebox.askyesno(title, question)


def _kill_this_process():
    os._exit(0)


def _shutdown_with_message(delay_ms=1200):
    global _hud_shutting_down

    _hud_shutting_down = True

    if _hud_label:
        _hud_label.config(text="Shutting down...")

    if _hud_exit_button:
        _hud_exit_button.config(state="disabled", text="...")

    if _hud_win:
        _hud_win.after(delay_ms, _kill_this_process)


def _hud_loop(text, x, y, w, h):
    global _hud_label, _hud_exit_button, _hud_win, _hud_shutting_down, _running

    _hud_shutting_down = False

    root = tk.Tk()
    root.withdraw()

    _hud_win = tk.Toplevel(root)
    _hud_win.overrideredirect(True)
    _hud_win.attributes("-topmost", True)
    _hud_win.attributes("-alpha", 0.9)
    _hud_win.configure(bg="#222222")
    _hud_win.geometry(f"{w}x{h}+{x}+{y}")

    frame = tk.Frame(_hud_win, bg="#222222")
    frame.pack(expand=True, fill="both", padx=8, pady=0)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=0)

    _hud_label = tk.Label(
        frame,
        text=text,
        fg="white",
        bg="#222222",
        font=("Segoe UI", 10, "bold"),
        anchor="w",
        justify="left",
        wraplength=max(120, w - 150),
    )
    _hud_label.grid(row=0, column=0, sticky="nsew")

    _hud_exit_button = tk.Button(
        frame,
        text="EXIT",
        command=_shutdown_with_message,
        relief="flat",
        bd=0,
        highlightthickness=0,
        bg="#2b2b2b",
        fg="white",
        activebackground="#3a3a3a",
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        padx=14,
        pady=1,
        cursor="hand2",
    )
    _hud_exit_button.grid(row=0, column=1, sticky="e", padx=(8, 0))

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


def show_hud(text="HUD", x=400, y=1, w=500, h=40):
    global _hud_thread

    if _hud_thread and _hud_thread.is_alive():
        if not _hud_shutting_down:
            update_hud(text)
        return

    _hud_thread = threading.Thread(
        target=_hud_loop,
        args=(text, x, y, w, h),
        daemon=True,
    )
    _hud_thread.start()

    time.sleep(0.1)


def update_hud(text):
    if _hud_shutting_down:
        return

    if _hud_label:
        _hud_win.lift()
        _hud_label.config(text=text)


def close_hud():
    global _hud_win
    if _hud_win:
        _hud_win.destroy()
        _hud_win = None