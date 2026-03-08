import customtkinter as ctk
import qrcode
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from python_script.functional.error_messages import NO_LOGO_TO_REMOVE
from python_script.functional.ui_errors import show_error

class RightScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.canvas = ctk.CTkCanvas(self, width=300, height=300, bg="#313131", highlightthickness=0)
        self.canvas.pack(padx=10, pady=(20, 0))

        self.export_button = ctk.CTkButton(
            self,
            text="Exportar PNG",
            command=self.export_image,
            height=60
        )
        self.export_button.pack(pady=10, padx=20, fill="x")

        self.tk_qr_image = None
        self.tk_logo_image = None

        self.current_qr = None
        self.logo_image = None

        self.last_data = "Muito obrigado por usar o MAQRO!"

        self.current_style = {
            "fill_color": "black",
            "back_color": "white"
        }

        self.final_image = None
        self._render_qr()

    def _render_qr(self):
        if not self.last_data:
            return

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )

        qr.add_data(self.last_data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=self.current_style["fill_color"],
            back_color=self.current_style["back_color"]
        ).convert("RGB")

        img = img.resize((310, 310), Image.NEAREST)

        self.current_qr = img
        self._render_canvas()

    def render_styled(self, data: str, style: dict):
        self.last_data = data
        self.current_style.update(style)

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=self.current_style["fill_color"],
            back_color=self.current_style["back_color"]
        ).convert("RGB")

        img = img.resize((260, 260), Image.NEAREST)
        
        self.current_qr = img
        self._render_canvas()

    def set_logo(self, pil_image):
        self.logo_image = pil_image
        self._render_canvas()

    def clear_logo(self):
        if self.logo_image is None:
            show_error(NO_LOGO_TO_REMOVE)
            return

        self.logo_image = None
        self.tk_logo_image = None
        self._render_canvas()

    def _render_canvas(self):
        if self.current_qr is None:
            return

        self.canvas.delete("all")

        self.final_image = self._compose_final_image()

        if self.final_image is None:
            return

        self.tk_qr_image = ImageTk.PhotoImage(self.final_image)
        self.canvas.create_image(150, 150, image=self.tk_qr_image)
    
    def _compose_final_image(self):
        if self.current_qr is None:
            return None

        final = self.current_qr.copy()

        if self.logo_image:
            qr_size = final.size[0]
            logo_size = int(qr_size * 0.30)

            logo = self.logo_image.copy()
            logo.thumbnail((logo_size, logo_size), Image.LANCZOS)

            pos = (
                (qr_size - logo.size[0]) // 2,
                (qr_size - logo.size[1]) // 2
            )

            if logo.mode in ("RGBA", "LA"):
                final.paste(logo, pos, logo)
            else:
                final.paste(logo, pos)

        return final
    
    def export_image(self):
        if self.final_image is None:
            return

        default_name = self._sanitize_filename(self.last_data)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagem PNG", "*.png")],
            title="Salvar QR Code",
            initialfile=default_name
        )

        if not file_path:
            return

        self.final_image.save(file_path)
    
    def render_from_string(self, data: str):
        self.last_data = data
        self._render_qr()
    
    def show_error(message: str):
        messagebox.showerror("Erro", message)
    
    def _sanitize_filename(self, text: str) -> str:
        if not text:
            return "qr_code"
        
        if text.startswith("https://"):
            text = text.replace("https://", "")

        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, "")

        text = text.strip()

        if len(text) > 40:
            text = text[:40]

        return text or "qr_code"