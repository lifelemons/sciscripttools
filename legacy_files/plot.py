import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib.ticker as ticker
import sciscripttools as st
import co2
import utility

fig_params = st.figure_parameters() # generate parameters
fig_params.brackets = 'square'
st.standard_font(font_size = fig_params.font_size) # standarise the font
marker_size = 10

def sort_xy_axes(sf, axes, x, y):
    
    # show pressure in units of Mega Pascal
    scale_y = 1e6
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
    for ax in axes:
        ax.yaxis.set_major_formatter(ticks_y)
        #sf.ylabel(ax, ylabel, yunit) # no longer label each axis, use fig.supylabel()
        
    # add units
    ylabel = "Pressure"; yunit = "\\mega\\pascal"
    sf.fig.supylabel("{} {}".format(ylabel, sf.latex_unit(yunit, fig_params.brackets)), x=0.06)

    xlabel = "Temperature"; xunit = "\\kelvin"
    sf.xlabel(axes[-1], xlabel, xunit)
    
    # when using this utility.add_min_max_points(), must set axis for nice plots
    # to avoid the odd points at (-1000, -1000)
    for ax in axes:
        ax.set_xlim([240, np.max(x)])
        ax.set_ylim([0.0, np.max(y)])
    
    return

def volume_label(sf):

    label = "Volume"
    unit = ("\\metre\\cubed")
    volume_string = "{} {}".format(label, sf.latex_unit(unit, sf.fig_params.brackets))
    
    return volume_string

def density_label(sf):
    
    label = "Density"
    unit = ("\\kilogram\\per\\metre\\cubed")
    denisty_string = "{} {}".format(label, sf.latex_unit(unit, sf.fig_params.brackets))
    
    return denisty_string


def add_co2_lines(axes):
    
    for ax in axes:
        co2.plot_vapourisation_condensation_pressure_line(ax)
    
    return

def scatter_n_separate(data):
    
    number_of_sets = len(data)
    
    fig, axes = plt.subplots(nrows=number_of_sets, ncols=1, sharex=True)
    if number_of_sets == 1:
        axes = np.array([axes])
    
    scatter_plots = []
    for i in range(0, number_of_sets):
        x, y, z = data[i]
        ax = axes.ravel().tolist()[i]
        scatter_plot_i = ax.scatter(x, y, c = z, cmap='Spectral', s = marker_size)
        scatter_plots.append(scatter_plot_i)
            
    add_co2_lines(axes)
    
    fig.subplots_adjust(hspace = 0.3) # set subplot width spacing
    sf = st.standard_figure(fig, axes, fig_params) # create standard_figure
    
    cbars = []
    for i in range(0, number_of_sets):
        cbar_i = fig.colorbar(scatter_plots[i], ax=axes.ravel().tolist()[i], pad = 0.05)
        cbars.append(cbar_i)
    
    x, y, z = data[0]
    sort_xy_axes(sf, axes, x, y)
    
    return sf, cbars   

def share_minmax_data(data):
    
    number_of_sets = len(data)
    
    data_p = data
    if (number_of_sets == 2):
        x1, y1, z1 = data[0]
        x2, y2, z2 = data[1]
        x1_p, y1_p, z1_p, x2_p, y2_p, z2_p = utility.add_min_max_points(x1, y1, z1, x2, y2, z2)
        data_p[0] = [x1_p, y1_p, z1_p]
        data_p[1] = [x2_p, y2_p, z2_p]
        
    if (number_of_sets == 3):
        x1, y1, z1 = data[0]
        x2, y2, z2 = data[1]
        x3, y3, z3 = data[2]
        x1_p, y1_p, z1_p, x2_p, y2_p, z2_p, x3_p, y3_p, z3_p = utility.add_min_max_points_3plots(x1, y1, z1, x2, y2, z2, x3, y3, z3)
        data_p[0] = [x1_p, y1_p, z1_p]
        data_p[1] = [x2_p, y2_p, z2_p]
        data_p[2] = [x3_p, y3_p, z3_p]
    
    return data_p

