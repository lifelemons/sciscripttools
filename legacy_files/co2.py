
import numpy as np
import matplotlib.pyplot as plt
import utility


# co2 properites
molecular_weight = 44.01 # co2 44.01 g/mol
molecular_weight_kg_per_mol = molecular_weight / 1000.0 # ideal gas law formular requires units of kg/mol

moles_per_kg = 1 / molecular_weight_kg_per_mol

critical_point = [304.25, 7390000] # [Kelvin, Pa]
triple_point = [216.55, 520000] # [Kelvin, Pa]

# plot the CO2 properities

# critical temperature plane
def plot_critical_temperature_plane(ax, y, z):
    ys = np.linspace(np.min(y), np.max(y), 100)
    zs = np.linspace(np.min(z), np.max(z), 100)

    Y, Z = np.meshgrid(ys, zs)
    X = critical_point[0] + Y*0
    
    ax.plot_surface(X, Y, Z, alpha=0.2)
    
    return
    
# critical temperature plane
def plot_critical_pressure_plane(ax, x, z):
    xs = np.linspace(np.min(x), np.max(x), 100)
    zs = np.linspace(np.min(z), np.max(z), 100)

    X, Z = np.meshgrid(xs, zs)
    Y = critical_point[1] + X*0
    
    ax.plot_surface(X, Y, Z, alpha=0.2)
    
    return

def plot_critical_point(ax):
    
    ax.scatter(critical_point[0], critical_point[1], s=30)
    
    return

# equation pulled from FLASH.CPP
def co2_vapourisation_condensation_pressure(temperature_F):
    
    pressure_psig = 1.1635637728E-08*np.power(temperature_F, 5) \
                    - 1.6992139721E-06*np.power(temperature_F, 4) \
                    + 1.9013071825E-04*np.power(temperature_F, 3) \
                    + 2.8833919357E-02*np.power(temperature_F, 2) \
                    + 5.1692662848E+00*temperature_F \
                    + 3.0568236164E+02 - 14.696
    
    return pressure_psig

# temp in kelvin, output pressure in pascal
def vapourisation_condensation_pressure(temperature):

    pressure = utility.convert_psig_to_pascal(co2_vapourisation_condensation_pressure(utility.convert_K_to_F(temperature)))
    
    return pressure 

def vapourisation_condensation_pressure_line(temperatures):

    pressures = np.full(0, 0.0)
    for temperature in temperatures:
        pressure = vapourisation_condensation_pressure(temperature)
        pressures = np.append(pressures, pressure)
    
    return pressures

def plot_vapourisation_condensation_pressure_line(ax):
    
    x = np.linspace(triple_point[0], critical_point[0], 25)
    y = vapourisation_condensation_pressure_line(x)

    ax.plot(x, y, c='grey', linewidth=2.5, solid_capstyle='round')       
    ax.plot(x, y, c='white', linewidth=2, solid_capstyle='round')
    
    return 