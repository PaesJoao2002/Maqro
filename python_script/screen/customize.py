import customtkinter as ctk
from tkinter import colorchooser, filedialog
from PIL import Image


class CustomizeTab(ctk.CTkFrame):
    def __init__(self, master, right_screen, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.right_screen = right_screen
        self.center_image = None

        self.qr_color = "#000000"
        self.bg_color = "#FFFFFF"

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=10)

        font_button = ctk.CTkFont(weight="bold")

        self.qr_btn = ctk.CTkButton(row, text="Cor dos pontos", font=font_button, command=self.pick_qr_color, height=40)
        self.qr_btn.pack(fill="x", pady=3)

        self.bg_btn = ctk.CTkButton(row, text="Cor do fundo", font=font_button, command=self.pick_bg_color, height=40)
        self.bg_btn.pack(fill="x", pady=3)

        self.logo_btn = ctk.CTkButton(row, text="Adicionar logo", font=font_button, command=self.pick_logo, height=40)
        self.logo_btn.pack(fill="x", pady=3)

        self.remove_logo_btn = ctk.CTkButton(row, text="Remover logo", font=font_button, command=self.remove_logo, height=40)
        self.remove_logo_btn.pack(fill="x", pady=3)

    def pick_logo(self):
        path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.webp")]
        )

        if not path:
            return

        self.center_image = Image.open(path).convert("RGBA")
        self.right_screen.set_logo(self.center_image)

    def remove_logo(self):
        self.center_image = None
        self.right_screen.clear_logo()

    def pick_qr_color(self):
        color = colorchooser.askcolor(title="Escolha a cor do QR")

        if color[1] is None:
            return

        self.qr_color = color[1]
        self._apply_style()

    def pick_bg_color(self):
        color = colorchooser.askcolor(title="Escolha a cor de fundo")

        if color[1] is None:
            return

        self.bg_color = color[1]
        self._apply_style()

    def _apply_style(self):

        style = {
            "fill_color": self.qr_color,
            "back_color": self.bg_color
        }

        self.right_screen.render_styled(
            self.right_screen.last_data,
            style
        )