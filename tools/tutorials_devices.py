"""Data of the /tutorials/devices/ page: open a program on another device of your network (gen_tutorials.py input).

Same step and block format as tutorials_data.py; this tutorial asks only for the device you open from, so every step
belongs to both network paths.
"""
from tutorials_data import ALL, BOTH, DESKTOP

PAGE = {
    "title": "Open your devices",
    "description": "Share a program on one of your devices and open it from another one by name: a web page, SSH, remote desktop or a file share. Step by step.",
    "lede": "Open a program on another device in your network by its name: a web page, SSH, remote desktop or a file share.",
    "other": "Both devices need Mesh Town in the same network. Not yet? Start with [Set up Mesh Town step by step](../index.html).",
    "question": "Which device will you open it from?",
    "android_note": "",
}

STEPS = [
    ("share", BOTH, ALL, "Share a program", "On the computer where the program runs", [
        ("p", "Do this on the computer where the program runs, for example a NAS or the office PC. Other devices can open a program only after you share it."),
        ("p", "Open the Mesh Town page → [[Networks]] → your network → [[Shared services (ports)]] → [[My published ports]]. Enter the port number of the program (for example 8080), choose [[All members]] or [[Selected members]] and click [[Publish port]]."),
        ("fig", "ports-mine"),
        ("p", "The device's name is part of the address. To give it a short name such as `nas`, change [[This computer's name]] on its Mesh Town page."),
        ("note", "You can share only programs that run on this device itself, not other devices in its home network."),
    ]),
    ("web", BOTH, ALL, "Open a web page", "", [
        ("os", DESKTOP, [
            ("p", "On your computer, open the Mesh Town page → [[Networks]] → your network → [[Shared services (ports)]]. The list [[Ports shared with you]] shows what other members share with you. For a device with a web page, click its address, for example `http://nas.meshtown`."),
            ("fig", "ports-shared"),
            ("p", "When you type an address yourself, start it with http://, not https://."),
            ("note", "Names like `nas.meshtown` work only in a browser that is connected to Mesh Town: see [Connect the browser](../index.html#browser)."),
        ]),
        ("os", ["android"], [
            ("p", "When Mesh Town is connected, type the address in any browser on the phone, for example `http://nas.meshtown`. You do not need to set up the browser: all of the phone's internet traffic goes through the app."),
            ("p", "To see which ports are shared with you, open [http://meshtown/](http://meshtown/) in the phone's browser."),
        ]),
    ]),
    ("apps", BOTH, DESKTOP, "Open it in another program", "SSH, remote desktop, file sharing", [
        ("p", "In the same list, click [[Open on this computer]] next to the port. The program then works on your computer at `127.0.0.1`: for example, port 22 becomes `127.0.0.1:2022`. Connect your program to that address."),
        ("fig", "devices-scheme"),
    ]),
]

END = {
    "title": "Your devices are open",
    "lines": [
        "Open [http://meshtown/](http://meshtown/) on any of your devices: it lists the ports shared with you.",
    ],
    "links": [
        ("Add another device", "../index.html?net=invite"),
        ("Invite someone", "../index.html?net=create#invite"),
        ("Update, remove, fix problems", "../../install/index.html"),
    ],
}

TUTORIAL = {"dir": "tutorials/devices", "up": "../../", "key": "devices", "nets": False,
            "page": PAGE, "steps": STEPS, "end": END}