def scatter_normals_errors(data_normal, data_errors):
    
    number_of_normal_plots = len(data_normal)
    number_of_error_plots = len(data_errors)
    total_number_of_plots = number_of_normal_plots + number_of_error_plots
    
    data_normal_p = share_minmax_data(data_normal)
    data_errors_p = share_minmax_data(data_errors)

    fig, axes = plt.subplots(nrows=total_number_of_plots, ncols=1, sharex=True, sharey=True)
    if (total_number_of_plots == 1):
        axes = np.array([axes])
    
    scatter_plots_normal = []
    for i in range(0, number_of_normal_plots):
        x, y, z = data_normal_p[i]
        ax = axes.ravel().tolist()[i]
        scatter_plot_i = ax.scatter(x, y, c = z, cmap='Spectral', s = marker_size)
        scatter_plots_normal.append(scatter_plot_i)
    
    print(scatter_plots_normal)
    scatter_plots_error = []
    for i in range(0, number_of_error_plots):
        x, y, z = data_errors_p[i]
        ax = axes.ravel().tolist()[i + number_of_normal_plots]
        scatter_plot_i = ax.scatter(x, y, c = z, cmap='Reds', s = marker_size)
        scatter_plots_error.append(scatter_plot_i)      

    add_co2_lines(axes)
        
    fig.subplots_adjust(hspace = 0.2) # set subplot width spacing
    sf = st.standard_figure(fig, axes, fig_params) # create standard_figure

    aspect_normal = 30
    aspect_error = 30
    if (total_number_of_plots == 3):
        if ((number_of_normal_plots == 1) & (number_of_error_plots == 2)):
            aspect_normal = 15
            aspect_error = 30
            
        if ((number_of_normal_plots == 2) & (number_of_error_plots == 1)):
            aspect_normal = 30
            aspect_error = 15
    
    cbar_n = 0
    if (number_of_normal_plots > 0):
        cbar_n = fig.colorbar(scatter_plots_normal[0], ax=axes.ravel().tolist()[0:number_of_normal_plots], pad = 0.1, aspect=aspect_normal)

    cbar_e = 0
    if (number_of_error_plots > 0):
        cbar_e = fig.colorbar(scatter_plots_error[0], ax=axes.ravel().tolist()[0 + number_of_normal_plots:total_number_of_plots], pad = 0.1, aspect=aspect_error)

    if (number_of_normal_plots > 0):
        x, y, z = data_normal_p[0]
        sort_xy_axes(sf, axes, x, y)
    elif (number_of_error_plots > 0):
        x, y, z = data_errors_p[0]
        sort_xy_axes(sf, axes, x, y)

    sf.add_subplot_labels_right(adjust_x=0.56)
    
    cbars = None
    if (cbar_n == 0):
        cbars = [cbar_e]
    elif (cbar_e == 0):
        cbars = [cbar_n]
    else:
        cbars = [cbar_n, cbar_e]

    return sf, cbars


def set_titles(axes, titles):
    for pair in zip(axes, titles):
        pair[0].set_title(pair[1])
        
def set_cbar_labels(cbars, labels):
    for pair in zip(cbars, labels):
        pair[0].set_label(pair[1])
        

def historgrams(x_array, n = 0):
    
    fig, axes = plt.subplots(nrows=len(x_array), sharex=True)
    
    if len(x_array) == 1:
        axes = [axes]
    
    for i in range(0, len(x_array)):
        
        if n == 0:
            n = len(x_array[i])
        
        axes[i].hist(x_array[i], weights = np.ones(len(x_array[i])) / n, bins = 100, cumulative = True)
    
    fig.subplots_adjust(hspace = 0.3) # set subplot width spacing
    sf = st.standard_figure(fig, axes, fig_params) # create standard_figure
    
    for ax in axes:
        ax.set_ylabel("Count")
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_ylim([0, 1])
    
    return sf

