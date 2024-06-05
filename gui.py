import tkinter as tk
from tkinter import ttk
import requests
import json

def send_request():
    # Collect data from the user inputs
    data = {
        'ph': float(entry_ph.get()),
        'Hardness': float(entry_hardness.get()),
        'Solids': float(entry_solids.get()),
        'Chloramines': float(entry_chloramines.get()),
        'Sulfate': float(entry_sulfate.get()),
        'Conductivity': float(entry_conductivity.get()),
        'Organic_carbon': float(entry_organic_carbon.get()),
        'Trihalomethanes': float(entry_trihalomethanes.get()),
        'Turbidity': float(entry_turbidity.get())
    }
    
    # Send data to the Flask API
    response = requests.post('http://127.0.0.1:5000/predict', json=data)
    result = response.json()

    # Display the results
    purity_label.config(text=f"Predicted Purity: {result['prediction'][0]:.2f}%")
    #interpretation_label.config(text=f"Interpretation: {result['interpretation']}")

# Create the main application window
root = tk.Tk()
root.title("Water Purity Predictor")

# Create and place the input fields and labels
fields = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
entries = {}

for field in fields:
    label = ttk.Label(root, text=field)
    label.pack()
    entry = ttk.Entry(root)
    entry.pack()
    entries[field] = entry

entry_ph = entries['ph']
entry_hardness = entries['Hardness']
entry_solids = entries['Solids']
entry_chloramines = entries['Chloramines']
entry_sulfate = entries['Sulfate']
entry_conductivity = entries['Conductivity']
entry_organic_carbon = entries['Organic_carbon']
entry_trihalomethanes = entries['Trihalomethanes']
entry_turbidity = entries['Turbidity']

# Create and place the buttons and labels for results
predict_button = ttk.Button(root, text="Predict Purity", command=send_request)
predict_button.pack()

purity_label = ttk.Label(root, text="Predicted Purity: ")
purity_label.pack()

interpretation_label = ttk.Label(root, text="Interpretation: ")
interpretation_label.pack()

# Start the Tkinter main loop
root.mainloop()