import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

from gui_left import create_left_panel
from gui_right import create_right_panel


def main():
    app = ttk.Window(themename="superhero")
    app.overrideredirect(True)   # Standardrahmen/Titelbar entfernen
    app.geometry("1024x768")

    # Statusvariablen für Maximize/Restore
    app.is_maximized = False
    app.prev_geom = app.geometry()

    # --- Farben ---
    titlebar_bg = "#1E3A8A"       # Dunkelblau für Titelleiste
    titlebar_fg = "white"

    menubar_bg = "#2C3E50"        # Hellerer Blauton/Grau wie Treeview-Hintergrund
    menu_btn_bg = menubar_bg      # File/Help Buttons = heller Hintergrund
    menu_btn_fg = "#D0D0D0"       # etwas dunklerer Grauton für Text

    menu_active_bg = "#2563EB"    # Hellblau für Hover
    menu_active_fg = "white"

    # --- Titelleiste ---
    titlebar = tk.Frame(app, bg=titlebar_bg, relief="flat", bd=0, height=32)
    titlebar.pack(fill=X, side=TOP)

    title_label = tk.Label(
        titlebar, text="Duplicates",
        bg=titlebar_bg, fg=titlebar_fg, font=("Segoe UI", 10, "bold")
    )
    title_label.pack(side=LEFT, padx=10)

    # Fenster verschieben
    def start_move(event):
        app.x = event.x
        app.y = event.y

    def on_move(event):
        dx = event.x - app.x
        dy = event.y - app.y
        app.geometry(f"+{app.winfo_x() + dx}+{app.winfo_y() + dy}")

    titlebar.bind("<Button-1>", start_move)
    titlebar.bind("<B1-Motion>", on_move)
    title_label.bind("<Button-1>", start_move)
    title_label.bind("<B1-Motion>", on_move)

    # Rechts: Min/Max/Close Buttons
    def minimize():
        app.overrideredirect(False)
        app.iconify()
        app.after(10, lambda: app.overrideredirect(True))

    def maximize_restore():
        if not app.is_maximized:
            app.prev_geom = app.geometry()
            app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")
            app.is_maximized = True
            btn_max.config(text="🗗")
        else:
            app.geometry(app.prev_geom)
            app.is_maximized = False
            btn_max.config(text="🗖")

    def close_app():
        app.destroy()

    btn_close = tk.Button(
        titlebar, text="✕", bg=titlebar_bg, fg="white", bd=0, command=close_app,
        activebackground="red", activeforeground="white"
    )
    btn_close.pack(side=RIGHT, ipadx=6, ipady=2)

    btn_max = tk.Button(
        titlebar, text="🗖", bg=titlebar_bg, fg="white", bd=0, command=maximize_restore,
        activebackground=menu_active_bg, activeforeground=menu_active_fg
    )
    btn_max.pack(side=RIGHT, ipadx=6, ipady=2)

    btn_min = tk.Button(
        titlebar, text="—", bg=titlebar_bg, fg="white", bd=0, command=minimize,
        activebackground=menu_active_bg, activeforeground=menu_active_fg
    )
    btn_min.pack(side=RIGHT, ipadx=6, ipady=2)

    # --- Menüleiste (unter Titelleiste) ---
    menubar_frame = tk.Frame(app, bg=menubar_bg, height=28)
    menubar_frame.pack(fill=X, side=TOP)

    # File-Menü
    btn_file = tk.Menubutton(
        menubar_frame, text="File",
        bg=menu_btn_bg, fg=menu_btn_fg,
        activebackground=menu_active_bg, activeforeground=menu_active_fg,
        bd=0, padx=10
    )
    file_menu = tk.Menu(
        btn_file, tearoff=0,
        bg=menubar_bg, fg=menu_btn_fg,
        activebackground=menu_active_bg, activeforeground=menu_active_fg,
        borderwidth=0
    )
    file_menu.add_command(label="Exit", command=app.destroy)
    btn_file.config(menu=file_menu)
    btn_file.pack(side=LEFT, padx=5)

    # Help-Menü
    btn_help = tk.Menubutton(
        menubar_frame, text="Help",
        bg=menu_btn_bg, fg=menu_btn_fg,
        activebackground=menu_active_bg, activeforeground=menu_active_fg,
        bd=0, padx=10
    )
    help_menu = tk.Menu(
        btn_help, tearoff=0,
        bg=menubar_bg, fg=menu_btn_fg,
        activebackground=menu_active_bg, activeforeground=menu_active_fg,
        borderwidth=0
    )
    help_menu.add_command(
        label="About",
        command=lambda: messagebox.showinfo("About", "Python Duplicates\nmit Custom Titlebar")
    )
    btn_help.config(menu=help_menu)
    btn_help.pack(side=LEFT, padx=5)

    # --- PanedWindow mit Links/Rechts ---
    panes = ttk.Panedwindow(app, orient=HORIZONTAL)
    panes.pack(fill=BOTH, expand=True)

    dummy_update = lambda: None
    right_panel, tree = create_right_panel(panes, dummy_update)
    left_panel, update_left_list, sel_list = create_left_panel(panes, tree, dummy_update)

    tree.callback = update_left_list

    panes.add(left_panel, weight=1)
    panes.add(right_panel, weight=3)

    app.mainloop()


if __name__ == "__main__":
    main()
