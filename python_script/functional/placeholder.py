import customtkinter as ctk

class PlaceholderManager:
    def __init__(self, entry: ctk.CTkEntry):
        self.entry = entry
        self.placeholder_text = ""
        self.active = False

    def set(self, text: str):
        self.placeholder_text = text
        self._apply_placeholder()

    def _apply_placeholder(self):
        self.entry.delete(0, "end")
        self.entry.insert(0,
                          self.placeholder_text)
        self.entry.configure(text_color="gray")
        self.active = True
        self.entry.icursor(0)
        self.entry.xview_moveto(0)

    def focus_in(self, event=None):
        if self.active:
            self.entry.icursor(0)
            self.entry.xview_moveto(0)

    def restore(self, event=None):
        if not self.entry.get():
            self._apply_placeholder()

    def clear_if_active(self):
        if self.active:
            self.entry.delete(0, "end")
            self.entry.configure(text_color=("#FFFFFF"))
            self.active = False