"""Data of the /tutorials/ page, set up Mesh Town (generator input for gen_tutorials.py; figures for all tutorials).

Step: (id, nets, oses, title, tag, blocks). `id` is also the page anchor. `nets` is the set of paths the step belongs to
("invite" = I have an invite, "create" = I am starting a new network), `oses` the systems it applies to.
Blocks are those of install_data.py plus ("os", [systems], [blocks]), ("note", text), ("wait", question, answer) and
("fig", figure id).
Markup in text: `code`, [label](url), [[button name]]: a button or screen name taken word for word from the program
texts (tools/check_tutorial_terms.py checks every one against them).
"""
from install_data import DIST

ALL = ("windows", "macos", "android")
DESKTOP = ("windows", "macos")
BOTH = ("invite", "create")
INSTALL_GUIDE = "../install/%s/index.html"

# Figure id -> (alt text naming the screen in words, own interface?). Own interface: <id>-light.webp and <id>-dark.webp;
# another program's window: <id>.webp. A figure with no file is left out.
FIGS = {
    "install-w": ("The Windows warning after More info, with the Run anyway button", False),
    "install-m": ("macOS Privacy & Security with the Open Anyway button", False),
    "install-a": ("Android Install unknown apps with the Allow from this source switch", False),
    "icon-w": ("The Mesh Town tray menu on Windows with the Join or create a network item", False),
    "icon-m": ("The Mesh Town menu bar menu on macOS with the Join or create a network item", False),
    "password": ("The Set a password screen with two fields and the Set password button", True),
    "join-form": ("The Join with an invite form with an invite pasted and the Join button", True),
    "joined": ("The page showing You joined the network", True),
    "create-form": ("The Create a new network form with the name family", True),
    "invite-start": ("The Invite a member button and the optional For whom field", True),
    "invite-ready": ("The ready invite with Send as text, Send as QR code and the invite itself", True),
    "browser-scope": ("The question Where should Mesh Town open sites and its two answers", True),
    "browser-w": ("Edit setup script in Windows proxy settings, with the Mesh Town address", False),
    "browser-m": ("macOS Proxies with Automatic Proxy Configuration", False),
    "browser-firefox": ("Firefox Connection Settings", False),
    "browser-firefox-pac": ("Firefox Connection Settings with Automatic proxy configuration URL", False),
    "exit-choose": ("The Choose an exit screen listing office-pc, nas and Directly, without an exit, and this computer's name laptop", True),
    "exit-tray": ("The Exit via menu in the macOS menu bar", False),
    "exit-status": ("The Home tab panel showing how sites open right now", True),
    "ports-mine": ("My published ports with the port form and the Publish port button", True),
    "ports-shared": ("Ports shared with you with an address and Open on this computer", True),
    "devices-scheme": ("The address http://nas.meshtown in a browser and 127.0.0.1:2022 for SSH", True),
    "android-join": ("The phone join form with the Scan QR button", True),
    "android-exit": ("The phone exit screen and the Connect button", False),
    "android-vpn": ("The Android Connection request window with the OK button", False),
    "android-connected": ("The phone status line reading Connected via office-pc", False),
}

PAGE = {
    "title": "Set up Mesh Town step by step",
    "description": "Install Mesh Town, join a network or start your own, choose an exit and connect the browser: step by step.",
    "lede": "When you finish, this device is in your network, and websites open through the member you choose.",
    "other": "Do you use Linux, a router or an iPhone? See the [install guides](../install/index.html). Already set up? [Open your devices →](devices/index.html)",
    "question": "Which device are you setting up?",
    "android_note": "A phone can only join a network. To start a new network, use a computer first.",
}

BROWSERS = [
    ("p", "Chrome, Edge, Safari, Brave and most other browsers use this system setting: there is nothing to change in them. Close the browser completely and open it again."),
    ("p", "Firefox: open Settings and type proxy in the search box. Open the proxy settings that appear and check that Use system proxy settings is selected (it is selected from the start). Opera: turn off its own VPN, or websites will not go through Mesh Town."),
]
COPY = ("p", "Click [[Copy]] next to the setup address `http://127.0.0.1:1080/proxy.pac`.")
SYSTEM_STEPS = [
    COPY,
    ("os", ["windows"], [
        ("ol", [
            "Open [[Settings]] → [[Network & internet]] → [[Proxy]].",
            "Next to [[Use setup script]], click [[Set up]].",
            "Turn on [[Use setup script]], paste the address into [[Script address]] and click [[Save]].",
        ]),
        ("fig", "browser-w"),
    ]),
    ("os", ["macos"], [
        ("ol", [
            "Open [[System Settings]] → [[Network]] and choose your connection.",
            "Click [[Details…]] and open [[Proxies]].",
            "Turn on [[Automatic Proxy Configuration]] and paste the address into the [[URL]] field.",
            "Click [[OK]]. If you use both Wi-Fi and a cable (Ethernet), do the same for Ethernet.",
        ]),
        ("fig", "browser-m"),
    ]),
]
FIREFOX_ONLY = [
    ("p", "On the Mesh Town page, choose [[Firefox]]. " + COPY[1]),
    ("ol", [
        "In Firefox, open Settings and type proxy in the search box. Click the Settings button that appears.",
        "Choose Automatic proxy configuration URL and paste the address into the field below it.",
        "Click OK.",
    ]),
    ("fig", "browser-firefox-pac"),
]
CHECK = ("p", "Check it: open [http://meshtown/](http://meshtown/). It says “This browser is connected to Mesh Town” and lists the ports shared with you.")

