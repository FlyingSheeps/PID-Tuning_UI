import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import control.matlab as mt
import numpy as np

def plot_all():
    # Get numerator and denominator from entry widgets
    numerator_str = numerator_entry.get()
    denominator_str = denominator_entry.get()

    # Convert input strings to lists of coefficients
    numerator_coeffs = list(map(float, numerator_str.split(',')))
    denominator_coeffs = list(map(float, denominator_str.split(',')))

    # Define the transfer function
    system = mt.TransferFunction(numerator_coeffs, denominator_coeffs)

    # Generate frequency values for the Bode plot
    frequency = np.logspace(-1, 2, 1000)

    # Calculate magnitude and phase
    magnitude, phase, omega = mt.bode(system, frequency)

    # Create a Bode plot
    magnitude_subplot.clear()
    phase_subplot.clear()
    magnitude_subplot.semilogx(omega, 20*np.log10(magnitude))
    magnitude_subplot.set_title('G')
    magnitude_subplot.set_ylabel('Magnitude (dB)')
    magnitude_subplot.grid(True, which='both', linestyle='--', linewidth=0.5)

    phase_subplot.semilogx(omega, np.degrees(phase))  # Display phase in degrees
    phase_subplot.set_xlabel('Frequency (rad/s)')
    phase_subplot.set_ylabel('Phase (degrees)')
    phase_subplot.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Create a W controller with gains from the widget
    kp = float(kp_entry.get())
    ki = float(ki_entry.get())
    kd = float(kd_entry.get())

    KP = mt.TransferFunction([1], [1])*kp
    KD = mt.TransferFunction([1, 0], [1])*kd
    KI = mt.TransferFunction([1], [1, 0])*ki

    W = (KP+KI)*system/(1+system*KD)

    # Calculate magnitude and phase for W controller
    W_magnitude, W_phase, W_omega = mt.bode(W, frequency)

    # Add W controller plot to the figure
    W_magnitude_subplot.semilogx(W_omega, 20*np.log10(W_magnitude))
    W_magnitude_subplot.set_title('W')
    W_magnitude_subplot.set_ylabel('Magnitude (dB)')
    W_magnitude_subplot.grid(True, which='both', linestyle='--', linewidth=0.5)
    W_magnitude_subplot.axhline(y=0, color='r', linestyle='--', label='Gain 0 dB')

    W_phase_subplot.semilogx(W_omega, np.degrees(W_phase))  # Display phase in degrees
    W_phase_subplot.set_xlabel('Frequency (rad/s)')
    W_phase_subplot.set_ylabel('Phase (degrees)')
    W_phase_subplot.grid(True, which='both', linestyle='--', linewidth=0.5)
    W_phase_subplot.axhline(y=-180, color='r', linestyle='--', label='Phase -180 degrees')

    # Plot Bode function and its step response
    Gyr = system*(KP+KI)/(1+system*(KP+KI+KD))
    Gyr_magnitude, Gyr_phase, Gyr_omega = mt.bode(Gyr, frequency)

    Gyr_magnitude_subplot.semilogx(Gyr_omega, 20*np.log10(Gyr_magnitude))
    Gyr_magnitude_subplot.set_title('Gyr')
    Gyr_magnitude_subplot.set_ylabel('Magnitude (dB)')
    Gyr_magnitude_subplot.grid(True, which='both', linestyle='--', linewidth=0.5)

    Gyr_phase_subplot.semilogx(Gyr_omega, np.degrees(Gyr_phase))  # Display phase in degrees
    Gyr_phase_subplot.set_xlabel('Frequency (rad/s)')
    Gyr_phase_subplot.set_ylabel('Phase (degrees)')
    Gyr_phase_subplot.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Calculate step response
    response, time = mt.step(Gyr)

    # Create a step plot
    step_subplot.plot(time, response)
    step_subplot.set_title('R to Y Step Response')
    step_subplot.set_xlabel('Time')
    step_subplot.set_ylabel('Amplitude')
    step_subplot.grid(True, linestyle='--', linewidth=0.5)

    # Create a canvas to display the plot
    canvas1.draw()
    canvas2.draw()
    canvas3.draw()
    canvas4.draw()

