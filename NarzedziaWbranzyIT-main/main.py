import tkinter as tk
from tkinter import filedialog
import json
import yaml
import os
import xmltodict

def convert_files():
    input_file = entry_input.get()
    output_file = entry_output.get()

    if not os.path.isfile(input_file):
        print(f"Plik wejściowy '{input_file}' nie istnieje.")
        return

    input_file_extension = input_file.split('.')[-1].lower()
    output_file_extension = output_format.get()

    # Wczytywanie danych
    with open(input_file, 'r') as file:
        if input_file_extension == 'json':
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print('Niepoprawny format pliku.', str(e))
                return

        elif input_file_extension == 'yaml':
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print('Niepoprawny format pliku YAML.', str(e))
                return

        elif input_file_extension == 'xml':
            try:
                data = xmltodict.parse(file.read())
            except xmltodict.ExpatError as e:
                print('Niepoprawny format pliku XML.', str(e))
                return
        else:
            print('Niepoprawny format pliku wejściowego. Dostępne formaty: xml, json, yaml.')
            return

    # Funkcje zapisywania danych do nowego formatu
    def json_to_yaml():
        with open(output_file, 'w') as file:
            yaml.dump(data, file, indent=4)

    def yaml_to_json():
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)

    def json_to_xml():
        with open(output_file, 'w') as file:
            xmltodict.unparse(data, output=file, pretty=True)

    def yaml_to_xml():
        with open(output_file, 'w') as file:
            xmltodict.unparse(data, output=file, pretty=True)

    def xml_to_json():
        json_data = json.dumps(data, indent=4)
        with open(output_file, "w") as json_file:
            json_file.write(json_data)

    def xml_to_yaml():
        yaml_data = yaml.dump(data, indent=4)
        with open(output_file, "w") as yaml_file:
            yaml_file.write(yaml_data)

    # Wywoływanie funkcji
    if input_file_extension == output_file_extension:
        print("Format pliku wejściowego i wyjściowego jest taki sam! Plik nie został utworzony.")
        return

    elif input_file_extension == 'json':
        if output_file_extension == 'yaml':
            print("Konwertowanie pliku json na yaml...")
            json_to_yaml()

        elif output_file_extension == 'xml':
            print("Konwertowanie pliku json na xml...")
            json_to_xml()

    elif input_file_extension == 'yaml':
        if output_file_extension == 'json':
            print("Konwertowanie pliku yaml na json...")
            yaml_to_json()

        elif output_file_extension == 'xml':
            print("Konwertowanie pliku yaml na xml...")
            yaml_to_xml()

    elif input_file_extension == 'xml':
        if output_file_extension == 'json':
            print("Konwertowanie pliku xml na json...")
            xml_to_json()

        elif output_file_extension == 'yaml':
            print("Konwertowanie pliku xml na yaml...")
            xml_to_yaml()

    print("Konwersja zakończona pomyślnie!")

def select_input_file():
    filename = filedialog.askopenfilename(filetypes=[('All Files', '*.*')])
    entry_input.delete(0, tk.END)
    entry_input.insert(tk.END, filename)

def select_output_file():
    filename = filedialog.asksaveasfilename(filetypes=[('All Files', '*.*')])
    entry_output.delete(0, tk.END)
    entry_output.insert(tk.END, filename)

root = tk.Tk()

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

lbl_input = tk.Label(frame, text="Plik wejściowy:")
lbl_input.grid(row=0, column=0, sticky='e')

entry_input = tk.Entry(frame, width=50)
entry_input.grid(row=0, column=1)

btn_input = tk.Button(frame, text="Wybierz...", command=select_input_file)
btn_input.grid(row=0, column=2)

lbl_output = tk.Label(frame, text="Plik wyjściowy:")
lbl_output.grid(row=1, column=0, sticky='e')

entry_output = tk.Entry(frame, width=50)
entry_output.grid(row=1, column=1)

btn_output = tk.Button(frame, text="Wybierz...", command=select_output_file)
btn_output.grid(row=1, column=2)

output_format = tk.StringVar(frame)
output_format.set('xml')  # ustawienie domyślnej wartości

lbl_format = tk.Label(frame, text="Format wyjściowy:")
lbl_format.grid(row=2, column=0, sticky='e')

opt_format = tk.OptionMenu(frame, output_format, 'xml', 'json', 'yaml')
opt_format.grid(row=2, column=1, sticky='w')

btn_convert = tk.Button(frame, text="Konwertuj", command=convert_files)
btn_convert.grid(row=3, column=1, pady=10)

root.mainloop()
