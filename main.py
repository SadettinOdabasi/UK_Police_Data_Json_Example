import json
import tkinter as tk
from tkinter import ttk
import requests


window = tk.Tk()
window.title("UK Police Forces Data")
window.minsize(600, 600)

FONT = ("Calibri", 14, "normal")

force_url = "https://data.police.uk/api/forces"


def get_list_no_params(url):
    response_text = requests.get(url).text
    return json.loads(response_text)


def get_list_with_params(url, payload):
    response_text = requests.get(url, params=payload).text
    return json.loads(response_text)


name_list = []
id_list = []
i = 0

force_list = get_list_no_params(force_url)

while i < len(force_list):
    name_list.append(force_list[i]["name"])
    id_list.append(force_list[i]["id"])
    i += 1

# print(name_list)

lbl_forces = tk.Label(text="Select Force", padx=10, pady=10, font=FONT)
lbl_forces.pack()

selected_force = tk.StringVar()

cmb_forces = ttk.Combobox(window, textvariable=selected_force, font=FONT)
cmb_forces["values"] = name_list
cmb_forces.pack(padx=10, pady=10)



lbl_date = tk.Label(text="Select Date", padx=10, pady=10, font=FONT)
lbl_date.pack()

selected_date = tk.StringVar()

cmb_date = ttk.Combobox(window, textvariable=selected_date, font=FONT)
cmb_date["values"] = ["2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08", "2021-09",
                      "2021-10", "2021-11", "2021-12"]
cmb_date.pack(padx=10, pady=10)

lbl_crimes = tk.Label(text="Select Crime Type", padx=10, pady=10, font=FONT)
lbl_crimes.pack()

crime_name_list = []
crime_url_list = []
crime_url = "https://data.police.uk/api/crime-categories"
payload = {"date": cmb_date.get()}
i = 0

crime_list = get_list_with_params(crime_url, payload)

while i < len(crime_list):
    crime_name_list.append(crime_list[i]["name"])
    crime_url_list.append(crime_list[i]["url"])
    i += 1

selected_crime = tk.StringVar()

cmb_crimes = ttk.Combobox(window, textvariable=selected_crime, font=FONT)
cmb_crimes["values"] = crime_name_list
cmb_crimes.pack(padx=10, pady=10)


def show_crime_numbers():

    url = "https://data.police.uk/api/crimes-no-location"
    index_of_selected_force = name_list.index(cmb_forces.get())
    id_of_selected_force = id_list[index_of_selected_force]
    crime_date = cmb_date.get()
    index_of_selected_crime = crime_name_list.index(cmb_crimes.get())
    url_of_selected_crime = crime_url_list[index_of_selected_crime]
    payload_button = {"category": url_of_selected_crime, "force": id_of_selected_force, "date": crime_date}
    response_button_text = requests.get(url, payload_button).text
    response_jason = json.loads(response_button_text)

    response_list = []
    i2 = 0

    while i2 < len(response_jason):
        response_list.append(response_jason[i]["id"])
        i2 += 1

    lbl_result.config(text=f"Number of crimes of selected values: {len(response_list)+1}")


btn_show_number_of_crimes = tk.Button(text="Show Number of Crimes", padx=10, pady=10, width=30, command=show_crime_numbers, font=FONT)
btn_show_number_of_crimes.pack()

lbl_result = tk.Label(text="", pady=10, padx=10, font=FONT)
lbl_result.pack()

window.mainloop()