def clear_all():

    # Clear
    magnitude_subplot.clear()
    phase_subplot.clear()
    W_magnitude_subplot.clear()
    W_phase_subplot.clear()
    Gyr_magnitude_subplot.clear()
    Gyr_phase_subplot.clear()
    step_subplot.clear()

    # Redraw
    canvas1.draw()
    canvas2.draw()
    canvas3.draw()
    canvas4.draw()



# Create the main window
window = tk.Tk()
window.title("PID-tune")

# Input Frame
input_frame = ttk.Frame(window)
input_frame.grid(row=0, column=0, padx=10, pady=10)

numerator_label = ttk.Label(input_frame, text="Numerator:")
numerator_label.grid(row=0, column=0, pady=5)
numerator_entry = ttk.Entry(input_frame)
numerator_entry.grid(row=0, column=1, pady=5)

denominator_label = ttk.Label(input_frame, text="Denominator:")
denominator_label.grid(row=0, column=2, pady=5)
denominator_entry = ttk.Entry(input_frame)
denominator_entry.grid(row=0, column=3, pady=5)

kp_label = ttk.Label(input_frame, text="KP:")
kp_label.grid(row=1, column=0, pady=5)
kp_entry = ttk.Entry(input_frame)
kp_entry.grid(row=1, column=1, pady=5)

ki_label = ttk.Label(input_frame, text="KI:")
ki_label.grid(row=1, column=2, pady=5)
ki_entry = ttk.Entry(input_frame)
ki_entry.grid(row=1, column=3, pady=5)

kd_label = ttk.Label(input_frame, text="KD:")
kd_label.grid(row=1, column=4, pady=5)
kd_entry = ttk.Entry(input_frame)
kd_entry.grid(row=1, column=5, pady=5)

# Buttons frame
button_frame = ttk.Frame(window)
button_frame.grid(row=1, column=0, padx=5, pady=5)
# Button to trigger the plot
plot_button = ttk.Button(button_frame, text="Plot", command=plot_all)
plot_button.grid(row=0, column=0, pady=5)

clear_button = ttk.Button(button_frame, text="clear", command=clear_all)
clear_button.grid(row=0, column=1, pady=5)

# Plot Frame
plot_frame = ttk.Frame(window)
plot_frame.grid(row=3, column=0, padx=5, pady=5)

# Create three separate figures in the canvas
figure1 = Figure(figsize=(4.3, 4.3))
magnitude_subplot = figure1.add_subplot(2, 1, 1)
phase_subplot = figure1.add_subplot(2, 1, 2)

figure2 = Figure(figsize=(4.3, 4.3))
W_magnitude_subplot = figure2.add_subplot(2, 1, 1)
W_phase_subplot = figure2.add_subplot(2, 1, 2)

figure3 = Figure(figsize=(4.3, 4.3))
Gyr_magnitude_subplot = figure3.add_subplot(2, 1, 1)
Gyr_phase_subplot = figure3.add_subplot(2, 1, 2)

figure4 = Figure(figsize=(4.3, 4.3))
step_subplot = figure4.add_subplot(1, 1, 1)

# Adjust layout parameters to extend the figure region
figure1.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.15)
figure2.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.15)
figure3.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.15)
figure4.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.15)

# Create a canvas to display the plot
canvas1 = FigureCanvasTkAgg(figure1, master=plot_frame)
canvas1_widget = canvas1.get_tk_widget()
canvas1_widget.grid(row=0, column=0, padx=1, pady=1)

canvas2 = FigureCanvasTkAgg(figure2, master=plot_frame)
canvas2_widget = canvas2.get_tk_widget()
canvas2_widget.grid(row=0, column=1, padx=1, pady=1)

canvas3 = FigureCanvasTkAgg(figure3, master=plot_frame)
canvas3_widget = canvas3.get_tk_widget()
canvas3_widget.grid(row=1, column=0, padx=1, pady=1)

canvas4 = FigureCanvasTkAgg(figure4, master=plot_frame)
canvas4_widget = canvas4.get_tk_widget()
canvas4_widget.grid(row=1, column=1, padx=1, pady=1)



# Run the Tkinter main loop
window.mainloop()
