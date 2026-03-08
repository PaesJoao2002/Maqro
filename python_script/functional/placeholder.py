import customtkinter as ctk

class PlaceholderTextManager:
    def __init__(self, entry: ctk.CTkEntry):
        self.text_entry = entry
        self.placeholder_text = ""
        self.active = False

    def set_placeholder_text(self, text: str):
        self.placeholder_text = text
        self._apply_placeholder_text()

    def _apply_placeholder_text(self):
        self.text_entry.delete(0, "end")
        self.text_entry.insert(0,
                          self.placeholder_text)
        self.text_entry.configure(text_color="gray")
        self.active = True
        self.text_entry.icursor(0)
        self.text_entry.xview_moveto(0)

    def focus_in(self, event=None):
        if self.active:
            self.text_entry.icursor(0)
            self.text_entry.xview_moveto(0)

    def restore(self, event=None):
        if not self.text_entry.get():
            self._apply_placeholder_text()

    def clear_if_active(self):
        if self.active:
            self.text_entry.delete(0, "end")
            self.text_entry.configure(text_color=("#FFFFFF"))
            self.active = False