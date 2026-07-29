"""
colors.py

Centralized color management for the Annotation Visualizer.

All colors are stored in OpenCV BGR format.
"""

import random

# ---------------------------------------------------------
# Default Label Colors (BGR)
# ---------------------------------------------------------

DEFAULT_COLORS = [

    (255, 102, 0),      # Blue
    (0, 180, 0),        # Green
    (0, 128, 255),      # Orange
    (180, 0, 255),      # Purple
    (0, 255, 255),      # Yellow
    (0, 0, 255),        # Red
    (255, 0, 255),      # Pink
    (255, 255, 0),      # Cyan
    (120, 60, 255),     # Violet
    (0, 200, 120),      # Emerald
    (80, 180, 255),     # Light Orange
    (150, 255, 100),    # Lime
    (200, 150, 50),     # Brown
    (255, 150, 200),    # Rose
    (180, 180, 180),    # Gray
    (255, 80, 80),      # Coral

]

# ---------------------------------------------------------
# Cache
# ---------------------------------------------------------

_COLOR_CACHE = {}

# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------

def random_color():
    """
    Generates a random bright color.
    """

    return (
        random.randint(40, 255),
        random.randint(40, 255),
        random.randint(40, 255),
    )


def get_color(category_id):
    """
    Returns a consistent color for every category.
    """

    if category_id not in _COLOR_CACHE:

        if category_id < len(DEFAULT_COLORS):
            _COLOR_CACHE[category_id] = DEFAULT_COLORS[category_id]

        else:
            _COLOR_CACHE[category_id] = random_color()

    return _COLOR_CACHE[category_id]


def get_text_color():
    """
    Label text color.
    """

    return (255, 255, 255)


def get_alpha():
    """
    Transparency of annotation fill.

    0.0 = Invisible
    1.0 = Fully opaque
    """

    return 0.20


def get_border_thickness():
    return 3


def get_font_scale():
    return 0.70


def get_font_thickness():
    return 2