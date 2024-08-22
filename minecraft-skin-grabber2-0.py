import customtkinter as ctk
from customtkinter import filedialog
import requests
from PIL import Image, ImageTk
from tkinter import PhotoImage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

mainwintitle = "N8rd's Simple Skin Grabber for Minecraft - 1.1"
mainwinsize = "600x450"  # X and Y

mainwin = ctk.CTk()
mainwin.geometry(mainwinsize)
mainwin.title(mainwintitle)

#mainwin.iconbitmap(mainiconfile)

#mainicon = Image.open("small-pfp.ico")
#mainwin.iconphoto(True, mainicon)

# Variables
username = ""
uuid = ""
skin_image = None

# Making and displaying head label
headlabel = ctk.CTkLabel(mainwin, text="N8rd's Skin Grabber 1.1", font=("AzoSans-Black", 40, "bold"))
headlabel.pack()

# Making and displaying log label
Loglabel = ctk.CTkLabel(mainwin, text="N8rd on Discord", font=("Arial", 10, "bold"))
Loglabel.pack()

# Function to fetch UUID
def get_uuid(username):
    try:
        uuid_request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uuid_request.status_code == 200:
            uuid_data = uuid_request.json()
            return uuid_data["id"]
        else:
            print("Failed to retrieve the UUID for the given username.")
            Loglabel.configure(text="Failed to retrieve the UUID for the given username.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching UUID: {e}")
        Loglabel.configure(text=f"An error occurred while fetching UUID: {e}")
    return None

# Function to download skin
def download_skin():
    global username, uuid
    try:
        username = input_username_textbox.get("1.0", "end-1c").strip()
        print(username)
        Loglabel.configure(text="Skin: "+username)
        
        # Fetching UUID for the given username
        uuid = get_uuid(username)
        
        if uuid:
            skin_url = f"https://crafatar.com/skins/{uuid}"
            save_path = ctk.filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG', '*.png')])
            
            if save_path:
                skin_request = requests.get(skin_url)
                if skin_request.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(skin_request.content)
                    print("Skin downloaded successfully.")
                    Loglabel.configure(text="Skin downloaded successfully.")
                else:
                    print("Failed to retrieve the skin for the given username.")
                    Loglabel.configure(text="Failed to retrieve the skin for the given username.")
            else:
                print("No file selected. Skin not downloaded.")
                Loglabel.configure(text="No file selected. Skin not downloaded.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the skin: {e}")
        Loglabel.configure(text=f"An error occurred while downloading the skin: {e}")

# Function to render skin
def render_skin():
    global username, skin_image
    try:
        username = input_username_textbox.get("1.0", "end-1c").strip()
        print(username)
        Loglabel.configure(text="Skin: " + username)

        # Fetching UUID for the given username
        uuid = get_uuid(username)

        if uuid:
            render_url = f"https://crafatar.com/renders/body/{uuid}?overlay"

            render_request = requests.get(render_url)
            if render_request.status_code == 200:
                with open('temp_render.png', 'wb') as f:
                    f.write(render_request.content)

                skin_image = Image.open('temp_render.png')
                skin_image.thumbnail((300, 300))  # Resizing the image for display

                # Convert to PhotoImage
                skin_photo = ImageTk.PhotoImage(skin_image)

                skin_label.configure(image=skin_photo)
                skin_label.image = skin_photo  # Keeping a reference to prevent garbage collection
            else:
                print("Failed to render the skin for the given username.")
                Loglabel.configure(text="Failed to render the skin for the given username.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while rendering the skin: {e}")
        Loglabel.configure(text=f"An error occurred while rendering the skin: {e}")





# Creating a text box widget
input_username_textbox = ctk.CTkTextbox(mainwin, height=5, width=160)
input_username_textbox.pack()

# Button to render the skin
render_button = ctk.CTkButton(mainwin, height=30, width=120, text="Render Skin", command=render_skin)
render_button.pack()

# Label to display the skin image
skin_label = ctk.CTkLabel(mainwin, text=" ")
skin_label.pack()

# Button to download the skin
download_button = ctk.CTkButton(mainwin, height=30, width=120, text="Download Skin", command=download_skin)
download_button.pack()



mainwin.mainloop()