STEPS = [
    ("install", BOTH, ALL, "Install Mesh Town", "", [
        ("os", ["windows"], [
            ("p", "Download [meshtown-setup.exe](" + DIST + "windows/meshtown-setup.exe) and open it. Windows asks for administrator permission, because the program is installed into Program Files. The last page has a Run Mesh Town box with a check mark: leave the check mark, and the program starts at once."),
            ("warn", "Windows may show a warning that it does not know this program. Click More info, then Run anyway."),
            ("fig", "install-w"),
            ("p", "Other ways to install, how to update, what to do if something goes wrong: [Windows install guide →](" + INSTALL_GUIDE % "windows" + ")"),
        ]),
        ("os", ["macos"], [
            ("tabs", ("macos", [
                ("brew", "Homebrew", [
                    ("cmd", "brew install mesh-town/macos/meshtown\nmeshtown"),
                    ("p", "When you install with Homebrew, macOS does not block the first start."),
                ]),
                ("app", "App", [
                    ("p", "Download the file for [Apple silicon](" + DIST + "macos/MeshTown-macos-arm64.zip) or for [Intel](" + DIST + "macos/MeshTown-macos-x86_64.zip). Open the zip file and move MeshTown.app to Applications."),
                    ("warn", "The first time, macOS blocks the app because Apple has not checked it. Open System Settings → Privacy & Security and click Open Anyway."),
                    ("fig", "install-m"),
                ]),
            ])),
            ("p", "Other ways to install, how to update, what to do if something goes wrong: [macOS install guide →](" + INSTALL_GUIDE % "macos" + ")"),
        ]),
        ("os", ["android"], [
            ("ol", [
                "On the phone, download [meshtown.apk](" + DIST + "android/meshtown.apk). If Chrome warns that the file might be harmful, choose Download anyway.",
                "Open the file from the notification or from Downloads. Android says it is not allowed to install apps from this source: press Settings, turn on Allow from this source, go back and open the file again.",
                "Start Mesh Town.",
            ]),
            ("note", "It needs Android 7.0 or newer on a 64-bit phone (ARM)."),
            ("fig", "install-a"),
            ("p", "Other ways to install, how to update, what to do if something goes wrong: [Android install guide →](" + INSTALL_GUIDE % "android" + ")"),
        ]),
    ]),
    ("open", BOTH, DESKTOP, "Open the Mesh Town page and set a password", "", [
        ("os", ["windows"], [("p", "A Mesh Town icon appears near the clock. Click it and choose [[Join or create a network…]] (later this item is called [[Open Mesh Town…]]).")]),
        ("os", ["macos"], [
            ("p", "A Mesh Town icon appears in the menu bar. Click it and choose [[Join or create a network…]] (later this item is called [[Open Mesh Town…]])."),
            ("note", "You do not see the icon? Look in System Settings → Menu Bar."),
        ]),
        ("fig-os", {"windows": "icon-w", "macos": "icon-m"}),
        ("p", "The Mesh Town page opens in your browser. On [[Set a password]], type a password two times and click [[Set password]]. This password only protects this page, not your network."),
        ("fig", "password"),
    ]),
    ("join", ("invite",), ALL, "Join with an invite", "Only with an invite", [
        ("p", "Ask a member of the network for an invite. You can use it only once, within 24 hours."),
        ("os", DESKTOP, [
            ("p", "Click [[Join with an invite]], paste the invite into [[Invite you received]] and click [[Join]]."),
            ("fig", "join-form"),
            ("p", "The page waits until a member of the network is online and lets you in. Then it shows [[✓ You joined the network]]."),
            ("fig", "joined"),
            ("wait", "Nothing happens after a minute?", "The person who invited you must have their device turned on, with Mesh Town running."),
        ]),
        ("os", ["android"], [
            ("p", "Open Mesh Town, tap [[Join with an invite]] and paste the invite, or tap [[Scan QR]] and point the camera at the QR code on the other person's screen."),
            ("fig", "android-join"),
            ("wait", "Nothing happens after a minute?", "The person who invited you must have their device turned on, with Mesh Town running."),
        ]),
    ]),
    ("create", ("create",), DESKTOP, "Create your network", "Only when you start a network", [
        ("p", "Click [[Create a new network]] and type a name for it, for example `family`. People you invite will see this name. Click [[Create network]]. Now you are the admin: the person who manages this network."),
        ("fig", "create-form"),
    ]),
    ("invite", ("create",), DESKTOP, "Invite a device or a person", "Only when you start a network", [
        ("p", "Click [[Invite a member]]. You can type who the invite is for, but you do not have to. Confirm. A window shows the invite as text; [[Send as QR code]] shows it as a QR code."),
        ("fig", "invite-start"),
        ("fig", "invite-ready"),
        ("p", "Send it to one person in a private message. It can be used only once, within 24 hours. Keep this computer turned on until the person joins."),
        ("p", "On the other device, open [this page](index.html?net=invite) and choose I have an invite."),
        ("p", "When someone has joined, you can make them a second admin: [[Networks]] → [[Members]] → ⋯ → [[Make admin]]."),
    ]),
    ("exit", BOTH, ALL, "Choose an exit", "", [
        ("p", "An exit is a member of your network. Websites you open go through that member's internet connection, so the websites see that member's address, not yours."),
        ("os", DESKTOP, [
            ("p", "On [[Choose an exit]], choose a member. Or choose [[Directly, without an exit]] to use your own internet connection. Below, in [[This computer's name]], type a name that other members will see, for example `laptop`. Click [[Next]]."),
            ("fig", "exit-choose"),
            ("p", "You can change the exit at any time: click the Mesh Town icon → [[Exit via…]], or open the Home tab of the Mesh Town page."),
            ("fig", "exit-tray"),
            ("fig", "exit-status"),
            ("note", "The list is empty? Then no member can be an exit yet. Computers and routers can be exits from the start, phones cannot. Until another computer or router joins, websites open directly."),
        ]),
        ("os", ["android"], [
            ("p", "The app chooses an exit for you. You can choose another member if you want."),
            ("fig", "android-exit"),
        ]),
        ("p", "The exit can see the names of the websites you visit, so choose a member you trust. If that member goes offline, websites stop opening until you choose another exit."),
    ]),
    ("connect", ("invite",), ("android",), "Connect", "", [
        ("p", "Tap [[Connect]] at the bottom of the screen. Allow notifications when asked, so you know when the connection is lost. Then Android asks to set up a VPN connection: press OK."),
        ("fig", "android-vpn"),
        ("p", "Once connected, Android may ask to let the app always run in the background: allow it, so the connection is not stopped. Then you see [[Connected via]] and the name of your exit at the bottom of the screen."),
        ("fig", "android-connected"),
    ]),
    ("browser", BOTH, DESKTOP, "Connect the browser", "", [
        ("p", "The page asks [[Where should Mesh Town open sites?]] Choose one of the two answers below."),
        ("fig", "browser-scope"),
        ("tabs", ("scope", [
            ("browser", "Only in one browser", [
                ("p", "Choose [[Only in one browser]]. Other programs on the computer keep going to the internet directly. Which browser do you use?"),
                ("tabs", ("browser", [
                    ("firefox", "Firefox", FIREFOX_ONLY),
                    ("other", "Safari, Chrome, Edge or another", [
                        ("p", "These browsers have no proxy setting of their own: they always use the setting of the whole computer. So they can work with Mesh Town only for all apps. Choose your browser on the Mesh Town page, then click [[Set up for all apps]] and follow these steps:"),
                    ] + SYSTEM_STEPS),
                ], "Your browser")),
            ]),
            ("system", "All apps on this computer", [
                ("p", "Choose [[All apps on this computer]]. Then the browser and all other programs go through Mesh Town."),
            ] + SYSTEM_STEPS + [BROWSERS[0], BROWSERS[1], ("fig", "browser-firefox")]),
        ], "Where Mesh Town opens sites")),
        ("p", "Then choose what happens [[When Mesh Town is off]]: [[Open sites directly]] or [[Keep sites closed]]."),
        CHECK,
    ]),
]

END = {
    "title": "You are ready",
    "lines": [
        "Open the Mesh Town page: [http://127.0.0.1:7777/](http://127.0.0.1:7777/). If it opens, Mesh Town is running.",
        "Open [http://meshtown/](http://meshtown/): it says “This browser is connected to Mesh Town”.",
    ],
    "links": [
        ("Open your devices", "devices/index.html"),
        ("Add another device", "index.html?net=invite"),
        ("Invite someone", "index.html?net=create#invite"),
        ("Update, remove, fix problems", "../install/index.html"),
    ],
}

TUTORIAL = {"dir": "tutorials", "up": "../", "key": "", "nets": True, "page": PAGE, "steps": STEPS, "end": END}
