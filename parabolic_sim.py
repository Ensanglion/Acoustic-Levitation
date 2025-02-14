import numpy as np
import matplotlib.pyplot as plt

# Constants
frequency = 80e3  # 80 kHz frequency
amplitude = 0.05  # Pa (pressure amplitude)
speed_of_sound = 343  # m/s
wavelength = speed_of_sound / frequency  # m
density = 2  # kg/m^3
cube_mass = 0.05  # kg
cube_area = 0.0001  # m^2
cube_width = 0.002  # m

# Time setup
time_duration = 0.005  # increased time duration for a longer simulation
time_steps = 100000  # increase number of steps for higher resolution
time = np.linspace(0, time_duration, time_steps)

# Wave properties
angular_frequency = 2 * np.pi * frequency
k = 2 * np.pi / wavelength

# Vectorized functions for pressure and net force
def pressure(x, t, offset=0):
    # Update to create a parabolic function for pressure that varies with time
    A = -amplitude / (wavelength / 2)**2  # Coefficient for x^2 (negative for downward opening)
    B = amplitude / (wavelength / 2)  # Linear coefficient to create a slope
    C = amplitude * (1 - (t / (time_duration / 2))**2) + 1  # Varying constant term based on time
    return A * x**2 + B * x + C

def net_force(x, t):
    # Calculate pressure difference across the cube
    pressure_front = pressure(x + cube_width / 2, t)
    pressure_back = pressure(x - cube_width / 2, t)
    pressure_diff = pressure_back - pressure_front  # Reverse the difference to reflect correct direction

    # Pressure-based force
    pressure_force = pressure_diff * cube_area

    # Combine forces (can comment one out if desired)
    return pressure_force

# Re-initialize variables for the new time frame
x = [0]  # Initial position (m) set slightly to the left of the minimum point of the parabolic function
v = 0.001  # Small initial velocity (m/s) to the right
dt = time_duration / time_steps

# Initialize variables for tracking min/max values during the loop
min_x, max_x = float('inf'), float('-inf')
min_pressure_front, max_pressure_front = float('inf'), float('-inf')
min_pressure_back, max_pressure_back = float('inf'), float('-inf')
min_force, max_force = float('inf'), float('-inf')

# Data storage for plotting
pressures_front = []
pressures_back = []
net_forces = []

# Compute position over time with the new time frame
for t in time:
    # Calculate the pressure at the front and back of the cube using the updated x positions
    pressure_front = pressure(x[-1] + cube_width / 2, t)
    pressure_back = pressure(x[-1] - cube_width / 2, t, offset=np.pi)
    pressures_front.append(pressure_front)
    pressures_back.append(pressure_back)

    F = net_force(x[-1], t)  # Net force on the cube
    a = F / cube_mass  # Acceleration

    x_new = x[-1] + v * dt + 0.5 * a * dt**2  # Position update
    x.append(x_new)

    net_forces.append(F)

    # Update min/max values during the loop
    min_x = min(min_x, x_new)
    max_x = max(max_x, x_new)
    min_pressure_front = min(min_pressure_front, pressure_front)
    max_pressure_front = max(max_pressure_front, pressure_front)
    min_pressure_back = min(min_pressure_back, pressure_back)
    max_pressure_back = max(max_pressure_back, pressure_back)
    min_force = min(min_force, F)
    max_force = max(max_force, F)

# Downsampling factor
downsample_factor = 100

# Downsampled time and data
time_downsampled = time[::downsample_factor]
x_downsampled = x[:-1:downsample_factor]
pressures_front_downsampled = pressures_front[::downsample_factor]
pressures_back_downsampled = pressures_back[::downsample_factor]
net_forces_downsampled = net_forces[::downsample_factor]

# Plot the results
plt.figure(figsize=(14, 10))

# Cube position
plt.subplot(3, 1, 1)
plt.plot(time_downsampled, x_downsampled, label='Cube Position')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Cube Position Over Time (80kHz)')
plt.legend(loc='upper left')
plt.grid()

# Pressures
plt.subplot(3, 1, 2)
plt.plot(time_downsampled, pressures_front_downsampled, label='Pressure Front')
plt.plot(time_downsampled, pressures_back_downsampled, linestyle='--', label='Pressure Back')
plt.xlabel('Time (s)')
plt.ylabel('Pressure (Pa)')
plt.title('Pressures at Front and Back of Cube (80kHz)')
plt.legend(loc='upper left')
plt.grid()

# Net Force
plt.subplot(3, 1, 3)
plt.plot(time_downsampled, net_forces_downsampled, color='purple', label='Net Force on Cube')
plt.xlabel('Time (s)')
plt.ylabel('Force (N)')
plt.title('Net Force on Cube Over Time (80kHz)')
plt.legend(loc='upper left')
plt.grid()

# Adjust subplot spacing
plt.subplots_adjust(hspace=0.4, wspace=0.3)

# Show the plot
plt.show()