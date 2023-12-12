import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading

def run_script(script_name):
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    output_display.insert(tk.END, result.stdout)
    output_display.insert(tk.END, result.stderr)
    output_display.yview(tk.END)  

def run_lhs1():
    threading.Thread(target=run_script, args=("LHS.py",), daemon=True).start()
def run_95ppu6():
    threading.Thread(target=run_script, args=("95PPU.py",), daemon=True).start()
def run_som_py():
    threading.Thread(target=run_script, args=("SOM-py.py",), daemon=True).start()

root = tk.Tk()
root.title("SWAT-SOM")
root.geometry("600x400")
root.configure(bg="lightgrey")
btn_lhs1 = tk.Button(root, text="Latin Hypercube Sampling", command=run_lhs1)
btn_lhs1.pack(pady=10)

btn_95ppu6 = tk.Button(root, text="Model Uncertainty Analysis-95PPU", command=run_95ppu6)
btn_95ppu6.pack(pady=10)

btn_som_py = tk.Button(root, text="SOM for Parameter Range Optimization", command=run_som_py)
btn_som_py.pack(pady=10)

output_display = scrolledtext.ScrolledText(root, width=70, height=10)
output_display.pack(pady=10)

root.mainloop()