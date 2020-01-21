# Plot defaults

fig_params_report = {
    # Default Font Sizes ------------------------------------------------------------

    # Latex Font Sizes
    # https://tex.stackexchange.com/questions/24599/what-point-pt-font-size-are-large-etc
    # These are for 12pt documents i.e. \documentclass[12pt]{article}
    "font_size"  : 10.95,

    # Default Figure Measurements --------------------------------------------------

    # report
    # using theses margins as in a main.tex
    #\documentclass[12pt,a4paper]{report}
    #\usepackage[left=4.25cm, right=3.10cm, top=3.5cm, bottom=3.5cm, textwidth=5.25in]{geometry}

    # measure with https://tex.stackexchange.com/questions/39383/determine-text-width
    # gives a measure of \textwidth at 5.37506 inches or 13.64806 cm
    # figure width of 5.315 inches, 13.5001cm, leaves 0.14796 cm or 0.74 mm on each side
    # thus should never be squashed to be fitted in 

    "width" : 5.315,        # inches 
    "ratio" : 3.0/2.0,      # default matplotlib ratio
    "height" : 5.315 / (3.0/2.0), # FIG_WIDTH_report / FIG_RATIO_report
    "height_small_percentage" : 0.75, # standard size for small plots

    "adjust_bottom" : 0.15, # adjust bottom to give space for label
    "adjust_subplot_label" : -0.225, # default of -0.225 chosen since it looks nice with above values
    "adjust_left" : 0.15, # even up the padding to better match right side # 0.15 looks decent, tested a few
    "adjust_bottom" : 0.2, # brings subplot label into view # 0.2 looks decent
    "adjust_subplot_wspace" : 0.05, # default value is good for sharing of y axis
    "adjust_subplot_hspace" : 0.075,

    # for figures with no ticks, this is the amount to adjust the label
    # to match the label position of plots with ticks
    "schematic_adjust_bottom_no_ticks" : 0.13, 
    # note the effective plot area is bigger on these plots

    "adjust_subplot_label_right_x" : 0.56,
    "adjust_subplot_label_right_y" : 0.5,

    # Other
    "brackets" : "round" # "round" (), or "square" []
}
