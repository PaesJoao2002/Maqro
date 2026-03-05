import customtkinter as ctk
from PIL import Image

class TitleMenu(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._drag_start_x = 0
        self._drag_start_y = 0

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.close_button = ctk.CTkButton(
            self,
            text="✕",
            width=45,
            height=45,
            corner_radius=8,
            font=("Segoe UI", 25, "bold"),
            cursor="arrow",
            command=self.close_app
        )
        self.close_button.grid(row=0, column=0, sticky="w", padx=(20, 0))
        self.close_button._no_drag = True

        spacer = ctk.CTkFrame(self, fg_color="transparent", height=0, width=80)
        spacer.grid(row=0, column=1, sticky="ew")

        self.header_image = ctk.CTkImage(
            light_image=Image.open("media/assets/header.png"),
            dark_image=Image.open("media/assets/header.png"),
            size=(481, 65)
        )

        self.header_label = ctk.CTkLabel(
            self,
            text="",
            image=self.header_image
        )
        self.header_label.grid(row=0, column=2, sticky="e") 

        self._bind_drag(self)

    def _start_move(self, event):
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def _on_move(self, event):
        dx = event.x_root - self._drag_start_x
        dy = event.y_root - self._drag_start_y

        window = self.winfo_toplevel()
        x = window.winfo_x() + dx
        y = window.winfo_y() + dy
        window.geometry(f"+{x}+{y}")

        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def _bind_drag(self, widget):
        if getattr(widget, "_no_drag", False):
            return

        widget.bind("<ButtonPress-1>", self._start_move)
        widget.bind("<B1-Motion>", self._on_move)

        try:
            widget.configure(cursor="fleur")
        except Exception:
            pass

        for child in widget.winfo_children():
            self._bind_drag(child)

    def close_app(self):
        self.winfo_toplevel().destroy()