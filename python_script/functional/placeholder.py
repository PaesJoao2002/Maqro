import customtkinter as ctk


class PlaceholderTextManager:
    def __init__(self, entry: ctk.CTkEntry):
        self.entry = entry
        self.placeholder = ""
        self.active = False

    def set(self, text: str):
        self.placeholder = text
        self.show()

    def show(self):
        e = self.entry
        e.delete(0, "end")
        e.insert(0, self.placeholder)
        e.configure(text_color="gray")
        e.icursor(0)
        e.xview_moveto(0)
        self.active = True

    def focus_in(self, event=None):
        if not self.active:
            return
        e = self.entry
        e.icursor(0)
        e.xview_moveto(0)

    def restore(self, event=None):
        if self.entry.get():
            return
        self.show()

    def clear_if_active(self):
        if not self.active:
            return
        e = self.entry
        e.delete(0, "end")
        e.configure(text_color="#FFFFFF")
        self.active = False