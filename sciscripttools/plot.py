import numpy as np
import json
import logging
import pprint

import matplotlib
import matplotlib.pyplot as plt
# for the standard_font class
from matplotlib import rc
# for the FixedOrderFormatter class
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

# import .plot_defaults
from .io import save_data
from .plot_defaults import fig_params_report

logger = logging.getLogger(__name__)

class FixedOrderFormatter(ScalarFormatter):
    """
    Formats axis ticks using scientific notation with a constant order of 
    magnitude
    
    E.g. usage:
    ax.yaxis.set_major_formatter(FixedOrderFormatter(-2)) # displays as 10^(-2)
    """
    def __init__(self, order_of_mag=0, useOffset=True, useMathText=False):
        self._order_of_mag = order_of_mag
        ScalarFormatter.__init__(self, useOffset=useOffset, 
                                 useMathText=useMathText)
    def _set_orderOfMagnitude(self, range):
        """Over-riding this to avoid having orderOfMagnitude reset elsewhere"""
        self.orderOfMagnitude = self._order_of_mag    

class figure_parameters:
    """
    Object to store all the default figure parameters.

    A dictionary can be:
    - auto generated from plot_defaults.py.
    - passed in as a dict object
    - read in from a file, by providing a filename when initialising the object.

    The parameters can also be outputed to a dictionary and also saved to a
    json file.

    Note: 
    - Note all variables need to be defined; however some methods of
    standard_figure class may fail as they do not have any defaults.
    - When a class variable is updated, the stored dictionary is not 
    automatically updated. 

    Methods
    -------
    __init__(self, parameters=fig_params_report) : initialisation
        Generate a figure_parameters object either using the default from 
        plot_defaults.py, a user given dictionary, or a json file.
    create_dictionary(self)
        Generate a dictionary object of the variables.
    update_dictionary(self)
        Update the parameters_dictionary with the current values. 
    save_data(self, filename, directory="")
        Update and output the parameters_dictionary to a json file.
        This allows the parameters to be loaded in for another figure.

    Class Variables
    ---------------
    parameters_dictionary : dict
        The original parameter dictionary
    font_size : float
        Font size for the figure.
    width : float
        Width of the figure in inches.
    ratio : float
        Ratio of the width and height.
    height : float
        Height of the figure in inches.
    height_small_percentage : float
        Fractional percentage to define the standard size for small plots.
    
    adjust_bottom : float
        Adjust the bottom padding.
    adjust_left : float
        Adjust the left side padding.
    adjust_subplot_bottom : float
        Adjust the bottom padding for figures with multiple subplots and thus
        subplot labels.
    adjust_subplot_label : float
        Adjust the location of the labels for the subplots.
    adjust_subplot_wspace : float
        Adjust the width spacing between subplots.
    adjust_subplot_hspace : float
        Adjust the height spacing between subplots.

    adjust_subplot_label_right_x : float
        For labels on the right hand side of the figure, 
        adjust the x location of subplot labels.
    adjust_subplot_label_right_y : float
        For labels on the right hand side of the figure, 
        adjust the y location of subplot labels.
    
    schematic_adjust_bottom_no_ticks : float
        For figures with no ticks, adjust the padding such that the
        labels match with the location of a plot with ticks.
        Note the effective plot area is bigger on these plots.

    brackets : "round", "square"
        The style of brackets to use around the unit.
        "round" (unit)
        "square" [unit] 
    """
        
    def __init__(self, parameters=fig_params_report):
        
        def load_parameter(parameter):
            """
            Try and load the parameter from the dictionary.
            """
            value = None
            try:
                value = self.parameters_dictionary[parameter]
            except: 
                logger.info("Could not load {}.".format(parameter))

            return value
    
        # if given a string, try and load the string
        if isinstance(parameters, str):
            try:
                parameters = json.load(open(parameters))
            except:
                logger.info("parameters was a string, {}, could not load.".format(parameter))

        if not isinstance(parameters, dict):
            raise Exception("Expecting a dictionary or parameters.")
        
        # store dictionary
        self.parameters_dictionary = parameters
        
        self.font_size = load_parameter("font_size")

        # default dimensional properties
        self.width = load_parameter("width")
        self.ratio = load_parameter("ratio")
        self.height = load_parameter("height")

        # 0 <= x < 1, fractional percentage of the default height for a smaller plot
        self.height_small_percentage = load_parameter("height_small_percentage")

        # default figure adjustments
        self.adjust_bottom = load_parameter("adjust_bottom")
        self.adjust_left = load_parameter("adjust_left")
        self.adjust_subplot_bottom = load_parameter("adjust_subplot_bottom")
        self.adjust_subplot_label = load_parameter("adjust_subplot_label")
        self.adjust_subplot_wspace = load_parameter("adjust_subplot_wspace")
        self.adjust_subplot_hspace = load_parameter("adjust_subplot_hspace")

        # for subplot labels on the right hand side
        self.adjust_subplot_label_right_x = load_parameter("adjust_subplot_label_right_x")
        self.adjust_subplot_label_right_y = load_parameter("adjust_subplot_label_right_y")

        self.schematic_adjust_bottom_no_ticks = load_parameter("schematic_adjust_bottom_no_ticks")

        self.brackets = load_parameter("brackets")
        
        return
    
    def __repr__(self):
        return pprint.pformat(self.parameters_dictionary)
    
    def create_dictionary(self):
        parameters = {
                "font_size"  : self.font_size,

                "width" : self.width,      
                "ratio" : self.ratio,
                "height" : self.height,
                "height_small_percentage" : self.height_small_percentage,

                "adjust_bottom" : self.adjust_bottom,
                "adjust_left" : self.adjust_left,
                "adjust_subplot_bottom" : self.adjust_subplot_bottom,
                "adjust_subplot_label" : self.adjust_subplot_label,
                "adjust_subplot_wspace" : self.adjust_subplot_wspace,
                "adjust_subplot_hspace" : self.adjust_subplot_hspace,

                "schematic_adjust_bottom_no_ticks" : self.schematic_adjust_bottom_no_ticks,

                "adjust_subplot_label_right_x" : self.adjust_subplot_label_right_x,
                "adjust_subplot_label_right_y" : self.adjust_subplot_label_right_y,

                "brackets" : self.brackets
                }
        return parameters
    
    def update_dictionary(self):
        parameters = self.create_dictionary()
        self.parameters_dictionary = parameters
        return 0
    
    def save_data(self, filename, directory=""):
        """
        Export the default values to a json file.
        """
        self.update_dictionary()
        save_data(filename, self.parameters_dictionary, directory = directory)
        return 0

