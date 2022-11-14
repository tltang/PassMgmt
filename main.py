from tkinter import *
import os.path
import random
import pyperclip
import json
# reason messagebox has to be imported separately is becuase it is not a class
from tkinter import messagebox

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    passwordlist = [random.choice(letters) for i in range(1, nr_letters + 1)]

    passwordlist += [random.choice(symbols) for i in range(1, nr_symbols + 1)]

    passwordlist += [random.choice(numbers) for i in range(1, nr_numbers + 1)]

    random.shuffle(passwordlist)                        # Shuffle a list

    finalpassword = "".join(passwordlist)
    pyperclip.copy(finalpassword)
    password_input.insert(0,finalpassword)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_clicked():
    website = website_input.get()
    user = username_input.get()
    password = password_input.get()
    is_ok = True
    new_data = {
        website: {
            "email": user,
            "password": password
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
        is_ok = False
        website_input.focus()

    if is_ok == True:
        is_ok = messagebox.askokcancel(website, message=f"You have entered \n website: {website} \n userid: {user} \n password: {password} \n ok to save?")

    if is_ok:
        try:
            with open("password.json", "r") as import_password:
                json_data = json.load(import_password)
        except FileNotFoundError:
            with open("password.json", "w") as import_password:
                json.dump(new_data, import_password, indent=4)
        else:
            json_data.update(new_data)

            with open("password.json", "w") as import_password:
                json.dump(json_data, import_password, indent=4)
        finally:
            website_input.delete(0, 'end')
            password_input.delete(0, 'end')
            username_input.delete(0, 'end')
            username_input.insert(0, 'tltang74@gmail.com')
            website_input.focus()

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_clicked():
    website = website_input.get()
    is_ok = True
    lFound = False

    if website == "":
        messagebox.showerror(title="Oops", message="Please enter a website to search for!")
        is_ok = False
        website_input.focus()

    if is_ok == False:
        return

    try:
        with open("password.json", "r") as import_password:
            json_data = json.load(import_password)
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="Password File Not Found!")
    else:
        for (k, v) in json_data.items():
            if k == website:
                lFound = True
                cEmail = v["email"]
                cPw = v["password"]
                messagebox.showinfo(website, message=f"userid: {cEmail} \n password: {cPw} \n\n\n")
                password_input.delete(0, 'end')
                username_input.delete(0, 'end')
                password_input.insert(0, cPw)
                username_input.insert(0, cEmail)

        if lFound == False:
            messagebox.showerror(title="Oops", message=f"Website {website} is not in password file!")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")

canvas = Canvas(width=200, height=200, highlightthickness=3, highlightbackground="black")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

window.config(padx=20, pady=20)
my_label1 = Label(text="Website:")
my_label1.grid(row=1)
my_label2 = Label(text="Email/Username:")
my_label2.grid(row=2)
my_label3 = Label(text="Password:")
my_label3.grid(row=3)
website_input = Entry(width=21)
website_input.grid(column=1, row=1, sticky='EW')
website_input.focus()
username_input = Entry(width=35)
username_input.grid(column=1, row=2, columnspan=2, sticky='EW')
username_input.insert(0, 'tltang74@gmail.com')
password_input = Entry(width=21)
password_input.grid(column=1, row=3, sticky='EW')

add_button = Button(text="Add", width=36, command=add_clicked)
add_button.grid(column=1, row=4, columnspan=2, sticky='EW')
search_button = Button(text="Search", command=search_clicked)
search_button.grid(column=2, row=1, sticky='EW')
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

window.mainloop()