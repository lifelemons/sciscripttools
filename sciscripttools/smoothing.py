import numpy as np
import matplotlib.pyplot as plt
import logging

# setup logging
logger = logging.getLogger(__name__)

def generate_smoothed_data_report(data):

    
    ## Compute the smoothed data
    # with a basic filter

    smoothed_datum = 0
    factor = 20
    smoothed_data = []
    for value in data:
        smoothed_datum += (value - smoothed_datum) / factor
        smoothed_data.append(smoothed_datum)
        
    smoothed_data = np.array(smoothed_data)

    ## Compute error

    error = data - smoothed_data
    error_percentage = (error / data) * 100.0

    stable_data_range = -1000 # to end
    error_average = np.average(np.abs(error[stable_data_range:]))
    error_percentage_average = np.average(np.abs(error_percentage[stable_data_range:]))

    print("Average percentage error: {:.2f}%".format(error_percentage_average))

    ## Compute stats

    # consider x as time
    num_samples = np.size(data)
    end_time = 0 + 0.035 * (num_samples - 1)
    time = np.linspace(0, end_time, num_samples)


    def moving_average(data, window_size):    
        weights = np.ones(window_size) / window_size
        return np.convolve(data, weights, mode='valid')


    # 15 * 0.035 = 0.500 ish, ie. half a second
    moving_average_error_percentage = moving_average(np.abs(error_percentage), 15)

    time_to_average_error = time[np.where(moving_average_error_percentage < error_percentage_average)[0][0]]

    print("Time to achieve value within average error: {:.2f}s".format(time_to_average_error))

    smoothed_data_std_dev = np.std(error_percentage)

    print("Smoothed Data stand deviation: {:.5f}".format(smoothed_data_std_dev))


    ## Plot

    # plot
    fig, axes = plt.subplots(3, 1, sharex = True) # create matplotlib figure
    ax1, ax2, ax3 = axes
    ax1.plot(time, data)
    ax1.plot(time, smoothed_data)

    ax2.plot(time, error)
    ax3.plot(time, error_percentage)

    # refine plot
    fig_params = st.figure_parameters() # generate parameters
    st.standard_font(font_size = fig_params.font_size) # standarise the font
    sf = st.standard_figure(fig, axes, fig_params) # create standard_figure

    # add units
    xlabel = "Time"; xunit = "\\second"
    sf.xlabel(ax3, xlabel, xunit)
    ax1.set_ylabel("Data")
    ax2.set_ylabel("Absolute Error")
    ax3.set_ylabel("Percentage Error")


    ax1.set_ylim(np.min(data)*0.98, np.max(data)*1.02)
    ax2.set_ylim(-standard_deviation*3, standard_deviation*3)
    ax3.set_ylim(-error_percentage_average*10, error_percentage_average*10)

    for ax in axes:
        ax.axvline(x=time_to_average_error, color='r', linestyle='-', linewidth=2)

    plt.show()
        


