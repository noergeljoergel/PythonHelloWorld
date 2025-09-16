import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from file_tree import CheckBoxTree
from utils import get_root_paths, list_subdirs

def create_right_panel(parent, update_selected_list):
    """Erzeugt das rechte Panel mit dem Verzeichnisbaum."""
    right = ttk.Frame(parent, padding=10)

    tree = CheckBoxTree(right, show="tree", callback=update_selected_list)
    tree.pack(fill=BOTH, expand=True, side=LEFT)
    scroll = ttk.Scrollbar(right, orient=VERTICAL, command=tree.yview, bootstyle="round")
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)

    # Root-Knoten
    for root_path in get_root_paths():
        node_id = tree.insert("", "end", text=root_path, values=(root_path,))
        tree.insert(node_id, "end", text="...")

    def on_open(event):
        node_id = tree.focus()
        path = tree.item(node_id, "values")[0]
        for child in tree.get_children(node_id):
            if tree.item(child, "text") == "...":
                tree.delete(child)
        for sub in list_subdirs(path):
            child_path = os.path.join(path, sub)
            child_id = tree.insert(node_id, "end", text=sub, values=(child_path,))
            tree.insert(child_id, "end", text="...")

    tree.bind("<<TreeviewOpen>>", on_open)

    return right, tree