class standard_font:
    """
    Standardise the figure fonts.

    Methods
    -------
     __init__(self, font_size=12) : initialisation
        Set the font to use LaTeX and standardise the font sizes within a figure.
    set_font(self)
        Set the font to use LaTeX.
    set_font_size(self, font_size=None)
        Standardise the font sizes within a figure.
    """

    def __init__(self, font_size=12):

        self.font_size = font_size
        
        # standardise plots
        self.setup_standard_font()

    def set_font(self):
        """Set the defaults fonts."""

        rc('text', usetex = True)
        plt.rcParams['text.latex.preamble']=[r"\usepackage{amsmath} \usepackage{siunitx} \usepackage{bm}"] 
        # amsmath # maths package
        # siunitx     # si units
        # bm           # maths bold symbols

        rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
        rc('font', family='serif')   
        
        return 0

    def set_font_size(self, font_size=None):
        """Set the default font size"""

        if font_size is None:
            font_size = self.font_size
        
        rc('font', size = font_size)          # controls default text sizes
        rc('axes', titlesize = font_size)     # fontsize of the axes title
        rc('axes', labelsize = font_size)     # fontsize of the x and y labels
        rc('xtick', labelsize = font_size)    # fontsize of the tick labels
        rc('ytick', labelsize = font_size)    # fontsize of the tick labels
        rc('legend', fontsize = font_size)    # legend fontsize
        rc('figure', titlesize = font_size)   # fontsize of the figure title
        
        return 0
    
    def setup_standard_font(self):
        
        # this to update the font size for plots so there is no need to run plotting stuff twice
        
        # seems like I don't need this function anymore, test if its needed, no harm leaving it in
        # could simply leave it as 
        # self.set_font()
        # self.set_font_size()
        
        fig, ax = plt.subplots(1,1)
        self.set_font()
        self.set_font_size()
        plt.close()  

