import numpy as np
import json
import logging
import pprint

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
    Object to store all the deafult figure parameters.
    """
        
    def __init__(self, parameters = fig_params_report):
        
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
        self.adjust_subplot_label = load_parameter("adjust_subplot_label")
        self.adjust_left = load_parameter("adjust_left")
        self.adjust_bottom = load_parameter("adjust_bottom")
        self.adjust_subplot_wspace = load_parameter("adjust_subplot_wspace")
        self.adjust_subplot_hspace = load_parameter("adjust_subplot_hspace")

        self.schematic_adjust_bottom_no_ticks = load_parameter("schematic_adjust_bottom_no_ticks")

        # for subplot labels on the right hand side
        self.adjust_subplot_label_right_x = load_parameter("adjust_subplot_label_right_x")
        self.adjust_subplot_label_right_y = load_parameter("adjust_subplot_label_right_y")

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
                "adjust_subplot_label" : self.adjust_subplot_label,
                "adjust_left" : self.adjust_left,
                "adjust_bottom" : self.adjust_bottom,
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
    """

    def __init__(self, font_size = 12):

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

    def set_font_size(self, font_size = None):
        """Set the default font size"""

        if font_size == None:
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

    def __init__(self, fig, axes, fig_params = fig_params_report):

        self.fig = fig
        
        self.axes = axes
        # if its only one axis, put into array
        try:
            len(axes)
        except:
            self.axes = [axes]
        
        if isinstance(fig_params, figure_parameters):
            self.fig_params = fig_params
        # process fig_params into a object
        elif isinstance(fig_params, dict):
            self.fig_params = figure_parameters(fig_params)
        else:
            raise Exception("Failed to process argument fig_params.")

        self.standard_size()
        self.standard_axes_ticks()
        
    def standard_size(self):

        self.fig.set_size_inches([self.fig_params.width, self.fig_params.height])

        # even up the padding to better match right side
        self.fig.subplots_adjust(left = self.fig_params.adjust_left, 
                                                bottom = self.fig_params.adjust_bottom) 

        return 0

    def standard_axes_ticks(self):
        "Standardise axis ticks"
        for i in range(0, len(self.axes)):
            ax = self.axes[i]
            ax.minorticks_on()
            ax.tick_params(direction = 'in', which = 'both', 
                                        bottom = True, top = True, left = True, right = True)
        return

    def argument_axes(self, axes):

        # default for other functions should be 'axes = None'
        # default to all axes if none
        if axes == None:
            axes = self.axes
        # if only one given, put it into an array
        else:
            try: 
                len(axes)
            except:
                axes = [axes]
        
        return axes

    def standard_legend(self, axes = None, title=None, loc = 1, ncol = 1,
                                            columnspacing = None):

        axes = self.argument_axes(axes)
        for ax in axes:
            ax.legend(title=title, loc = loc, ncol = ncol, handlelength=1,
                                columnspacing = columnspacing)
        return 0

    def add_subplot_labels(self, axes = None, adjust = None, fig_adjust_bottom = None):

        axes = self.argument_axes(axes)

        if adjust == None:
            adjust = self.fig_params.adjust_subplot_label
        if fig_adjust_bottom == None:
            fig_adjust_bottom = self.fig_params.adjust_bottom
        
        
        
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

    def add_subplot_labels_right(self, adjust_x = None, adjust_y = None):
        
        if adjust_x == None:
            adjust_x = self.fig_params.adjust_subplot_label_right_x
        if adjust_y == None:
            adjust_y = self.fig_params.adjust_subplot_label_right_y
        
        
        # defaults chosen as it works well with default values
        alphabet = ["a", "b", "c", "d", "e", "f"]
        for i in range(0, len(self.axes )):
            ax = self.axes[i]
            x_label_px, x_label_py  = ax.xaxis.get_label().get_position()
            ax.text(x_label_px + adjust_x, 
                        x_label_py + adjust_y, 
                        '({})'.format(alphabet[i]), 
                        horizontalalignment='center',
                        verticalalignment='center',
                        transform = ax.transAxes)

        return 0

    def reduce_axes_clutter(self, axes=None, axis_xy =  ["x", "y"], nticks = False, order = False):

        axes = self.argument_axes(axes)

        if axis_xy == "x":
            axis_xy = ["x"]
        elif axis_xy == "y":
            axis_xy = ["y"]

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

    def standard_size_adjust(self, height_percentage = 1.0, adjust_bottom = None):

        if adjust_bottom == None:
            adjust_bottom = self.fig_params.adjust_bottom
        
        w, h = self.fig.get_size_inches()
        self.fig.set_size_inches([w, h * height_percentage])

        self.fig.subplots_adjust(left=self.fig_params.adjust_left) 
        self.fig.subplots_adjust(bottom=fig_adjust_bottom)        

        return

    # x and y labels -------------------
    def latex_unit(self, unit, brackets = None):
        
        if brackets == None:
            brackets = self.fig_params.brackets

        # if no unit given, return empty string
        if unit == None:
            return ""
        # otherwise return unit string
        if brackets == "round":
            return "$\\left( \\si{" + unit + "} \\right)$"
        elif brackets == "square":
            return "$\\left[ \\si{" + unit + "} \\right]$"
        else:
            raise Exception("Incorrect string for brackets argument.")

    def xlabel(self, ax, xlabel, xunit = None, brackets = None):
        ax.set_xlabel("{} {}".format(xlabel, self.latex_unit(xunit, brackets)))
        return 0

    def ylabel(self, ax, ylabel, yunit = None, brackets = None):
        ax.set_ylabel("{} {}".format(ylabel, self.latex_unit(yunit, brackets)))
        return 0

    def xylabel(self, ax, xlabel, xunit, ylabel, yunit, brackets = None):
        self.xlabel(self, ax, xlabel, xunit, brackets)
        self.ylabel(self, ax, ylabel, yunit, brackets)
        return 0

    # could use self.axes here to run over multiple axes
    def remove_ticks(self, ax):
        """
        removing the axis ticks
        """
        ax.set_xticks([]) # labels
        ax.set_yticks([])
        ax.xaxis.set_ticks_position('none') # tick markers
        ax.yaxis.set_ticks_position('none')
        return 0
        
    # could use self here to run over multiple axes
    def remove_axes(self, ax):
        """
        removing the default axis on all sides
        """
        for side in ['bottom','right','top','left']:
            ax.spines[side].set_visible(False)

        return 0

    # could use self.axes here to run over multiple axes
    def schematic_arrow_axis(self, ax, xaxis = True, yaxis = True,
                                                        xwidth = 0.001, ywidth = 0.001,
                                                        remove_defaults = True,
                                                        set_yaxis_zero = None):
    
        # width default from matplotlib is 0.001
        # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.arrow.html

        # set_yaxis_zero: moves the x axis

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

            if set_yaxis_zero == None:
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
    def schematic_subplots_adjust_single_text(self, adjust_bottom = None):
        
            if adjust_bottom == None:
                adjust_bottom = self.fig_params.schematic_adjust_bottom_no_ticks
        
            self.fig.subplots_adjust(bottom = bottom)
            return 0 


    def schematic_log_arrow_axis(self, ax, xaxis = True, yaxis = True,
                                            xwidth = 0.001, ywidth = 0.001,
                                            remove_defaults = True,
                                            set_yaxis_zero = None):
        """
        Draw schematic arrow axes for log plots
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

            if set_yaxis_zero == None:
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
    def vector_arrows_2D(self, ax, xaxis = True, yaxis = True,
                        length = 5.0, x_offset = 0.0, y_offset = 0.0,
                        xlabel = "", ylabel = "",
                        xlabel_x_offset = 0.0, xlabel_y_offset = 0.0,
                        ylabel_x_offset = 0.0, ylabel_y_offset = 0.0):
        """
        Plot small vector arrows to help define 2D directions
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