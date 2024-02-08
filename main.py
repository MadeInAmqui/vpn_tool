import tkinter as tk
import subprocess

from windows import make_window

bg = "#010d1d"

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def get_result():
    result = subprocess.run(["ifconfig"], shell=True, capture_output=True, text=True)
    result = str(result)
    return result

def validate_button(popup, connected, password_entry):
    password = password_entry.get()
    if connected == True:
        subprocess.run(["sudo -S -k wg-quick down wg0"], input=password, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(["sudo -S -k wg-quick up wg0"], input=password, shell=True, capture_output=True, text=True)
        popup.destroy()
    clear_frame(frame1)
    connected = load_frame1()
    if connected == True:
        label = tk.Label(frame1, text=' Connecté a VPN Maison ! ', background=bg, foreground='white')
        label.place(relx=0.75, rely=0.6, anchor="center")
    elif connected == False:
        label = tk.Label(frame1, text="Le VPN n'est pas connecté", background=bg, foreground='white')
        label.place(relx=0.75, rely=0.6, anchor="center")

def bouton_press(connected, frame1):
    result = get_result()
    
    if "broadcast" in result:
        popup = tk.Toplevel(frame1)
        popup.title("Mot de passe")
        popup.resizable(False, False)

        image = '/usr/local/etc/VPN/data/bg2.png'
        resize = (400, 300)
        make_window(popup, image, resize)

        label = tk.Label(popup, text='Enter le mot de passe "SUDO":', background=bg, foreground='white')
        label.place(relx=0.5, rely=0.25, anchor="center")

        password_entry = tk.Entry(popup, show="*")
        password_entry.place(relx=0.5, rely=0.5, anchor="center")

        bouton = tk.Button(popup, text='Validate', command=lambda:validate_button(popup, connected, password_entry))
        bouton.place(relx=0.5, rely=0.75, anchor="center")

        # fait la même chose que quand on clic mais avec le toucher enter
        popup.bind('<Return>', lambda event=None: validate_button(popup, connected, password_entry))
    else:
        label = tk.Label(frame1, text="Aucune connexion réseau", background=bg, foreground='white')
        label.place(relx=0.75, rely=0.6, anchor="center")

def load_frame1():
    image = '/usr/local/etc/VPN/data/bg.png'
    resize = (500, 350)
    make_window(frame1, image, resize)

    result = get_result()

    if "wg0" in result:
        bouton = tk.Button(frame1, text="Disconnect from VPN", command=lambda:bouton_press(True, frame1))
        bouton.place(relx=0.75, rely=0.3, anchor="center")
        connected = True
    else:
        bouton = tk.Button(frame1, text="Connect to VPN", command=lambda:bouton_press(False, frame1))
        bouton.place(relx=0.75, rely=0.3, anchor="center")
        connected = False
    
    return connected

app = tk.Tk()
app.resizable(False, False)
app.title('VPN')

frame1 = tk.Frame(app)
frame1.grid(column=0, row=0)

load_frame1()


app.mainloop()