class standard_figure:
    """
    Class to standarise figures given a set of parameters.
    Methods act on a figure and its axes to modify the figure and axes.
    
    Built upon the matplotlib figure and axes classes.

    Class Variables
    ----------
    fig : matplotlib figure
        Matplotlib figure object
    axes : matplotlib.axes
        Singluar matplotlib.axes or array of axes objects.
    fig_params : dict, figure_parameters
        Dicitionary or figure_parameters object with the figure parameters

    Example
    -------

    fig, axes = plt.subplots(1, 2)      # normal matplotlib call
    fig_params = figure_parameters()    # initialise figure parameters
    sf = standard_figure(fig, axes, fig_params) # initialise standard figure

    sf.add_subplot_labels() # add subplot labels to figure

    Methods
    -------
    __init__(self, fig, axes, fig_params=fig_params_report) : initialisation
        Create a standard_figure object, which stores the figure, axes, and 
        parameters.
        It also sets the size and ticks for the figure.
    standard_size(self)
        Sets the size of the figure.
        Used within __init__.
    standard_axes_ticks(self)
        Sets the ticks for the figure.
        Used within __init__.

    argument_axes(self, axes)
        Process input argument of 'axes' for other class methods.
    argument_axis_xy(self, axis_xy)
        Process input argument of 'axis_xy' for other class methods.

    standard_legend(self, axes=None, title=None, loc=1, ncol=1, 
                                                columnspacing=None)
        Standarise the legend.
    add_subplot_labels(self, axes=None, adjust=None, fig_adjust_bottom=None)
        Add subplot labels to the axes.
    add_subplot_labels_right(self, axes=None, adjust_x=None, adjust_y=None)
        Add subplot labels to the right of the axes.
    reduce_axes_clutter(self, axes=None, axis_xy=None, nticks=False, 
                                                                order=False)
        Reduce ticks and thus numbers that appear on the axes.
    
    standard_size_adjust(self, height_percentage=None, adjust_bottom=None)
        Adjust the size of the figure based on a height fractional percentage.

    latex_unit(self, unit=None, brackets=None)
        Generate a string for latex units in labels.
    xlabel(self, ax, label, unit=None, brackets=None)
    ylabel(self, ax, label, unit=None, brackets=None)
    xylabel(self, ax, xlabel, xunit, ylabel, yunit, brackets=None)
        Set the x, y, or both labels.

    set_xtick_labels(self, ax, x)
    set_ytick_labels(self, ax, y)
        Set the x or y tick labels.

    remove_ticks(self, axes=None)
        Remove the axis ticks for both x and y axes.
    remove_axes(self, axes=None)
        Remove the visable axis lines.

    schematic_arrow_axis(self, ax, xaxis=True, yaxis=True,
                                                        xwidth=0.001, ywidth=0.001,
                                                        remove_defaults=True,
                                                        set_yaxis_zero=None)
        Replace axis lines with arrows to represent a schematic diagram.
    schematic_subplots_adjust_single_text(self, adjust_bottom=None)
        Adjust the bottom of a figure, such that the label of the x axis in
        a schematic figure lines up with the label of a normal figure.

    schematic_log_arrow_axis(self, ax, xaxis=True, yaxis=True,
                                            xwidth=0.001, ywidth=0.001,
                                            remove_defaults=True,
                                            set_yaxis_zero=None)
        Replace axis lines with arrows to represent a schematic diagram,
        for log plots

    vector_arrows_2D(self, ax, xaxis=True, yaxis=True,
                        length=5.0, x_offset=0.0, y_offset=0.0,
                        xlabel="", ylabel="",
                        xlabel_x_offset=0.0, xlabel_y_offset=0.0,
                        ylabel_x_offset=0.0, ylabel_y_offset=0.0)
        Plot small vector arrows to help define 2D directions

    loglog_ticks(self, axes=None, axis_xy=None)
        Display the loglog ticks. 
    loglog_remove_labels(self, axes=None, axis_xy=None)
        Remove the log 10^(a) labels.
    """

    def __init__(self, fig, axes, fig_params=fig_params_report):
        """
        Initialise the standard figure. 
        Sets the figure size and axes ticks.

        Parameters
        ----------
        fig : matplotlib figure
            Matplotlib figure object.
        axes : matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
        fig_params : dict, figure_parameters
            Dicitionary or figure_parameters object with the figure parameters.
            Default is a fig_params_report define in plot_defaults.py
        """

        self.fig = fig
        
        self.axes = axes
        # if its only one axis, put into array
        try:
            len(axes)
        except:
            self.axes = [axes]
        
        if isinstance(fig_params, figure_parameters):
            self.fig_params = fig_params
        elif isinstance(fig_params, dict):
            # process fig_params into an object
            self.fig_params = figure_parameters(fig_params)
        else:
            raise Exception("Failed to process argument fig_params.")

        # set the figure size and axes ticks
        self.standard_size()
        self.standard_axes_ticks()
        
    def standard_size(self):
        """
        Set the size of the figure.
        """

        self.fig.set_size_inches([self.fig_params.width, self.fig_params.height])

        # even up the padding to better match right side
        self.fig.subplots_adjust(left = self.fig_params.adjust_left, 
                                                bottom = self.fig_params.adjust_bottom) 

        return 0

    def standard_axes_ticks(self):
        """
        Standardise the axes ticks.
        """
        for i in range(0, len(self.axes)):
            ax = self.axes[i]
            ax.minorticks_on()
            ax.tick_params(direction = 'in', which = 'both', 
                                        bottom = True, top = True, left = True, right = True)
        return

    def argument_axes(self, axes):
        """
        Process input argument of 'axes' for other class methods.
        Defaults to perform the operation on all axes.

        Default for other functions should be 'axes = None'

        Parameters
        ----------
        axes : matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
        """

        # default to all axes if none
        if axes is None:
            axes = self.axes
        # if only one given, put it into an array
        else:
            try: 
                len(axes)
            except:
                axes = [axes]
        
        return axes

    def argument_axis_xy(self, axis_xy):
        """
        Process input argument of 'axis_xy' for other class methods.
        Defaults to perform the operation on both x and y axes.

        Default for other functions should be 'axis_xy = None'

        Parameters
        ----------
        axis_xy : None, ["x", "y"], "x", "y"
            Select which x, y, or both axes.
        """

        if axis_xy is None:
            axis_xy = ["x", "y"]
        elif axis_xy == "x":
            axis_xy = ["x"]
        elif axis_xy == "y":
            axis_xy = ["y"]
        elif len(axis_xy) == 2:
            if axis_xy[0] == "x" and axis_xy[1] == "y":
                pass
            elif axis_xy[0] == "y" and axis_xy[1] == "x":
                pass
            else:
                raise Exception("Likely incorrect axis_xy argument.")
        else:
            raise Exception("Incorrect axis_xy argument.")
        
        return axis_xy

    def standard_legend(self, axes=None, title=None, loc=1, ncol=1,
                                            columnspacing=None):
        """
        Standarise the legend.

        Parameters
        ----------
        axes : None, matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
            Defaults to all axes in a figure.
        title : None, str
            Legend title.
            Default is no title.
        loc : int
            Legend location.
        ncol : int
            Number of columns.
        columnspacing : float
            Column spacing.
        """

        axes = self.argument_axes(axes)
        for ax in axes:
            ax.legend(title=title, loc = loc, ncol = ncol, handlelength=1,
                                columnspacing = columnspacing)
        return 0

    def add_subplot_labels(self, axes=None, adjust=None, fig_adjust_bottom=None):
        """
        Add subplot labels to the axes.

        Parameters
        ----------
        axes : None, matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
            Defaults to all axes in a figure.
        adjust : float
            Adjust location.
        fig_adjust_bottom : float
            Adjust the bottom of the figure.
        """

        axes = self.argument_axes(axes)

        if adjust is None:
            adjust = self.fig_params.adjust_subplot_label
        if fig_adjust_bottom is None:
            fig_adjust_bottom = self.fig_params.adjust_subplot_bottom   
        
        
        
        # defaults chosen as it works well with default values
        alphabet = ["a", "b", "c", "d", "e", "f"]
        for i in range(0, len(axes)):
            ax = axes[i]
            letter = alphabet[i]
            x_label_px, _ = ax.xaxis.get_label().get_position()
            ax.text(x_label_px, adjust,'({})'.format(letter), 
                            horizontalalignment='center',
                            verticalalignment='center',
                            transform = ax.transAxes)

        # adjust figure to make visual the subcaptions
        self.fig.subplots_adjust(bottom=fig_adjust_bottom)

        return 0

    def add_subplot_labels_right(self, axes=None, adjust_x=None, adjust_y=None):
        """
        Add subplot labels to the right of the axes.

        Parameters
        ----------
        axes : None, matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
            Defaults to all axes in a figure.
        adjust_x : float
            Adjust x location of the label.
        adjust_y : float
            Adjust y location of the label.
        """
        
        axes = self.argument_axes(axes)

        if adjust_x is None:
            adjust_x = self.fig_params.adjust_subplot_label_right_x
        if adjust_y is None:
            adjust_y = self.fig_params.adjust_subplot_label_right_y
        
        # defaults chosen as it works well with default values
        alphabet = ["a", "b", "c", "d", "e", "f"]
        for i in range(0, len(axes)):
            ax = axes[i]
            x_label_px, x_label_py  = ax.xaxis.get_label().get_position()
            ax.text(x_label_px + adjust_x, 
                        x_label_py + adjust_y, 
                        '({})'.format(alphabet[i]), 
                        horizontalalignment='center',
                        verticalalignment='center',
                        transform = ax.transAxes)

        return 0

    def reduce_axes_clutter(self, axes=None, axis_xy=None, nticks=False, 
                                                                order=False):
        """
        Reduce ticks and thus numbers that appear on the axes.

        Parameters
        ----------
        axes : None, matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
            Defaults to all axes in a figure.
        axis_xy : None, ["x", "y"], "x", "y"
            Select which x, y, or both axes to reduce the clutter on.
            Defaults to both x and y axes.
        nticks : False, Bool
            Number of major ticks on the axis.
            The number may not be rigidly preserved.
        order : float
            Change the major order format.
            E.g. to have values on the axis written with respect to 10^-4
            order = -4
        """

        axes = self.argument_axes(axes)
        axis_xy = self.argument_axis_xy(axis_xy)

        for ax in axes:
            for xy in axis_xy:
                if nticks != False:
                    ax.locator_params(axis=xy, nbins=nticks)

                if order != False:
                    print("Warning: changing the scale order found to not work in scripts, check plot. Does work in a notebook!")
                    print("Using function reduce_axes_clutter() with order argument")
                    if xy == "x":
                        ax.xaxis.set_major_formatter(FixedOrderFormatter(order))
                    if xy == "y": 
                        ax.yaxis.set_major_formatter(FixedOrderFormatter(order))

        return 0        

    def standard_size_adjust(self, height_percentage=None, adjust_bottom=None):
        """
        Adjust the size of the figure based on a height fractional percentage.

        Parameters
        ----------
        height_percentage : float
            Fractional percentage of which to scale the height of the figure.
        adjust_bottom : float
            Adjust the bottom of the figure, to give space for label.
        """

        if height_percentage is None:
            height_percentage = self.height_small_percentage
        if adjust_bottom is None:
            adjust_bottom = self.fig_params.adjust_bottom
        
        w, h = self.fig.get_size_inches()
        self.fig.set_size_inches([w, h * height_percentage])

        self.fig.subplots_adjust(left=self.fig_params.adjust_left) 
        self.fig.subplots_adjust(bottom=adjust_bottom)        

        return

    # x and y labels -------------------
    def latex_unit(self, unit=None, brackets=None):
        """
        A string which holds the latex defined unit with brackets.

        Parameters
        ----------
        unit : str
            String with unit as defined with the latex SI package.
            E.g. "\\meter\\per\\second"
        brackets : "round", "square"
            The style of brackets to use around the unit.
            "round" (unit)
            "square" [unit] 
        """
        
        if brackets is None:
            brackets = self.fig_params.brackets

        # if no unit given, return empty string
        if unit is None:
            return ""
        # otherwise return unit string
        if brackets == "round":
            return "$\\left( \\si{" + unit + "} \\right)$"
        elif brackets == "square":
            return "$\\left[ \\si{" + unit + "} \\right]$"
        else:
            raise Exception("Incorrect string for brackets argument.")

    def xlabel(self, axes, label, unit=None, brackets=None):
        """
        Set the x axis label with a label and a unit.

        Parameters
        ----------
        ax : matplotlib axis
            Single axis object.
        label : str
            Label for the axis.
            For latex maths use $$, e.g. "Energy Change $r^{-a}$"
        unit : str
            String with unit as defined with the latex SI package.
            E.g. "\\meter\\per\\second"
        brackets : "round", "square"
            The style of brackets to use around the unit.
            "round" (unit)
            "square" [unit] 
        """
        axes = self.argument_axes(axes)
        for ax in axes:
            ax.set_xlabel("{} {}".format(label, self.latex_unit(unit, brackets)))
        
        return 0

    def ylabel(self, axes, label, unit=None, brackets=None):
        """
        Set the y axis label with a label and a unit.

        Parameters
        ----------
        ax : matplotlib axis
            Single axis object.
        label : str
            Label for the axis.
            For latex maths use $$, e.g. "Energy Change $r^{-a}$"
        unit : str
            String with unit as defined with the latex SI package.
            E.g. "\\meter\\per\\second"
        brackets : "round", "square"
            The style of brackets to use around the unit.
            "round" (unit)
            "square" [unit] 
        """
        axes = self.argument_axes(axes)
        for ax in axes:
            ax.set_ylabel("{} {}".format(label, self.latex_unit(unit, brackets)))
        
        return 0

    def xylabel(self, axes, xlabel, xunit, ylabel, yunit, brackets=None):
        """
        Set the x and y axis labels with labels and units.

        Parameters
        ----------
        ax : matplotlib axis
            Single axis object.
        xlabel : str
            Label for the axis.
            For latex maths use $$, e.g. "Energy Change $r^{-a}$"
        xunit : str
            String with unit as defined with the latex SI package.
            E.g. "\\meter\\per\\second"
        ylabel : str
        yunit : str

        brackets : "round", "square"
            The style of brackets to use around the unit.
            "round" (unit)
            "square" [unit] 
        """
        axes = self.argument_axes(axes)
        for ax in axes:
            self.xlabel(ax, xlabel, xunit, brackets)
            self.ylabel(ax, ylabel, yunit, brackets)
        
        return 0

    def set_xtick_labels(self, axes, x):
        """
        Set x axis tick lables.
        Parameters
        ----------
        ax : matplotlib axis
            Single matplotlib axis.
        x : array
            x values of numbers.
            x is converted into strings within the function.
        """
        axes = self.argument_axes(axes)

        labels = np.asarray(x, dtype=str)

        for ax in axes:
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
        return 0
    
    def set_ytick_labels(self, axes, y):
        """
        Set y axis tick lables.
        Parameters
        ----------
        ax : matplotlib axis
            Single matplotlib axis.
        y : array
            y values of numbers.
            y is converted into strings within the function.
        """

        axes = self.argument_axes(axes)

        labels = np.asarray(y, dtype=str)

        for ax in axes:
            ax.set_yticks(y)
            ax.set_yticklabels(labels)

        return 0

    def remove_ticks(self, axes=None):
        """
        Remove the axis ticks for both x and y axes.

        Parameters
        ----------
        axes : None, matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
            Defaults to all axes in a figure.
        """

        axes = self.argument_axes(axes)

        for ax in axes:
            ax.set_xticks([]) # labels
            ax.set_yticks([])
            ax.xaxis.set_ticks_position('none') # tick markers
            ax.yaxis.set_ticks_position('none')

        return 0
        
    def remove_axes(self, axes=None):
        """
        Remove the visable axis lines.

        Parameters
        ----------
        axes : matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
            Defaults to all axes in a figure.
        """

        axes = self.argument_axes(axes)

        for ax in axes:
            for side in ['bottom','right','top','left']:
                ax.spines[side].set_visible(False)

        return 0


    # --------------------------------
    # functions below could use some cleaning up and improved reusabilty
    # some code overlaps 

    # could use self.axes here to run over multiple axes
    def schematic_arrow_axis(self, ax, xaxis=True, yaxis=True,
                                                        xwidth=0.001, ywidth=0.001,
                                                        remove_defaults=True,
                                                        set_yaxis_zero=None):
        """
        Replace axis lines with arrows to represent a schematic diagram.

        Parameters
        ----------
        ax : matplotlib axis
            Single axis.
        xaxis : True, Bool
            Turn the x axis into an arrow.
        yaxis : True, Bool
            Turn the y axis into an arrow.
        xwidth : 0.001,
            Thickness of the arrow line.
            Width default from matplotlib is 0.001
            # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.arrow.html
        ywidth : 0.001, float
            Thickness of the arrow line.
            Width default from matplotlib is 0.001
            # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.arrow.html 
        remove_defaults, True, Bool
            Remove the current ticks and axes.
        set_yaxis_zero : float
            Moves the x axis.
        """

        # remove current axes
        if remove_defaults == True:
            self.remove_ticks(ax)
            self.remove_axes(ax)

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        # get width and height of axes object to compute
        # matching arrowhead length and width
        dps = self.fig.dpi_scale_trans.inverted()
        bbox = ax.get_window_extent().transformed(dps)
        width, height = bbox.width, bbox.height

        # manual arrowhead width and length
        hw = 1./70.*(ymax-ymin)
        hl = 1./140.*(xmax-xmin)
        lw = 0.5 # axis line width

        # compute matching arrowhead length and width
        yhw = hw/(ymax-ymin)*(xmax-xmin)* height/width
        yhl = hl/(xmax-xmin)*(ymax-ymin)* width/height

        # draw x and y axis
        if xaxis == True:

            if set_yaxis_zero is None:
                yzero = ymin
            else:
                yzero = set_yaxis_zero

            ax.arrow(xmin, yzero, xmax-xmin, 0.0, fc='k', ec='k', lw = lw,
                    head_width=hw, head_length=hl, width = xwidth,
                    length_includes_head= True, clip_on = False)

        if yaxis == True:
            ax.arrow(xmin, ymin, 0., ymax-ymin, fc='k', ec='k', lw = lw,
                    head_width=yhw, head_length=yhl, width = ywidth,
                    length_includes_head= True, clip_on = False)
        
        return 0

    # single text in the sense that only ticks or only x label
    def schematic_subplots_adjust_single_text(self, adjust_bottom=None):
        """
        Adjust the bottom of a figure, such that the label of the x axis in
        a schematic figure lines up with the label of a normal figure.

        Parameters
        ----------
        adjust_bottom : float
            Adjust the bottom of the figure.

        """

        if adjust_bottom is None:
            adjust_bottom = self.fig_params.schematic_adjust_bottom_no_ticks
    
        self.fig.subplots_adjust(bottom = adjust_bottom)
        return 0 


    def schematic_log_arrow_axis(self, ax, xaxis=True, yaxis=True,
                                            xwidth=0.001, ywidth=0.001,
                                            remove_defaults=True,
                                            set_yaxis_zero=None):
        """
        Replace axis lines with arrows to represent a schematic diagram,
        for log plots

        Parameters
        ----------
        ax : matplotlib axis
            Single axis.
        xaxis : True, Bool
            Turn the x axis into an arrow.
        yaxis : True, Bool
            Turn the y axis into an arrow.
        xwidth : 0.001,
            Thickness of the arrow line.
            Width default from matplotlib is 0.001
            # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.arrow.html
        ywidth : 0.001, float
            Thickness of the arrow line.
            Width default from matplotlib is 0.001
            # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.arrow.html 
        remove_defaults, True, Bool
            Remove the current ticks and axes.
        set_yaxis_zero : float
            Moves the x axis.
        """
        # width default from matplotlib is 0.001
        # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.arrow.html

        # set_yaxis_zero: moves the x axis

        if remove_defaults == True:
            self.remove_ticks(ax)
            self.remove_axes(ax)

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        # functions fx and fy take log-scale coordinates to 'axes' coordinates
        def fx(x):
            return (np.log(x) - np.log(xmin))/(np.log(xmax) - np.log(xmin))
        def fy(y):
            return (np.log(y) - np.log(ymin))/(np.log(ymax) - np.log(ymin))
        
        lw = 0.5 # axis line width

        # draw x and y axis
        if xaxis == True:

            if set_yaxis_zero is None:
                yzero = ymin
            else:
                yzero = set_yaxis_zero

            x0 = fx(xmin)
            y0 = fy(ymin)
            x1 = fx(xmax) - fx(xmin)
            y1 = fy(ymin) - fy(ymin)
            
            head_width = 0.015
            head_length = 0.006
            
            ax.arrow(x0, y0, x1, y1, # input transformed arrow coordinates 
                        transform = ax.transAxes, # tell matplotlib to use axes coordinates   
                        facecolor = 'black', ec='k', lw = lw,
                        head_width=head_width, head_length=head_length, width = xwidth,
                        length_includes_head= True, clip_on = False)
                
        if yaxis == True:
            x0 = fx(xmin)
            y0 = fy(ymin)
            x1 = fx(xmax) - fx(xmax)
            y1 = fy(ymax) - fy(ymin)
            
            head_width = 0.0060 
            head_length = 0.015
            
            ax.arrow(x0, y0, x1, y1, # input transformed arrow coordinates 
                        transform = ax.transAxes, # tell matplotlib to use axes coordinates   
                        facecolor = 'black', ec='k', lw = lw,
                        head_width=head_width, head_length=head_length, width = ywidth,
                        length_includes_head= True, clip_on = False
                        )

        return 0



    # this uses very similar code to schematic arrows
    # could reduce this to reuse overlapping code
    def vector_arrows_2D(self, ax, xaxis=True, yaxis=True,
                        length=5.0, x_offset=0.0, y_offset=0.0,
                        xlabel="", ylabel="",
                        xlabel_x_offset=0.0, xlabel_y_offset=0.0,
                        ylabel_x_offset=0.0, ylabel_y_offset=0.0):
        """
        Plot small vector arrows to help define 2D directions
 
        Parameters
        ----------
        ax : matplotlib axis
            Single axis.
        xaxis : True, Bool
            An arrow for the x direction.
        yaxis : True, Bool
            An arrow for the y direction.
        length : 5.0, float
            Length of the arrow.
        x_offset : float
            Base location of the x arrow.
        y_offset : float
            Base location of the y arrow.
        xlabel : str 
            Label for the x arrow.
        ylabel : str
            Label for the y arrow.
        xlabel_x_offset : float
            Offset the x label in the x direction.
        xlabel_y_offset : float
            Offset the x label in the y direction.
        ylabel_x_offset : float
            Offset the y label in the x direction.
        ylabel_y_offset : float
            Offset the y label in the y direction.
        """
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        # location of end of arrows
        xmax = xmin + length
        ymax = ymin + length

        # get width and height of axes object to compute
        # matching arrowhead length and width
        dps = self.fig.dpi_scale_trans.inverted()
        bbox = ax.get_window_extent().transformed(dps)
        width, height = bbox.width, bbox.height

        width = 1 ; height = 1

        # manual arrowhead width and length
        hw = 1.0/10.0*(ymax-ymin)
        hl = 1.0/10.0*(xmax-xmin)
        lw = 0.5 # axis line width

        # compute matching arrowhead length and width
        yhw = hw/(ymax-ymin)*(xmax-xmin)* height/width
        yhl = hl/(xmax-xmin)*(ymax-ymin)* width/height

        # draw x and y axis
        xbase = xmin + x_offset
        ybase = ymin + y_offset

        xwidth = 0.001; ywidth = 0.001
        if xaxis == True:
            ax.arrow(xbase, ybase, xmax-xmin, 0.0, fc='k', ec='k', lw = lw,
                    head_width=hw, head_length=hl, width = xwidth,
                    length_includes_head= True, clip_on = False)

            ax.annotate(ylabel, xy = (xmin, ymin), 
                        xytext = (xbase + length + xlabel_x_offset, ybase + xlabel_y_offset))
            
        if yaxis == True:
            ax.arrow(xbase, ybase, 0., ymax-ymin, fc='k', ec='k', lw = lw,
                    head_width=yhw, head_length=yhl, width = ywidth,
                    length_includes_head= True, clip_on = False)
        
            ax.annotate(xlabel, xy = (xmin, ymin), 
                        xytext = (xbase + ylabel_x_offset , ybase + length + ylabel_y_offset))
        
        # for ax.annotate
        # xy = (xmin, ymin), as point has to remain in plot
        # so only move text
        # if point not in plot, text will not appear
        
        return 0

    def loglog_ticks(self, axes=None, axis_xy=None):
        """
        Sort the display the loglog ticks. 
        (Try and force the display of the ticks.)
        (Generally reduce number of ticks.)

        Parameters
        ----------
        axes : None, matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
            Defaults to all axes in a figure.
        axis_xy : None, ["x", "y"], "x", "y"
            Select which x, y, or both axes.
        """

        axes = self.argument_axes(axes)
        axis_xy = self.argument_axis_xy(axis_xy)

        locmin = matplotlib.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=10)

        for ax in axes:
            for xy in axis_xy:
                if xy == "x":
                    ax.xaxis.set_minor_locator(locmin)
                    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
                if xy == "y": 
                    ax.yaxis.set_minor_locator(locmin)
                    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

        return 0

    def loglog_remove_labels(self, axes=None, axis_xy=None):
        """
        Remove other log 10^(a) labels.
        Reduces the log labels for more minor ticks.

        Parameters
        ----------
        axes : None, matplotlib.axes
            Singluar matplotlib.axes or array of axes objects.
            Defaults to all axes in a figure.
        axis_xy : None, ["x", "y"], "x", "y"
            Select which x, y, or both axes.
        """

        axes = self.argument_axes(axes)
        axis_xy = self.argument_axis_xy(axis_xy)

        formatter = matplotlib.ticker.LogFormatter(labelOnlyBase=True, minor_thresholds=(1,2))
        for ax in axes:
            for xy in axis_xy:
                if xy == "x":
                    ax.get_xaxis().set_minor_formatter(formatter)
                if xy == "y": 
                    ax.get_yaxis().set_minor_formatter(formatter)

        return 0



