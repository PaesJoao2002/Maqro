import tkinter as tk

class EntryContextMenu:
    def __init__(self, entry, placeholder_attr=None):
        self.entry = entry
        self.placeholder_attr = placeholder_attr

        self.menu = tk.Menu(entry, tearoff=0)
        self.menu.add_command(label="Copiar", command=self._copy)
        self.menu.add_command(label="Colar", command=self._paste)
        self.menu.add_command(label="Recortar", command=self._cut)
        self.menu.add_command(label="Excluir", command=self._delete)

        self.entry.bind("<Button-3>", self._show_menu)

    def _show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def _copy(self):
        try:
            selection = self.entry.selection_get()
            self.entry.clipboard_clear()
            self.entry.clipboard_append(selection)
        except tk.TclError:
            pass

    def _paste(self):
        try:
            paste_text = self.entry.clipboard_get()
        except tk.TclError:
            paste_text = ""

        if not paste_text:
            return

        self._disable_placeholder()

        idx = self.entry.index("insert")
        self.entry.insert(idx, paste_text)

    def _cut(self):
        try:
            selection = self.entry.selection_get()
            self.entry.clipboard_clear()
            self.entry.clipboard_append(selection)
            start = self.entry.index("sel.first")
            end = self.entry.index("sel.last")
            self.entry.delete(start, end)
        except tk.TclError:
            pass
        self._disable_placeholder()

    def _delete(self):
        try:
            start = self.entry.index("sel.first")
            end = self.entry.index("sel.last")
            self.entry.delete(start, end)
        except tk.TclError:
            self.entry.delete(0, "end")
        self._disable_placeholder()

    def _disable_placeholder(self):
        if self.placeholder_attr and hasattr(self.entry.master, self.placeholder_attr):
            setattr(self.entry.master, self.placeholder_attr, False)
        try:
            self.entry.configure(text_color=("gray10", "gray90"))
        except Exception:
            pass