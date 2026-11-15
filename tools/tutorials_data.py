"""Data of the /tutorials/ page (generator input for gen_tutorials.py).

Step: (id, nets, oses, title, tag, blocks). `id` is also the page anchor. `nets` is the set of paths the step belongs to
("invite" = I have an invite, "create" = I am starting a new network), `oses` the systems it applies to.
Blocks are those of install_data.py plus ("os", [systems], [blocks]), ("note", text) and ("fig", figure id).
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
    "install-w": ("The Windows warning about an unsigned program after More info, with Run anyway", False),
    "install-m": ("macOS Privacy & Security with the Open Anyway button", False),
    "install-a": ("Android asking to allow installing apps from this source", False),
    "icon-w": ("The Mesh Town tray menu on Windows with the Join or create a network item", False),
    "icon-m": ("The Mesh Town menu bar menu on macOS with the Join or create a network item", False),
    "password": ("The Set a password screen with two fields and the Continue button", True),
    "join-form": ("The Join with an invite form with an invite pasted and the Join button", True),
    "joined": ("The page showing You joined the network", True),
    "create-form": ("The Create a new network form with the name family", True),
    "invite-start": ("The Invite a member button and the optional For whom field", True),
    "invite-ready": ("The ready invite with Send as text, Send as QR code and the invite itself", True),
    "browser-scope": ("The question Where should Mesh Town open sites with the setup address", True),
    "browser-w": ("Edit setup script in Windows proxy settings, with the Mesh Town address", False),
    "browser-m": ("macOS Proxies with Automatic Proxy Configuration", False),
    "browser-firefox": ("Firefox Connection Settings", False),
    "exit-choose": ("The Choose an exit screen listing office-pc, nas and Directly, without an exit, and this computer's name laptop", True),
    "exit-tray": ("The Exit via menu in the macOS menu bar", False),
    "exit-status": ("The Home tab panel showing how sites open right now", True),
    "ports-mine": ("My published ports with the port form and the Publish port button", True),
    "ports-shared": ("Ports shared with you with an address and Open on this computer", True),
    "devices-scheme": ("The address http://nas.meshtown in a browser and 127.0.0.1:2022 for SSH", True),
    "android-join": ("The phone join form with the Scan QR button", True),
    "android-exit": ("The phone exit screen and the Connect button", False),
    "android-vpn": ("The Android window asking to allow a connection", False),
    "android-connected": ("The phone status line reading Connected via office-pc", False),
}

PAGE = {
    "title": "Set up Mesh Town step by step",
    "description": "Install Mesh Town, join a network or start your own, choose an exit, connect the browser and open your devices by name: step by step.",
    "lede": "At the end this device is in your network, its browser opens your devices by name, and sites open through the member you pick.",
    "other": "On Linux, a router or an iPhone? See the [install guides](../install/index.html).",
    "android_note": "Start a network on a computer first, then join from the phone",
}

BROWSERS = [
    ("p", "Chrome, Edge, Safari, Brave and most other browsers use this system setting: there is nothing to change in them. Close the browser completely and open it again."),
    ("p", "Firefox: open Settings, type proxy in the search box, open the proxy settings it finds and make sure Use system proxy settings is selected (it is the default). Opera: turn off its built-in VPN, or sites bypass Mesh Town."),
]
CHECK = ("p", "Check it: open [http://meshtown/](http://meshtown/). It says “This browser is connected to Mesh Town” and lists the ports shared with you.")

STEPS = [
    ("install", BOTH, ALL, "Install Mesh Town", "", [
        ("os", ["windows"], [
            ("p", "Download [meshtown-setup.exe](" + DIST + "windows/meshtown-setup.exe) and run it. Windows asks for administrator permission, because the installer puts the program in Program Files. On the last page, leave Run Mesh Town ticked."),
            ("warn", "Windows may warn that the program is not signed. Choose More info, then Run anyway."),
            ("fig", "install-w"),
            ("p", "Other ways to install, updating, troubleshooting: [Windows install guide →](" + INSTALL_GUIDE % "windows" + ")"),
        ]),
        ("os", ["macos"], [
            ("tabs", ("macos", [
                ("brew", "Homebrew", [
                    ("cmd", "brew install mesh-town/macos/meshtown\nmeshtown"),
                    ("p", "A Homebrew install is not marked as downloaded from the internet, so macOS does not stop the first launch."),
                ]),
                ("app", "App", [
                    ("p", "Download for [Apple silicon](" + DIST + "macos/MeshTown-macos-arm64.zip) or for [Intel](" + DIST + "macos/MeshTown-macos-x86_64.zip), unzip and move MeshTown.app to Applications."),
                    ("warn", "macOS stops the first launch of an app that is not notarized. Open System Settings → Privacy & Security and press Open Anyway."),
                    ("fig", "install-m"),
                ]),
            ])),
            ("p", "Other ways to install, updating, troubleshooting: [macOS install guide →](" + INSTALL_GUIDE % "macos" + ")"),
        ]),
        ("os", ["android"], [
            ("ol", [
                "On the phone, download [meshtown.apk](" + DIST + "android/meshtown.apk).",
                "Open the file. Android asks to allow installing apps from this source: allow it.",
                "Start Mesh Town.",
            ]),
            ("note", "It needs a 64-bit ARM phone with Android 7.0 or newer."),
            ("fig", "install-a"),
            ("p", "Other ways to install, updating, troubleshooting: [Android install guide →](" + INSTALL_GUIDE % "android" + ")"),
        ]),
    ]),
    ("open", BOTH, DESKTOP, "Open the node page and set a password", "", [
        ("os", ["windows"], [("p", "A Mesh Town icon appears near the clock. Click it and choose [[Join or create a network…]] (later it reads [[Open Mesh Town…]]).")]),
        ("os", ["macos"], [
            ("p", "A Mesh Town icon appears in the menu bar. Click it and choose [[Join or create a network…]] (later it reads [[Open Mesh Town…]])."),
            ("note", "No icon? Check System Settings → Menu Bar."),
        ]),
        ("fig-os", {"windows": "icon-w", "macos": "icon-m"}),
        ("p", "The page opens in your browser. On [[Set a password]], type a password twice and press [[Continue]]. It protects this settings page only."),
        ("fig", "password"),
    ]),
    ("join", ("invite",), ALL, "Join with an invite", "Only with an invite", [
        ("p", "Ask a member of the network for an invite. It works once, for 24 hours."),
        ("os", DESKTOP, [
            ("p", "Press [[Join with an invite]], paste it into [[Invite you received]] and press [[Join]]."),
            ("fig", "join-form"),
            ("p", "The page waits until a member is online to let you in, then shows [[✓ You joined the network]]."),
            ("fig", "joined"),
            ("note", "Nothing after a minute? The person who invited you must keep their device on."),
        ]),
        ("os", ["android"], [
            ("p", "Open Mesh Town, tap [[Join with an invite]] and paste the invite, or tap [[Scan QR]] and point the camera at the QR code on the other person's screen."),
            ("fig", "android-join"),
            ("note", "Nothing after a minute? The person who invited you must keep their device on."),
        ]),
    ]),
    ("create", ("create",), DESKTOP, "Create your network", "Only when you start a network", [
        ("p", "Press [[Create a new network]], type a name members will see in the invite, for example `family`, and press [[Create network]]. You are its admin."),
        ("fig", "create-form"),
    ]),
    ("invite", ("create",), DESKTOP, "Invite a device or a person", "Only when you start a network", [
        ("p", "Press [[Invite a member]], optionally type who it is for, and confirm. A window shows the invite as text; [[Send as QR code]] shows it as a QR code."),
        ("fig", "invite-start"),
        ("fig", "invite-ready"),
        ("p", "Send it to one person in a private message: it works once, for 24 hours. Keep this computer on until they join."),
        ("p", "On the other device, open [this page](index.html?net=invite) and follow it with I have an invite."),
        ("p", "Once someone joins, make a second member an admin: [[Networks]] → [[Members]] → ⋯ → [[Make admin]]."),
    ]),
    ("exit", BOTH, ALL, "Choose an exit", "", [
        ("p", "An exit is a member whose internet connection your sites go through: sites see that member's address, not yours."),
        ("os", DESKTOP, [
            ("p", "On [[Choose an exit]], pick a member, or [[Directly, without an exit]] to keep your own connection. Below it, in [[This computer's name]], type a name others will see, for example `laptop`. Press [[Next]]."),
            ("fig", "exit-choose"),
            ("p", "Change it any time: tray icon → [[Exit via…]], or the Home tab of the node page."),
            ("fig", "exit-tray"),
            ("fig", "exit-status"),
            ("note", "The list is empty? No member offers an exit yet: computers and routers do by default, phones do not. Until another computer or router joins, sites open directly."),
        ]),
        ("os", ["android"], [
            ("p", "The app suggests an exit; change it if you want another member."),
            ("fig", "android-exit"),
        ]),
        ("p", "An exit sees which hosts you connect to, so pick members you trust. If the member goes offline, sites stop opening until you choose another."),
    ]),
    ("connect", ("invite",), ("android",), "Connect", "", [
        ("p", "Tap [[Connect]] at the bottom of the screen. Android asks to allow the app to set up a connection: press OK."),
        ("fig", "android-vpn"),
        ("p", "Allow notifications and background use when asked, so the connection is not stopped. The status line reads [[Connected via]] and the name of your exit."),
        ("fig", "android-connected"),
    ]),
    ("browser", BOTH, DESKTOP, "Connect the browser", "", [
        ("p", "The page asks [[Where should Mesh Town open sites?]] Choose [[All apps on this computer (recommended)]]."),
        ("p", "Press [[Copy]] next to the setup address (PAC), `http://127.0.0.1:1080/proxy.pac`."),
        ("fig", "browser-scope"),
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
                "Click [[OK]]. Repeat for Ethernet if you use both Wi-Fi and Ethernet.",
            ]),
            ("fig", "browser-m"),
        ]),
        BROWSERS[0],
        BROWSERS[1],
        ("fig", "browser-firefox"),
        ("p", "Then pick what happens [[When Mesh Town is off]]: [[Open sites directly]] or [[Keep sites closed]]."),
        CHECK,
    ]),
    ("devices", BOTH, ALL, "Open your devices", "", [
        ("os", DESKTOP, [
            ("p", "A device is reachable when a program on it is shared. On the device that runs the program, open the node page → [[Networks]] → your network → [[Shared services (ports)]] → [[My published ports]]: enter the port, choose [[All members]] or [[Selected members]] and press [[Publish port]]."),
            ("fig", "ports-mine"),
            ("p", "On this computer the same tab lists [[Ports shared with you]]. For a web panel, click its address, such as `http://nas.meshtown`: type http://, not https://."),
            ("fig", "ports-shared"),
            ("p", "For SSH, remote desktop and other programs, press [[Open on this computer]]. The port appears on `127.0.0.1`: for example, 22 becomes `127.0.0.1:2022`; connect your program there."),
            ("fig", "devices-scheme"),
            ("p", "To give a device a short name such as `nas`, change [[This computer's name]] on its node page."),
            ("note", "Names work only in a browser set up in the previous step, and only over http://. Only programs running on the device itself can be shared, not other machines on its local network."),
        ]),
        ("os", ["android"], [
            ("p", "With Mesh Town connected, type the address in any browser on the phone, for example `http://nas.meshtown`. There is nothing to set up in the browser: the app carries all of the phone's traffic."),
            ("note", "The app does not list shared ports yet: ask the member who shares a device for its address."),
        ]),
    ]),
]

END = {
    "title": "You are set",
    "lines": [
        "Open your node page: [http://127.0.0.1:7777/](http://127.0.0.1:7777/). If it opens, Mesh Town is running.",
        "Open [http://meshtown/](http://meshtown/): it says “This browser is connected to Mesh Town”.",
    ],
    "links": [
        ("Add another device", "index.html?net=invite"),
        ("Invite someone", "index.html?net=create#invite"),
        ("Update, remove, troubleshooting", "../install/index.html"),
    ],
}
