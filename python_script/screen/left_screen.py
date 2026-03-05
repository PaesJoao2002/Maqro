import customtkinter as ctk
from python_script.script_appearance.title import TitleMenu
from python_script.functional.mode_selection import ModeSelection
from python_script.qr_mode.general import GeneralTab
from python_script.screen.customize import CustomizeTab
from python_script.screen.text_hint import TextFrame


class LeftScreen(ctk.CTkFrame):
    def __init__(self, master, right_screen, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.right_screen = right_screen

        title = TitleMenu(self)
        title.pack(anchor="w")

        self.mode_menu = ModeSelection(self, command=self._on_mode_change)
        self.mode_menu.pack(anchor="center", fill="x", expand=False, pady=10)

        self.left_screen_content = ctk.CTkFrame(
            self,
            fg_color="#313131",
            height=205
        )
        self.left_screen_content.pack(fill="x", padx=20)
        self.left_screen_content.pack_propagate(False)

        self.textframe = TextFrame(self.left_screen_content, self.mode_menu)
        self.textframe.pack(fill="both", expand=True, padx=20)

        self.general_tab = GeneralTab(self, self.right_screen, self.mode_menu)
        self.general_tab.pack(side="top", fill="x")

        self.customize_tab = CustomizeTab(self.left_screen_content, self.right_screen)
        self.customize_tab.pack(side="top", fill="x", padx=20)

        current_mode = self.mode_menu.get()
        self.textframe.initialize_mode(current_mode)
        self._on_mode_change(self.mode_menu.get())

    def _on_mode_change(self, value):
        print("Modo mudou para:", value)
        self.textframe.update_mode(value)

        if value == "Customizar...":
            self.general_tab.pack_forget()
            self.textframe.pack_forget()
            self.customize_tab.pack(fill="both", expand=True, padx=20, pady=0)

        else:
            self.customize_tab.pack_forget()
            self.textframe.pack(fill="both", expand=True, padx=20, pady=0)
            self.general_tab.pack(side="top", fill="x", expand=False, padx=10, pady=0)
            self.general_tab.on_mode_change(value)