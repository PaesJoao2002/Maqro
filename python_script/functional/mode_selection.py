import customtkinter as ctk

class ModeSelection(ctk.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.segmented = ctk.CTkSegmentedButton(
            self,
            values=["Texto", "Redirecionamento", "Pix", "Customizar..."],
            command=command
        )
        self.segmented.pack(anchor="w", padx=20, fill="x")

        self.segmented.set("Texto")

    def get(self):
        return self.segmented.get()