"""Rings drawn over /tutorials/ pictures around what the step tells you to click (gen_tutorials.py input).

Figure id -> boxes (x, y, width, height) as fractions of the picture, top left origin, around the text of the item;
the page draws a ring a little larger than the box.
A "<id>-dark" entry replaces the rings on the dark picture when it is laid out differently from the light one. Boxes come from text recognition of the picture: after a reshoot,
check them by eye on the page.
"""

MARKS = {
    "install-w": [(0.558, 0.905, 0.147, 0.028)],
    "install-m": [(0.829, 0.629, 0.120, 0.028)],
    "install-a": [(0.056, 0.380, 0.900, 0.052)],
    "icon-w": [(0.079, 0.129, 0.311, 0.074)],
    "icon-m": [(0.029, 0.144, 0.335, 0.060)],
    "password": [(0.074, 0.903, 0.198, 0.031)],
    "join-form": [(0.222, 0.356, 0.128, 0.034), (0.222, 0.898, 0.032, 0.031)],
    "join-form-dark": [(0.222, 0.333, 0.128, 0.032), (0.222, 0.905, 0.032, 0.029)],
    "joined": [(0.206, 0.114, 0.252, 0.030)],
    "create-form": [(0.222, 0.894, 0.109, 0.033)],
    "invite-start": [(0.300, 0.350, 0.425, 0.150)],
    "invite-ready": [(0.390, 0.331, 0.287, 0.037)],
    "browser-scope": [(0.288, 0.394, 0.300, 0.071)],
    "browser-w": [(0.073, 0.481, 0.273, 0.045), (0.236, 0.846, 0.097, 0.045)],
    "browser-m": [(0.354, 0.287, 0.259, 0.025), (0.397, 0.408, 0.040, 0.019)],
    "browser-firefox": [(0.024, 0.298, 0.265, 0.039)],
    "exit-choose": [(0.234, 0.318, 0.075, 0.024), (0.930, 0.936, 0.035, 0.019)],
    "exit-tray": [(0.301, 0.259, 0.086, 0.054)],
    "exit-status": [(0.169, 0.292, 0.337, 0.124)],
    "ports-mine": [(0.879, 0.411, 0.086, 0.041)],
    "ports-shared": [(0.297, 0.296, 0.262, 0.041), (0.798, 0.300, 0.150, 0.041)],
    "android-join": [(0.260, 0.917, 0.148, 0.030)],
    "android-exit": [(0.166, 0.592, 0.134, 0.017), (0.433, 0.938, 0.137, 0.016)],
    "android-vpn": [(0.795, 0.600, 0.065, 0.026)],
    "android-connected": [(0.304, 0.892, 0.393, 0.020)],
}