# Log Plots

def loglog_guide_manual(ax, x, p0, p1, colour="grey", label="", linestyle=":",
                                                linewidth=1.5, logtype=None):
    """
    Manual log line of form p0 * ( x^(p1) )

    Parameters
    ----------
    ax : matplotlib axis
        Single matplotlib axis.
    x : array
        x value data
    p0 : float
        Constant
    p1 : float
        Power constant
    colour : str
        Matplotlib colours
    label : str
        Label for the line.
    linestyle : str
        matplotlib style of the line
    linewidth : float
        Thickness of the line.
    logtype : "loglog", "semilogy"
        Loglog plots or semilogy plots.
    """

    if logtype is None:
            logtype = "loglog"

    if label == "":
        label_v = '{' + str(p1) + '}'
        label = r'$r^{}$'.format(label_v)

    if logtype == "loglog":
        ax.loglog(x, p0*(np.power(x, p1)),
                        linestyle=linestyle, color=colour, 
                        label = label, linewidth = linewidth)

    if logtype == "semilogy":
        ax.semilogy(x, p0*(np.power(x, p1)),
                                linestyle=linestyle, color=colour, 
                                label = label, linewidth = linewidth)


    return 0

def loglog_guide(x, y, indices=None):
    """
    A rough fit of a loglog x and y line.
    Uses the first and last point of x and y
    A log line of form p0 * ( x^(p1) )
    Returns the y values and the p constants.

    Parameters
    ----------
    ax : matplotlib axis
        Single matplotlib axis.
    x : array
        x values (does not need to be log values)
    y : array
        y values (does not need to be log values)
    indices : None, array
        Indices of x and y to fit to. 
        Default will use first and last points of x and y.

    Returns
    -------
    y_g : array
        y values of guide line of form y_g = rf_p[0] * ( x^(rf_p[1]) )
    rf_p : [p0, p1]
        Rough fit parameters of log guide of form rf_p[0] * ( x^(rf_p[1]) )
    """

    if indices is None:
        indices = np.arange(0,len(x), 1)

    x = np.array(x)[indices]
    y = np.array(y)[indices]

    # remove 0.0 values and negatives
    x = np.abs(x)[x != 0.0]
    y = np.abs(y)[y != 0.0]

    def rough_fit(x, y):
        x_log = np.log(x)
        y_log = np.log(y)
        a_0 = y[0]/( np.power( x[0], ((y_log[0] - y_log[len(y)-1]) / (x_log[0] - x_log[len(x)-1])) ) )
        g = (y_log[0] - y_log[len(y)-1]) / (x_log[0] - x_log[len(x)-1])
        p_g = [a_0, round(g,2)]
        return p_g

    def model(x, p):
        return p[0]*(np.power(x, p[1]))

    rf_p = rough_fit(x, y) # rough fit parameters
    y_g = model(x, rf_p) # log line of y values using rough fit

    return y_g, rf_p

