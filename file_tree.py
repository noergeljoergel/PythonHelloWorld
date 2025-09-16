import tkinter as tk
import ttkbootstrap as ttk

class CheckBoxTree(ttk.Treeview):
    """TreeView mit Checkboxen (anklickbar)."""

    def __init__(self, master=None, callback=None, **kw):
        super().__init__(master, **kw)
        self.callback = callback

        self.img_unchecked = tk.PhotoImage(width=16, height=16)
        self.img_checked = tk.PhotoImage(width=16, height=16)
        self._draw_checkbox(self.img_unchecked, False)
        self._draw_checkbox(self.img_checked, True)

        self._checked = {}
        self.bind("<Button-1>", self._on_click)

    def _draw_checkbox(self, img, checked):
        """Zeichnet ein Kästchen, optional mit fettem grünen Häkchen."""
        # Hintergrund weiß
        img.put(("white",), to=(0, 0, 15, 15))
        # schwarzer Rahmen
        for i in range(16):
            img.put(("black",), to=(i, 0))
            img.put(("black",), to=(i, 15))
            img.put(("black",), to=(0, i))
            img.put(("black",), to=(15, i))
        if checked:
            # dickes grünes Häkchen (✓)
            # linker Teil: von links unten nach Mitte hoch
            for i in range(4, 8):
                for w in range(-1, 2):  # macht die Linie dick
                    img.put(("green",), to=(i, i + 4 + w))
                    img.put(("green",), to=(i, i + 5 + w))
            # rechter Teil: von Mitte nach rechts oben
            for i in range(8, 13):
                for w in range(-1, 2):
                    img.put(("green",), to=(i, 18 - i + w))
                    img.put(("green",), to=(i, 17 - i + w))

    def insert(self, parent, index, iid=None, **kw):
        node_id = super().insert(parent, index, iid=iid, **kw)
        self._checked[node_id] = False
        self.item(node_id, image=self.img_unchecked)
        return node_id

    def _on_click(self, event):
        region = self.identify("region", event.x, event.y)
        if region == "tree":
            node_id = self.identify_row(event.y)
            if node_id:
                self.toggle(node_id)

    def toggle(self, node_id):
        current = self._checked.get(node_id, False)
        new_state = not current
        self._checked[node_id] = new_state
        self.item(node_id, image=self.img_checked if new_state else self.img_unchecked)
        if self.callback:
            self.callback()

    def get_checked_paths(self):
        paths = []
        for node_id, state in self._checked.items():
            if state:
                vals = self.item(node_id, "values")
                if vals:
                    paths.append(vals[0])
        return paths

    def reset_all(self):
        for node_id in list(self._checked.keys()):
            self._checked[node_id] = False
            self.item(node_id, image=self.img_unchecked)
        if self.callback:
            self.callback()
