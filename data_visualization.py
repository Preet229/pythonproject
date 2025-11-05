import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

# Initialize main window
root = tk.Tk()
root.title("📊 Data Visualization Dashboard")
root.geometry("950x700")
root.config(bg="#dbd4d4")

# Global variables
current_canvas = None
current_fig = None
data = None

# --- Function to load CSV file ---
def load_csv():
    global data
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            data = pd.read_csv(file_path)
            columns = list(data.columns)
            if len(columns) < 2:
                messagebox.showwarning("⚠️ Warning", "The selected CSV must contain at least two columns.")
                return
            x_dropdown["values"] = columns
            y_dropdown["values"] = columns
            x_dropdown.current(0)
            y_dropdown.current(1)
            messagebox.showinfo("✅ Success", f"File loaded successfully:\n{file_path}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Could not read the CSV file:\n{e}")

# --- Function to draw selected chart ---
def draw_chart(chart_type):
    global current_canvas, current_fig, data

    if data is None:
        messagebox.showwarning("⚠️ No Data", "Please load a CSV file first.")
        return

    x_col = x_var.get()
    y_col = y_var.get()

    if not x_col or not y_col:
        messagebox.showwarning("⚠️ Missing Columns", "Please select both X and Y columns.")
        return

    # Clear previous chart
    for widget in chart_frame.winfo_children():
        widget.destroy()
    current_canvas = None
    current_fig = None

    # Create figure
    fig, ax = plt.subplots(figsize=(7, 5), facecolor="#f4f4f4")

    try:
        if chart_type == "Bar Chart":
            ax.bar(data[x_col], data[y_col], color="#d6f0dd")
            ax.set_title(f"{y_col} by {x_col} (Bar Chart)", fontsize=14)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)

        elif chart_type == "Line Chart":
            ax.plot(data[x_col], data[y_col], marker='o', color="#C9E2F4")
            ax.set_title(f"{y_col} vs {x_col} (Line Chart)", fontsize=14)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)

        elif chart_type == "Pie Chart":
            ax.pie(data[y_col], labels=data[x_col], autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
            ax.set_title(f"{y_col} Distribution (Pie Chart)", fontsize=14)

        elif chart_type == "Scatter Plot":
            ax.scatter(data[x_col], data[y_col], color="#8b4211", s=100, edgecolor="black")
            ax.set_title(f"{y_col} vs {x_col} (Scatter Plot)", fontsize=14)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)

        # Display chart
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        current_canvas = canvas
        current_fig = fig

    except Exception as e:
        messagebox.showerror("❌ Error", f"Could not plot data:\n{e}")

# --- Function to clear chart ---
def clear_chart():
    global current_canvas, current_fig
    if current_canvas:
        for widget in chart_frame.winfo_children():
            widget.destroy()
        current_canvas = None
        current_fig = None

# --- Function to save chart as PNG ---
def save_chart():
    global current_fig
    if current_fig:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")])
        if file_path:
            current_fig.savefig(file_path)
            messagebox.showinfo("✅ Success", f"Chart saved successfully as:\n{file_path}")
    else:
        messagebox.showwarning("⚠️ No Chart", "Please generate a chart before saving.")

# --- Exit Application ---
def exit_app():
    root.destroy()

# --- UI Layout ---
title_label = tk.Label(root, text="📊 Data Visualization Dashboard", font=("Arial", 18, "bold"),
                       bg="#1e1e1e", fg="white")
title_label.pack(pady=10, fill="x")

# Load CSV Button
load_btn = tk.Button(root, text="📂 Load CSV File", bg="#e6a3b3", fg="white",
                     font=("Arial", 12, "bold"), width=20, command=load_csv)
load_btn.pack(pady=10)

# Chart Selection Frame
options_frame = tk.Frame(root, bg="#dbd4d4")
options_frame.pack(pady=10)

# Dropdowns for X and Y columns
x_var = tk.StringVar()
y_var = tk.StringVar()

tk.Label(options_frame, text="X-Axis:", bg="#dbd4d4", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
x_dropdown = ttk.Combobox(options_frame, textvariable=x_var, font=("Arial", 11), width=18, state="readonly")
x_dropdown.grid(row=0, column=1, padx=5)

tk.Label(options_frame, text="Y-Axis:", bg="#dbd4d4", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5)
y_dropdown = ttk.Combobox(options_frame, textvariable=y_var, font=("Arial", 11), width=18, state="readonly")
y_dropdown.grid(row=0, column=3, padx=5)

# Chart Type Dropdown
chart_type = tk.StringVar()
chart_dropdown = ttk.Combobox(options_frame, textvariable=chart_type, font=("Arial", 11), width=18, state="readonly")
chart_dropdown["values"] = ("Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot")
chart_dropdown.current(0)
chart_dropdown.grid(row=0, column=4, padx=10)

# Button Frame
button_frame = tk.Frame(root, bg="#dbd4d4")
button_frame.pack(pady=10)

btn_generate = tk.Button(button_frame, text="Generate Chart", bg="#76a3f1", fg="white",
                         font=("Arial", 12, "bold"), width=15,
                         command=lambda: draw_chart(chart_type.get()))
btn_generate.grid(row=0, column=0, padx=5)

btn_clear = tk.Button(button_frame, text="Clear Chart", bg="#605C5C", fg="white",
                      font=("Arial", 12, "bold"), width=15, command=clear_chart)
btn_clear.grid(row=0, column=1, padx=5)

btn_save = tk.Button(button_frame, text="Save Chart", bg="#00aa66", fg="white",
                     font=("Arial", 12, "bold"), width=15, command=save_chart)
btn_save.grid(row=0, column=2, padx=5)

btn_exit = tk.Button(button_frame, text="Exit", bg="#cc0000", fg="white",
                     font=("Arial", 12, "bold"), width=15, command=exit_app)
btn_exit.grid(row=0, column=3, padx=5)

# Chart Display Area
chart_frame = tk.Frame(root, bg="#f4e5e5", relief="sunken", bd=2)
chart_frame.pack(pady=20, fill="both", expand=True)

root.mainloop()
