import numpy as np
import matplotlib.pyplot as plt

# helper functions

def convert_K_to_F(temperature_K):
    temperature_F = (temperature_K - 273.15)* 1.8 + 32.0
    return temperature_F

def convert_F_to_K(temperature_F):
    temperature_K = (temperature_F + 459.67) * 5.0/9.0
    return temperature_K

def convert_psig_to_pascal(pressure_psig):
    
    pressure_psia = pressure_psig + 14.696
    pressure_bar = pressure_psia / 14.503773800722
    pressure_pascal = pressure_bar * 100000.0

    return pressure_pascal


# to allow for the same range in the colour bar
def add_min_max_points(x1, y1, z1, x2, y2, z2):

    x1_output = x1
    y1_output = y1
    z1_output = z1
    
    x2_output = x2
    y2_output = y2
    z2_output = z2
        
    # need to add four points to each array
    # for each min, max of the two z arrays
    
    xys = [x1_output, y1_output, x2_output, y2_output]
    
    for i in range(0, len(xys)):
        for j in range(0, 4):
            xys[i] = np.append(xys[i], -1000) 

    # add all min max of  ranges to each other, so that when the error is computed, they cancel out
    z_outputs = [z1_output, z2_output]
    z_inputs = [z1, z2]
    for i in range(0, len(z_outputs)):
        for j in range(0, len(z_inputs)):
            z_outputs[i] = np.append(z_outputs[i], np.min(z_inputs[j]))
            z_outputs[i] = np.append(z_outputs[i], np.max(z_inputs[j]))
    
    x1_output = xys[0]
    y1_output = xys[1]
    z1_output = z_outputs[0]
    
    x2_output = xys[2]
    y2_output = xys[3]
    z2_output = z_outputs[1]
            
    return x1_output, y1_output, z1_output, x2_output, y2_output, z2_output

def add_min_max_points_3plots(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    
    x1_output = x1
    y1_output = y1
    z1_output = z1
    
    x2_output = x2
    y2_output = y2
    z2_output = z2
    
    x3_output = x3
    y3_output = y3
    z3_output = z3
    
    # need to add six points to each array
    # for each min, max of the two z arrays
    
    xys = [x1_output, y1_output, x2_output, y2_output, x3_output, y3_output]
    
    for i in range(0, len(xys)):
        for j in range(0, 6):
            xys[i] = np.append(xys[i], -1000) 

    # add all min max of  ranges to each other, so that when the error is computed, they cancel out
    z_outputs = [z1_output, z2_output, z3_output]
    z_inputs = [z1, z2, z3]
    for i in range(0, len(z_outputs)):
        for j in range(0, len(z_inputs)):
            z_outputs[i] = np.append(z_outputs[i], np.min(z_inputs[j]))
            z_outputs[i] = np.append(z_outputs[i], np.max(z_inputs[j]))
    
    x1_output = xys[0]
    y1_output = xys[1]
    z1_output = z_outputs[0]
    
    x2_output = xys[2]
    y2_output = xys[3]
    z2_output = z_outputs[1]
    
    x3_output = xys[4]
    y3_output = xys[5]
    z3_output = z_outputs[2]
    
    return x1_output, y1_output, z1_output, x2_output, y2_output, z2_output, x3_output, y3_output, z3_output


def bound_array(x, lower_bound, upper_bound):
    
    x_bounded = x
    
    x_bounded[np.where(x_bounded > upper_bound)] = upper_bound 
    x_bounded[np.where(x_bounded < lower_bound)] = lower_bound
    
    return x_bounded

def bound_data(x, y, z, lower_bound, upper_bound):
    
    bounded_indices = np.where((z <= upper_bound) & (z >= lower_bound))[0]
    x_output = x[bounded_indices]
    y_output = y[bounded_indices]
    z_output = z[bounded_indices] 
    
    return x_output, y_output, z_output

def bound_data_indices(x, y, z, indices):
    
    x_output = x[indices]
    y_output = y[indices]
    z_output = z[indices] 
    
    return x_output, y_output, z_output 

# add a rectangle, with text in the middle
# (x1, y1) bottom left corner and # (x2, y2) top right corner of the rectangle
def add_zone(ax, x1, y1, x2, y2, text):

    xdiff = x2 - x1
    ydiff = y2 - y1
    
    zone = plt.Rectangle((x1,y1), xdiff, ydiff, fc='grey',ec="grey", alpha=0.4)
    ax.add_patch(zone)
    
    x_mid_point = x1 + xdiff/2.0
    y_mid_point = y1 + ydiff/2.0
    
    ax.text(x_mid_point*0.99, y_mid_point*0.98, text, c='white')
    return

def compute_log_percentage_error(a, b):
    
    absolute_error = np.abs(a - b)
    absolute_error[np.where(absolute_error == 0.0)] = 1e-16
    
    adjusted_a = a
    if len(a[np.where(a == 0.0)]) > 1:
        adjusted_a[np.where(a == 0.0)] = 1e-16
        
    error = np.log10(np.abs(absolute_error / adjusted_a))

        
    return error