def scatter_3d(x, y, z, step = 1):
    # step changes the density of points
    
    # subset points
    n = len(x)
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(x[1:n:step], y[1:n:step], z[1:n:step], alpha=0.4)

    # critical temperature plane
    co2.plot_critical_temperature_plane(ax, y, z)
    co2.plot_critical_pressure_plane(ax, x, z)
    co2.plot_critical_point(ax)

    # add units
    sf = st.standard_figure(fig, ax, fig_params) # create standard_figure
    
    sort_xy_axes(sf, [ax], x, y)
    
    return sf


def add_vertical_line_with_text(ax, x_point, text):
       
    ax.axvline(x_point, linestyle = "--", color = 'orange')
    ax.text(x_point, 0.1, s = text, c='orange')
    
    return

def error_histogram(ax, x):
    
    ax.hist(x, weights = np.ones(len(x)) / len(x), bins = 100, cumulative = True)

    ax.set_ylabel("Count")
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.set_ylim([0, 1])
    
    xlim_lower = np.min(x)
    xlim_upper = np.max(x)
    
    if (np.abs(xlim_lower - xlim_upper) <= 0.5):
        xlim_upper = xlim_upper + 1.0
        
    if (xlim_upper <= 0.0):
        xlim_upper = 0.0 + 0.2
    
    add_vertical_line_with_text(ax, -3.0, "0.1$\%$")
    add_vertical_line_with_text(ax, -2.0, "1$\%$")
    add_vertical_line_with_text(ax, -1.0, "10$\%$")
    add_vertical_line_with_text(ax, 0.0, "100$\%$")
    add_vertical_line_with_text(ax, 1.0, "1000$\%$")
    
    ax.set_xlim([xlim_lower, xlim_upper])
    ax.set_xlabel("Log Percentage Error")
    
    return

def fit_analysis(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
    
    x1_p, y1_p, z1_p, x2_p, y2_p, z2_p, x3_p, y3_p, z3_p = utility.add_min_max_points_3plots(x1, y1, z1, x2, y2, z2, x3, y3, z3)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(5, 1, 1)
    ax2 = fig.add_subplot(5, 1, 2, sharex = ax1, sharey = ax1)
    ax3 = fig.add_subplot(5, 1, 3, sharex = ax1, sharey = ax1)
    ax4 = fig.add_subplot(5, 1, 4, sharex = ax1, sharey = ax1)
    ax5 = fig.add_subplot(5, 1, 5)
    axes = np.array([ax1, ax2, ax3, ax4, ax5])
    
    scatter_plot_a = ax1.scatter(x1_p, y1_p, c = z1_p, cmap='Spectral', s = marker_size)
    scatter_plot_b = ax2.scatter(x2_p, y2_p, c = z2_p, cmap='Spectral', s = marker_size)
    scatter_plot_c = ax3.scatter(x3_p, y3_p, c = z3_p, cmap='Spectral', s = marker_size)
    scatter_plot_d = ax4.scatter(x4, y4, c = z4, cmap='Reds', s = marker_size)
    error_histogram(ax5, z4)
    
    add_co2_lines(axes)
    
    fig.subplots_adjust(hspace =  0.2) # set subplot width spacing
    sf = st.standard_figure(fig, axes, fig_params) # create standard_figure
    cbar_a = fig.colorbar(scatter_plot_a, ax=[axes.ravel().tolist()[0], axes.ravel().tolist()[1], axes.ravel().tolist()[2]], pad = 0.1)
    cbar_d = fig.colorbar(scatter_plot_d, ax=[axes.ravel().tolist()[3]], pad = 0.1)
    cbars = [cbar_a, cbar_d]
    
    sort_xy_axes(sf, axes[0:4], x1, y1)
            
    ax1.set_title("NIST")
    ax2.set_title("Section To Fit")
    ax3.set_title("Calculated Surface")
    ax4.set_title("Log Percentage Error")
        
    xlabel = "Temperature"; xunit = "\\kelvin"
    sf.xlabel(ax4, xlabel, xunit)
    
        
    
    return sf, cbars


