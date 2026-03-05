import customtkinter as ctk
from tkextrafont import Font
from PIL import Image, ImageTk
from python_script.screen.right_screen import RightScreen
from python_script.screen.left_screen import LeftScreen

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("appearance/qrcode_theme.json")

app = ctk.CTk()
app.geometry("1000x406")

app.overrideredirect(True)

main = ctk.CTkFrame(app)
main.pack(fill="both", expand=True, padx=10, pady=10)

right = ctk.CTkFrame(main, fg_color="transparent")
right.pack(side="right", fill="both", expand=True)

right_screen = RightScreen(right)
right_screen.pack(anchor="w", fill="both", expand=True)

separator = ctk.CTkFrame(main, fg_color="#4a4a4a", width=2, corner_radius=0)
separator.pack(anchor="center", side="right", fill="y")

left = ctk.CTkFrame(main, fg_color="transparent")
left.pack(side="left", fill="both", expand=True)

left_screen = LeftScreen(left, right_screen)
left_screen.pack(anchor="center", fill="both", expand=True)

icon = ctk.CTkImage(light_image=Image.open("media/assets/icon.png"))
app.iconphoto(True, ImageTk.PhotoImage(Image.open("media/assets/icon.png")))

app.mainloop()