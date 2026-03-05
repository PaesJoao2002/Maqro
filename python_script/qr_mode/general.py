import customtkinter as ctk
from python_script.qr_mode.pix import gerar_payload_pix
from python_script.functional.ui_errors import show_error
from ..functional.placeholder import PlaceholderManager
from .pix_masks import apply_phone_mask, apply_cpf_mask, apply_cnpj_mask
from ..functional.validators import validate_text, validate_phone, validate_cpf, validate_cnpj, validate_email, validate_random_key
from python_script.screen.context_menu import EntryContextMenu

class GeneralTab(ctk.CTkFrame):
    def __init__(self, master, right_screen, mode_menu, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.right_screen = right_screen
        self.mode_menu = mode_menu

        action_row = ctk.CTkFrame(self, fg_color="transparent")
        action_row.pack(fill="x", pady=10)
        action_row.grid_columnconfigure(1, weight=1)

        self.pix_key_type = ctk.CTkOptionMenu(
            action_row,
            values=["Telefone","CPF","CNPJ","E-mail","Chave Aleatória"],
            width=140, height=40, command=self.on_pix_type_change
        )
        self.pix_key_type.grid(row=0,
                               column=0,
                               padx=(10,0),
                               sticky="w")

        self.input_container = ctk.CTkFrame(action_row, fg_color="transparent")
        self.input_container.grid(row=0,
                                  column=1,
                                  sticky="ew",
                                  padx=(10,0))
        self.input_container.grid_columnconfigure(1, weight=1)

        self.prefix_label = ctk.CTkLabel(self.input_container, text="https://")
        self.prefix_label.grid(row=0,
                               column=0,
                               padx=(20,10))
        self.prefix_label.grid_remove()

        self.text_field = ctk.CTkEntry(self.input_container,
                                       height=40,
                                       state="normal")
        self.text_field.grid(row=0,
                             column=1,
                             sticky="ew")

        EntryContextMenu(self.text_field, placeholder_attr="placeholder_active")

        self.button = ctk.CTkButton(action_row, text="Gerar/Atualizar", height=40, command=self.send_qr)
        self.button.grid(row=0, column=2, padx=10)

        self.placeholder = PlaceholderManager(self.text_field)
        self.placeholder.set("Digite aqui...")

        self.text_field.bind("<FocusIn>", self.placeholder.focus_in)
        self.text_field.bind("<FocusOut>", self.placeholder.restore)
        self.text_field.bind("<KeyPress>", self._handle_keypress)
        self.text_field.bind("<KeyRelease>", self._check_empty_and_mask)

        self.on_mode_change(self.mode_menu.segmented.get())

    def on_mode_change(self, mode: str):
        if mode == "Redirecionamento":
            self.pix_key_type.grid_remove()
            self.prefix_label.grid()
            self.placeholder.set("Digite o domínio (ex: google.com)")
        elif mode == "Pix":
            self.pix_key_type.grid()
            self.prefix_label.grid_remove()
            self._update_pix_placeholder()
        else:
            self.pix_key_type.grid_remove()
            self.prefix_label.grid_remove()
            self.placeholder.set("Digite seu texto aqui...")

    def _update_pix_placeholder(self):
        tipo = self.pix_key_type.get()
        texts = {
            "Telefone": "Digite o telefone (somente números)",
            "CPF": "Digite o CPF (somente números)",
            "CNPJ": "Digite o CNPJ (somente números)",
            "E-mail": "Digite o e-mail da chave Pix",
            "Chave Aleatória": "Digite a chave aleatória (UUID, 32 caracteres hex)"
        }
        self.placeholder.set(texts.get(tipo,"Digite a chave Pix..."))

    def _handle_keypress(self, event):
        if self.placeholder.active:
            if (event.state & 0x4) and event.keysym.lower() == "v":
                self.placeholder.clear_if_active()
                return
            if event.char and event.char.isprintable():
                self.placeholder.clear_if_active()
                return
            return "break"
        if event.state & 0x4:
            return
        allowed = ("BackSpace", "Delete", "Left", "Right", "Home", "End")
        if event.keysym in allowed or (event.char and event.char.isprintable()):
            return
        return "break"

    def send_qr(self):
        if self.placeholder.active:
            show_error("Campo vazio")
            return
        raw_text = self.text_field.get().strip()
        mode = self.mode_menu.segmented.get()
        try:
            if mode == "Texto":
                payload = validate_text(raw_text)
            elif mode == "Redirecionamento":
                if "." not in raw_text.split("/")[-1]:
                    raise ValueError("URL inválida")
                payload = "https://" + raw_text
            elif mode == "Pix":
                validators = {
                    "Telefone": validate_phone,
                    "CPF": validate_cpf,
                    "CNPJ": validate_cnpj,
                    "E-mail": validate_email,
                    "Chave Aleatória": validate_random_key
                }
                key_type = self.pix_key_type.get()
                payload = gerar_payload_pix(chave=validators[key_type](raw_text),
                                            tipo=key_type)
            else:
                return
            self.right_screen.render_from_string(payload)
        except ValueError as e:
            show_error(str(e))

    def _check_empty_and_mask(self, event=None):
        if self.placeholder.active:
            return
        mode = self.mode_menu.segmented.get()
        if mode != "Pix":
            return
        key_type = self.pix_key_type.get()
        text = self.text_field.get()
        if key_type == "Telefone":
            self.text_field.delete(0,"end")
            self.text_field.insert(0, apply_phone_mask(text))
        elif key_type == "CPF":
            self.text_field.delete(0,"end")
            self.text_field.insert(0, apply_cpf_mask(text))
        elif key_type == "CNPJ":
            self.text_field.delete(0,"end")
            self.text_field.insert(0, apply_cnpj_mask(text))
        elif not self.text_field.get():
            self.placeholder._apply_placeholder()

    def on_pix_type_change(self, value):
        self._update_pix_placeholder()