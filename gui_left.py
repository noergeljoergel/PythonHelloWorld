import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_left_panel(parent, tree, update_selected_list):
    """Erzeugt das linke Panel (Buttons, Eingabefelder, Checkboxen, Auswahlliste)."""

    left = ttk.Frame(parent, padding=10)

    # Button-Leiste
    btn_frame = ttk.Frame(left)
    btn_frame.pack(fill=X, pady=(0, 10))

    def start_search():
        checked = tree.get_checked_paths()
        if checked:
            ttk.dialogs.Messagebox.show_info("Suche gestartet", "Durchsuche:\n" + "\n".join(checked))
        else:
            ttk.dialogs.Messagebox.show_warning("Keine Auswahl", "Bitte mindestens einen Ordner auswählen.")

    def reset_all():
        tree.reset_all()
        sel_list.delete(0, tk.END)

    ttk.Button(btn_frame, text="Suchen", bootstyle=SUCCESS, command=start_search).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="Reset", bootstyle=DANGER, command=reset_all).pack(side=LEFT, padx=5)

    # Eingabefelder
    options_box = ttk.Labelframe(left, text="Optionen", padding=8)
    options_box.pack(fill=X)
    for i in range(4):
        ttk.Label(options_box, text=f"Feld {i+1}:").grid(row=i, column=0, sticky=W, pady=3)
        ttk.Entry(options_box).grid(row=i, column=1, sticky=EW, padx=5, pady=3)
    options_box.columnconfigure(1, weight=1)

    # Checkboxen
    chk_frame = ttk.Labelframe(left, text="Optionen (Checkboxen)", padding=8)
    chk_frame.pack(fill=X, pady=(10, 0))
    for i in range(4):
        ttk.Checkbutton(chk_frame, text=f"Option {i+1}").pack(anchor=W, pady=2)

    # Liste ausgewählter Ordner
    sel_frame = ttk.Labelframe(left, text="Ausgewählte Ordner", padding=8)
    sel_frame.pack(fill=BOTH, expand=True, pady=(10, 0))
    sel_list = tk.Listbox(sel_frame)
    sel_list.pack(fill=BOTH, expand=True)

    # Callback in update_selected_list
    def update_list_wrapper():
        sel_list.delete(0, tk.END)
        for path in tree.get_checked_paths():
            sel_list.insert(tk.END, path)
        update_selected_list()

    return left, update_list_wrapper, sel_list
