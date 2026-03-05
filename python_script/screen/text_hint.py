import customtkinter as ctk

class TextFrame(ctk.CTkFrame):
    def __init__(self, master, mode_menu, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.configure(height=90)
        self.pack_propagate(False)

        self.mode_menu = mode_menu

        self.hint_title = ctk.CTkLabel(self, text="", font=("Segoe UI Light", 45))
        self.hint_title.pack(anchor="w")

        self.hint_desc = ctk.CTkLabel(
            self,
            justify="left",
            anchor="nw",
            text=""
        )
        self.hint_desc.pack(anchor="w", fill="both", expand=True, pady=5)

        self.hint_observation = ctk.CTkLabel(
            self,
            justify="left",
            anchor="sw",
            text_color="#9C9C9C",
            text="",
            font=("Segoe UI", 12),
            pady=20
        )
        self.hint_observation.pack(anchor="w", fill="both", expand=True, pady=5)

        self.bind("<Configure>", self._update_wraplength)

    def initialize_mode(self, value):
        self.update_mode(value)

    def set_hint_text(self, text):
        self.hint_desc.configure(text=text)
        self.update_idletasks()
        self._update_wraplength()
    
    def set_observation_text(self, text):
        self.hint_observation.configure(text=text)
        self.update_idletasks()
        self._update_wraplength()

    def _update_wraplength(self, event=None):
        width = self.winfo_width() - 20
        if width > 50:
            self.hint_desc.configure(wraplength=width)
            self.hint_observation.configure(wraplength=width)

    def update_mode(self, value):
        print("TextFrame.update_mode recebeu:", value)

        self.hint_title.configure(text="")
        self.set_hint_text("")
        self.set_observation_text("")

        self.hint_title.configure(text=value)

        if value == "Texto":
            self.set_hint_text(
                "Texto é o modo mais tradicional de se produzir QR Codes. "
                "Um QR Code em texto exibirá um texto direto da câmera "
                "do celular e será usado para transmitir mensagens rápidas, "
                "instruções, avisos ou até declarações."
            )
            self.set_observation_text(
                "OBS.: Esse modo não é recomendado para gerar QR Codes "
                "para redirecionar o usuário para outro site ou para gerar "
                "QR Codes para pagamentos via pix. Acesse a aba \"Redirecionamento\" "
                "ou \"Pix\" para esses fins."
            )

        elif value == "Redirecionamento":
            self.set_hint_text(
                "Gera QR Codes que contém links. "
                "Podem ser usados para redirecionar usuários para sites, "
                "imagens, vídeos, arquivos PDF, adicionar número de Whatsapp "
                "ou ir para uma rede social específica."
            )
            
            self.set_observation_text(
                "OBS.: Esse modo não é recomendado para gerar QR Codes "
                "para pagamentos via pix. Acesse a aba \"Pix\" "
                "para esse fim."
            )

        elif value == "Pix":
            self.set_hint_text(
                "Nessa opção você pode gerar QR Codes para pagamentos via Pix. "
                "Útil para comerciantes ou prestadores de serviços, basta inserir "
                "sua chave (opcionalmente o valor que deseja)."
            )
            self.set_observation_text(
                "OBS.: Esse modo não é recomendado para gerar QR Codes "
                "para redirecionar o usuário para outro site. Acesse a aba "
                "\"Redirecionamento\" para esse fim."
            )

        elif value == "Customizar...":
            self.set_hint_text("")
            self.hint_title.configure(text="")
        
        self.update_idletasks()
        self._update_wraplength()
