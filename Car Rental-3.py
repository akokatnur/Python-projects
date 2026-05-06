import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

Car_Data = "car_rentals.txt"

car_list = [
    ("Audi", "audi.jpeg"),
    ("Yellow Audi", "audiyellow.jpeg"),
    ("Ford", "ford.jpeg"),
    ("Range Rover", "range.jpeg"),
    ("Mercedes", "mercedes.jpeg")
]

selected_cars = []

def generate_unique_id():
    existing_ids = set()
    if os.path.exists(Car_Data):
        with open(Car_Data, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 1:
                    existing_ids.add(parts[0])
    while True:
        new_id = str(random.randint(1000, 9999))
        if new_id not in existing_ids:
            return new_id

def save_cars():
    name = name_entry.get().strip()
    if not name or not selected_cars:
        messagebox.showerror("Input Error", "Please enter your name and select at least one car.")
        return

    customer_id = generate_unique_id()

    with open(Car_Data, "a") as file:
        for car in selected_cars:
            file.write(f"{customer_id},{name},{car}\n")

    messagebox.showinfo("Success", f"Rental saved with ID: {customer_id}")
    name_entry.delete(0, tk.END)
    for var in car_vars:
        var.set(0)
    selected_cars.clear()

def view_cars():
    if not os.path.exists(Car_Data):
        messagebox.showinfo("No Data", "No rental records found.")
        return
    with open(Car_Data, "r") as file:
        records = file.readlines()
    if not records:
        messagebox.showinfo("Empty", "No rentals found.")
    else:
        messagebox.showinfo("Car Rentals", "".join(records))

def return_car():
    def process_return():
        return_id = entry_id.get().strip()
        return_car = entry_car.get().strip()
        if not os.path.exists(Car_Data):
            messagebox.showerror("Error", "No rental records found.")
            return
        updated_lines = []
        removed = False
        with open(Car_Data, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3 and parts[0] == return_id and parts[2] == return_car:
                    removed = True
                    continue
                updated_lines.append(line)
        with open(Car_Data, "w") as file:
            file.writelines(updated_lines)
        if removed:
            messagebox.showinfo("Returned", f"{return_car} has been returned.")
            return_window.destroy()
        else:
            messagebox.showerror("Not Found", "Matching rental not found.")

    return_window = tk.Toplevel(app)
    return_window.title("Return Car")
    return_window.geometry("300x150")
    tk.Label(return_window, text="Enter Customer ID:").pack(pady=5)
    entry_id = tk.Entry(return_window)
    entry_id.pack()
    tk.Label(return_window, text="Enter Car Name:").pack(pady=5)
    entry_car = tk.Entry(return_window)
    entry_car.pack()
    tk.Button(return_window, text="Return", command=process_return).pack(pady=10)

def process_car_data(index):
    if car_vars[index].get():
        selected_cars.append(car_list[index][0])
    else:
        if car_list[index][0] in selected_cars:
            selected_cars.remove(car_list[index][0])

# GUI Setup
app = tk.Tk()
app.title("Car Rental System")
app.geometry("650x500")
app.configure(bg="white")

tk.Label(app, text="Enter Your Name:", font=("Arial", 12), bg="white").pack(pady=5)
name_entry = tk.Entry(app, font=("Arial", 12))
name_entry.pack()

frame = tk.Frame(app, bg="white")
frame.pack(pady=20)

car_vars = []
car_images = []

for i, (car_name, img_file) in enumerate(car_list):
    var = tk.IntVar()
    car_vars.append(var)
    try:
        image = Image.open(img_file)
        image = image.resize((60, 40))
        photo = ImageTk.PhotoImage(image)
        car_images.append(photo)
    except:
        car_images.append(None)

    chk = tk.Checkbutton(frame, text=car_name, variable=var, image=car_images[i],
                         compound='left', padx=10, bg='white', command=lambda i=i: process_car_data(i),
                         font=("Arial", 10))
    chk.pack(anchor='w', pady=4)

tk.Button(app, text="Save Rental", bg="green", fg="white", command=save_cars).pack(pady=10)
tk.Button(app, text="View Rentals", command=view_cars).pack()
tk.Button(app, text="Return Car", command=return_car).pack(pady=5)

app.mainloop()