# Other

def move_view(ax, point, width, height=None, maintain_aspect_ratio=True):
    """
    Move the view of a plot around a point.

    Parameters
    ----------
    ax : matplotlib axis
        Single matplotlib axis.
    point : [x, y]
        Centre point of the view.
    wdith : float
        Width of the box.
    height : float
        Height of the box.
    maintain_aspect_ratio : True, Bool
        Retain the axis's current aspect ratio.
    """

    # default to a box around the point
    if height is None:
        height = width

    px = point[0]
    py = point[1]
    wh = 0.5*width # width half
    hh = 0.5*height # height half
    
    if maintain_aspect_ratio == True:
        
        # calculate current axis limit aspect ratio
        xl1, xl2 = ax.get_xlim()
        yl1, yl2 = ax.get_ylim()
        axis_ratio = (np.abs(xl2 - xl1))/(np.abs(yl2 - yl1))
        
        # adjust height to match aspect ratio
        hh = 0.5*(height/axis_ratio)
    
    ax.set_xlim([px - wh, px + wh])
    ax.set_ylim([py - hh, py + hh])
    
    xl1, xl2 = ax.get_xlim()
    yl1, yl2 = ax.get_ylim()
    axis_ratio = (np.abs(xl2 - xl1))/(np.abs(yl2 - yl1))
    
    return 0