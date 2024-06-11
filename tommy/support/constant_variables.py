"""
This file contains all constant variable, such as colour codes and fonts.
"""

import os

from PySide6.QtGui import QFontDatabase

from tommy.support.application_settings import application_settings


# Primary colour properties
prim_col_red = "#E40046"
dark_prim_col_red = "#B3003C"
hover_prim_col_red = "#C3003C"
prim_col_black = "#000000"

# Secondary colour properties
sec_col_yellow = "#FED800"
seco_col_blue = "#00968F"
hover_seco_col_blue = "#007D74"
pressed_seco_col_blue = "#00665C"
sec_col_orange = "#FFA300"
hover_seco_col_orange = "#D88C00"
pressed_seco_col_orange = "#B97A00"
sec_col_purple = "#3F2A56"
hover_seco_col_purple = "#5A3F6E"
pressed_seco_col_purple = "#6F547F"
light_seco_col_purple = "#5A3F6E"
seco_purple_border_color = "#A59BC3"
sec_col_brown = "#94795D"

# Gray color properties
disabled_gray = "#B0B0B0"
light_gray = "#E0E0E0"
extra_light_gray = "#F5F5F5"
medium_light_gray = "#D3D3D3"
dark_medium_light_gray = "#B0B0B0"
hover_medium_light_gray = "#C0C0C0"
selected_medium_light_gray = "#A0A0A0"
pressed_medium_light_gray = "#909090"
medium_gray = "#666666"
dark_gray = "#333333"
darker_gray = "#222222"

# Font properties
source_sans_3_id = QFontDatabase.addApplicationFont(os.path.join(
    application_settings.fonts_data_folder,
    "Source_Sans_3",
    "static",
    "SourceSans3-Regular.ttf"))
raleway_id = QFontDatabase.addApplicationFont(os.path.join(
    application_settings.fonts_data_folder,
    "Raleway",
    "static",
    "Raleway-Regular.ttf"))
source_sans_3 = QFontDatabase.applicationFontFamilies(source_sans_3_id)[0]
raleway = QFontDatabase.applicationFontFamilies(raleway_id)[0]
text_font = f"'{source_sans_3}', Corbel"
heading_font = f"{raleway}, 'Century Gothic'"

# Label properties
label_height = 25

# Plot colors
plot_colors = [prim_col_red, sec_col_yellow, seco_col_blue, sec_col_purple,
               '#E16402', '#80E49E', '#B90CA4', '#409AED', '#475E3E', '#8072BD'
               ]
emma_colors = [prim_col_red, seco_col_blue, sec_col_orange, sec_col_purple]

# Scrollbar style
scrollbar_style = f"""
    QScrollBar:vertical {{
        border: 0px;
        background: {extra_light_gray};
        width: 10px;
        margin: 0px 0px 0px 0px;
    }}
    
    QScrollBar::handle:vertical {{
        background: rgba(0, 0, 0, 0.2);
        min-height: 20px;
    }}
    
    
    QScrollBar::add-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        height: 0px;
    }}
"""

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
