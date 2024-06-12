import os

from PySide6.QtGui import QFontDatabase, QFont

from tommy.support.application_settings import application_settings

"""
This file contains all constant variable, such as colour codes and fonts.
"""

# Primary color properties
prim_col_red = "#E40046"
dark_prim_col_red = "#B3003C"
hover_prim_col_red = "#C3003C"
prim_col_black = "#000000"

# Secondary color properties
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
source_sans_3 = ""
raleway = ""
gwendolyn = ""
text_font = ""
heading_font = ""

# Define fonts
title_label_font = QFont(f"Century Gothic, Raleway", 13)
apply_button_font = QFont(f"Century Gothic, Raleway", 12)
collapse_button_font = QFont(f"Raleway", 12)
config_button_font = QFont(f"Raleway", 12)
file_label_font = QFont(f"Source Sans 3", 12)


def initialize_fonts() -> None:  # TODO: remove Gwendolyn & print statements
    """
    Function to initialize the fonts.
    :return: None
    """
    global source_sans_3, raleway, text_font, heading_font, gwendolyn

    _font_db = QFontDatabase()

    # Print path of the font files
    source_sans_path = os.path.join(
        application_settings.fonts_data_folder,
        "Source_Sans_3",
        "static",
        "SourceSans3-Regular.ttf"
    )

    raleway_path = os.path.join(
        application_settings.fonts_data_folder,
        "Raleway",
        "static",
        "Raleway-Bold.ttf"
    )

    gwendolyn_path = os.path.join(
        application_settings.fonts_data_folder,
        "Gwendolyn",
        "Gwendolyn-Regular.ttf"
    )

    # Check if the font files exist
    if not os.path.isfile(source_sans_path):
        print(f"Source Sans 3 font file not found at {source_sans_path}")
        return

    if not os.path.isfile(raleway_path):
        print(f"Raleway font file not found at {raleway_path}")
        return

    if not os.path.isfile(gwendolyn_path):
        print(f"Gwendolyn font file not found at {gwendolyn_path}")
        return

    # Load Source Sans 3
    source_sans_3_id = _font_db.addApplicationFont(source_sans_path)
    if source_sans_3_id == -1:
        print("Failed to load Source Sans 3 font.")
    else:
        source_sans_3_families = _font_db.applicationFontFamilies(
            source_sans_3_id)
        if not source_sans_3_families:
            print("No font families found for Source Sans 3.")
        else:
            source_sans_3 = source_sans_3_families[0]

    # Load Raleway
    raleway_id = _font_db.addApplicationFont(raleway_path)
    if raleway_id == -1:
        print("Failed to load Raleway font.")
    else:
        raleway_families = _font_db.applicationFontFamilies(raleway_id)
        if not raleway_families:
            print("No font families found for Raleway.")
        else:
            raleway = raleway_families[0]

    # Load Gwendolyn
    gwendolyn_id = _font_db.addApplicationFont(gwendolyn_path)
    if gwendolyn_id == -1:
        print("Failed to load Gwendolyn font.")
    else:
        gwendolyn_families = _font_db.applicationFontFamilies(
            gwendolyn_id)
        if not gwendolyn_families:
            print("No font families found for Gwendolyn.")
        else:
            gwendolyn = gwendolyn_families[0]

    text_font = source_sans_3  # Alternative for Corbel
    heading_font = raleway  # Alternative for Century Gothic


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
