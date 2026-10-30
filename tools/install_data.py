"""Data for the install pages of the Mesh Town site (one-off generator input).

Blocks are tuples: ("h3", text) ("p", text) ("cmd", code) ("warn", text) ("ol", [text, ...])
("out", sample output) ("label", caption before a code block)
("tabs", (group, [(key, label, [blocks]), ...])): variants of one OS as tabs; the same group name keeps
the choice in sync across the page.
Inline markup inside text: `code` and [label](url).
Each OS entry: three steps (title, blocks, anchor or None), an optional "after" section, "maintain",
"trouble" (question, answer) pairs and "docs" links.
"""

BLOB = "https://github.com/mesh-town/meshtown/blob/main/"
DIST = "https://github.com/mesh-town/meshtown-dist/raw/main/"
DOCS_INSTALL = ("Install reference", BLOB + "docs/INSTALL.md")
DOCS_USAGE = ("Usage reference", BLOB + "docs/USAGE.md")
DOCS_CONFIG = ("Settings file", BLOB + "docs/CONFIG-FILE.md")
DOCS_BUILD = ("Building from source", BLOB + "docs/BUILDING.md")
DOCS_ROUTER = ("Router notes", BLOB + "platforms/linux/build/openwrt/README.md")

LEDE_DESKTOP = "Three steps: the %s, the node page and your network. After that, shared devices open by name."
LEDE_ROUTER = "Three steps: the package, your network and the phones and computers behind the router."


def open_page(first):
    return ("Open the node page", [
        ("p", first),
        ("out", "Mesh Town page: http://127.0.0.1:7777/?token=…"),
        ("p", "The link works once and for 10 minutes. On the first visit, set a password; after that, sign in with it."),
    ], None)


OPEN_MAC = open_page("Start Mesh Town. The node page opens from the menu bar icon, or from the sign-in link printed at start:")
OPEN_WIN = open_page("Start Mesh Town. The node page opens from the tray icon, or from the sign-in link printed at start:")
OPEN_LINUX = open_page("Start `meshtown` for the tray app, or `meshtown-cli` in a terminal. The node page opens from the tray icon, or from the sign-in link printed at start (a service writes it to the system log):")

DESKTOP_NETWORK = ("Create or join a network", [
    ("p", "Press Create a new network and name it, for example `home-lab`. You become its first administrator; add a second one soon."),
    ("p", "To add a device or a person, press Invite a member: you get a single-use string, valid for a day, that does not contain the network key. Hand it over in person. The page also shows it as a link and a QR code; on Android, Scan QR reads it."),
    ("p", "On the new device, press Join with an invite and paste the string, or in a terminal:"),
    ("cmd", "meshtown run --invite mesh-invite2-…"),
    ("p", "Until a member is online, the node reports that it is waiting for network members."),
], None)

DESKTOP_AFTER = ("Open a device by its name", [
    ("p", "On the device that runs the service, open the network's Shared services (ports) tab and publish the port, to all members or to selected ones. Only programs running on that device itself can be shared."),
    ("p", "Each device has a name, two random words by default, such as finch-unwary; for a short one such as nas, set node.name in the settings file. The Ports shared with you tab shows the exact link for every port."),
    ("p", "In the browser: in your system's proxy settings, turn on automatic proxy configuration (PAC) and paste `http://127.0.0.1:1080/proxy.pac`. Then type the address with http://, for example `http://nas.meshtown`. Ordinary sites go through the node while Mesh Town runs and open directly while it is stopped; `*.meshtown` addresses work only through the node."),
    ("p", "For SSH, RDP and other programs, press Open on this computer: a member's port gets a local port, for example 22 becomes `127.0.0.1:2022`."),
])


def router_join(stop, cmd):
    return ("Join your network", [
        ("p", "A router node usually joins a network you already have. Ask a member for a single-use invite (Invite a member on their node page), then run this once while the service is stopped:"),
        ("cmd", stop + "\nmeshtown run --config " + cmd + " --invite mesh-invite2-…"),
        ("p", "Stop it with Ctrl+C once it reports joining, then start the service: the network is now saved in the settings file and survives restarts. To share the router's web panel with the network, see the [router notes](" + DOCS_ROUTER[1] + ")."),
    ], None)


ROUTER_DEVICES = ("Connect phones and computers", [
    ("p", "Phones, tablets and computers on the router's home network open sites through Mesh Town once their Wi‑Fi or network settings point to the router's setup address (PAC). iPhone and iPad work this way too — there is no app for them."),
    ("p", "First open the proxy for the home network: on the router's node page (port 7777) go through the setup steps and click \"Open for the home network\", or set `\"socks\": {\"access\": \"localnet\"}` in the settings file and restart the service."),
    ("p", "The setup address is `http://<router address>:1080/proxy.pac`, for example `http://192.168.1.1:1080/proxy.pac`. The node page shows the exact one."),
    ("ol", [
        "iPhone and iPad: \"Settings\" → \"Wi‑Fi\" → ⓘ next to the network → \"Configure Proxy\" → \"Automatic\", paste the address into \"URL\", \"Save\".",
        "Android: Wi‑Fi settings → the network → \"Proxy\" → \"Proxy Auto-Config\", paste the address into \"PAC URL\", \"Save\".",
        "macOS: \"System Settings\" → \"Network\" → the connection → \"Details…\" → \"Proxies\" → \"Automatic Proxy Configuration\".",
        "Windows: \"Settings\" → \"Network & internet\" → \"Proxy\" → \"Use setup script\" → \"Script address\".",
        "Linux (GNOME): \"Settings\" → \"Network\" → \"Proxy\" → \"Automatic\" → \"Configuration URL\".",
    ]),
    ("warn", "The proxy has no password: any device on the home network can use it, and so can guest Wi‑Fi unless it is separated. Do not open port 1080 on the WAN side."),
], "devices")

DEB_CMD = ("A=$(dpkg --print-architecture)\n"
           "wget https://mesh-town.github.io/meshtown-dist/linux/debian/meshtown_${A}.deb\n"
           "sudo apt install ./meshtown_${A}.deb")
TAR_CMD = ("curl -LO https://github.com/mesh-town/meshtown-dist/raw/main/linux/meshtown-linux-$(uname -m).tar.gz\n"
           "tar -xzf meshtown-linux-$(uname -m).tar.gz")

NO_DIRECT = "one of the networks may prevent direct connections; try another network, or add a member with a public address to the network: it relays the connection"
KEEP = " Keep config.json private."

OSES = [
    {
        "slug": "macos", "name": "macOS",
        "title": "Install Mesh Town on macOS",
        "description": "Install Mesh Town on a Mac with Homebrew or as an app, and connect it to your private network.",
        "lede": LEDE_DESKTOP % "app",
        "meta": "Apple silicon and Intel.",
        "steps": [
            ("Install", [
                ("tabs", ("macos", [
                    ("brew", "Homebrew", [
                        ("cmd", "brew install mesh-town/macos/meshtown\nmeshtown"),
                        ("p", "`meshtown` starts the menu bar app; `meshtown-cli` runs the node in a terminal. A Homebrew install is not marked as downloaded from the internet, so macOS does not stop the first launch."),
                    ]),
                    ("app", "App", [
                        ("p", "Download for [Apple silicon](" + DIST + "macos/MeshTown-macos-arm64.zip) or for [Intel](" + DIST + "macos/MeshTown-macos-x86_64.zip), unzip and move MeshTown.app to Applications."),
                        ("warn", "The app is signed ad hoc and is not notarized, so Gatekeeper stops the first launch of a zip downloaded in a browser. Open System Settings → Privacy & Security and press Open Anyway, or run:"),
                        ("cmd", "xattr -dr com.apple.quarantine /Applications/MeshTown.app"),
                    ]),
                ])),
            ], None),
            OPEN_MAC, DESKTOP_NETWORK,
        ],
        "after": DESKTOP_AFTER,
        "maintain": ("Update and remove", [("tabs", ("macos", [
            ("brew", "Homebrew", [("label", "Update"), ("cmd", "brew upgrade meshtown"), ("label", "Remove"), ("cmd", "brew uninstall meshtown")]),
            ("app", "App", [("p", "Update: download the zip again from the same link and replace MeshTown.app in Applications."), ("p", "Remove: quit Mesh Town and move MeshTown.app to the Trash.")]),
        ]))]),
        "trouble": [
            ("Homebrew refuses the formula after brew tap", "Newer Homebrew versions do not trust a new tap until you run:\n`brew trust mesh-town/macos`"),
            ("\"MeshTown\" cannot be opened", "See the Gatekeeper note above: Open Anyway, or remove the quarantine mark."),
            ("Where are the settings and logs?", "`~/Library/Application Support/meshtown/` holds config.json and the logs meshtown.log and meshtown-tray.log." + KEEP),
        ],
        "docs": [DOCS_INSTALL, DOCS_USAGE, DOCS_CONFIG],
    },
    {
        "slug": "windows", "name": "Windows",
        "title": "Install Mesh Town on Windows",
        "description": "Download Mesh Town for Windows and connect your PC to your private network.",
        "lede": LEDE_DESKTOP % "app",
        "meta": "64-bit Windows on x86.",
        "steps": [
            ("Install", [
                ("p", "Download [meshtown.exe](" + DIST + "windows/meshtown.exe), the tray app. For a terminal or a server there is [meshtown-cli.exe](" + DIST + "windows/meshtown-cli.exe)."),
                ("warn", "The program is not signed, so SmartScreen may warn on the first launch. Choose More info, then Run anyway."),
            ], None),
            OPEN_WIN, DESKTOP_NETWORK,
        ],
        "after": DESKTOP_AFTER,
        "maintain": ("Update", [("p", "Download the file again from the same link; it always points to the latest build.")]),
        "trouble": [
            ("SmartScreen warns", "See the note above."),
            ("Where are the settings and logs?", "`%APPDATA%\\meshtown\\` holds config.json and the logs meshtown.log and meshtown-tray.log." + KEEP),
            ("The other devices never appear", NO_DIRECT[0].upper() + NO_DIRECT[1:].replace("another network", "another network, such as home Wi-Fi") + "."),
        ],
        "docs": [DOCS_INSTALL, DOCS_USAGE, DOCS_CONFIG],
    },
    {
        "slug": "linux", "name": "Linux",
        "title": "Install Mesh Town on Linux",
        "description": "Install Mesh Town on Debian, Ubuntu or any Linux, as a desktop app or a server.",
        "lede": LEDE_DESKTOP % "package",
        "meta": "64-bit x86 and ARM.",
        "steps": [
            ("Install", [
                ("tabs", ("linux", [
                    ("apt", "Debian / Ubuntu", [
                        ("cmd", DEB_CMD),
                        ("p", "The package adds a signed apt repository, so later updates come with apt, and installs the meshtown service, stopped. On a desktop, run `meshtown` for the tray app and leave the service off."),
                        ("p", "On a server, join your network first with an invite from a member (step 3):"),
                        ("cmd", "sudo meshtown run --config /etc/meshtown/config.json --invite mesh-invite2-…"),
                        ("p", "Stop it with Ctrl+C once it reports joining, then start the service:"),
                        ("cmd", "sudo systemctl enable --now meshtown"),
                    ]),
                    ("static", "Other Linux", [
                        ("cmd", TAR_CMD),
                        ("p", "Run `meshtown` for the tray app, or `meshtown-cli` in a terminal or on a server. For the console-only archive, use `meshtown-cli-linux-$(uname -m).tar.gz` in the same place."),
                    ]),
                ])),
            ], None),
            OPEN_LINUX, DESKTOP_NETWORK,
        ],
        "after": DESKTOP_AFTER,
        "maintain": ("Update and remove", [("tabs", ("linux", [
            ("apt", "Debian / Ubuntu", [("label", "Update"), ("cmd", "sudo apt update && sudo apt upgrade"), ("label", "Remove"), ("cmd", "sudo apt remove meshtown")]),
            ("static", "Other Linux", [("p", "Update: download the archive again and unpack it over the old files."), ("p", "Remove: delete the unpacked files.")]),
        ]))]),
        "trouble": [
            ("The service does not start by itself", "It is installed stopped on purpose:\n`sudo systemctl enable --now meshtown`"),
            ("Where is the settings file?", "`/etc/meshtown/config.json` for the service, `~/.config/meshtown/config.json` for a user. Keep it private; `meshtown config-path` prints the one in use."),
            ("The other devices never appear", NO_DIRECT[0].upper() + NO_DIRECT[1:] + "."),
        ],
        "docs": [("Install reference (apt)", BLOB + "docs/INSTALL.md#debian-ubuntu-apt"), DOCS_USAGE, DOCS_CONFIG, DOCS_BUILD],
    },
    {
        "slug": "android", "name": "Android",
        "title": "Install Mesh Town on Android",
        "description": "Install the Mesh Town app on an Android phone and join your private network.",
        "lede": "Three steps: the app, the first launch and your network. The phone is then a member like any other device.",
        "meta": "64-bit ARM phones with Android 7.0 or newer; the app is installed from a file.",
        "steps": [
            ("Install", [("ol", [
                "On the phone, download [meshtown.apk](" + DIST + "android/meshtown.apk).",
                "Open the file. Android asks to allow installing apps from this source: allow it.",
                "Start Mesh Town.",
            ])], None),
            ("Open the app", [("p", "The app opens with the Members and Device settings tabs.")], None),
            ("Join your network", [
                ("p", "Ask a member of your network to press Invite a member on their node page and give you the single-use string. Join with it: paste the link, or press Scan QR and photograph the QR code on their node page."),
                ("p", "On the first connect, Android may ask for permission to show notifications (Android 13 and newer), then shows a system window asking to allow the app to set up a connection: press OK. Once, it also asks about running in the background and battery use; allow it so the connection is not stopped."),
            ], None),
        ],
        "after": None,
        "maintain": ("Update", [("p", "Download the file again from the same link and install it over the old one.")]),
        "trouble": [
            ("Android does not offer to install the file", "Allow installing unknown apps for the browser or file manager you opened it from."),
            ("The app does not install", "It needs a 64-bit ARM phone and Android 7.0 or newer."),
            ("No connection on mobile data", "Some mobile operators prevent direct connections between nodes; try Wi-Fi, or add a member with a public address to the network: it relays the connection."),
        ],
        "docs": [DOCS_INSTALL, DOCS_USAGE],
    },
    {
        "slug": "openwrt", "name": "OpenWrt",
        "title": "Install Mesh Town on an OpenWrt router",
        "description": "Install Mesh Town on an OpenWrt router so its services join your private network.",
        "lede": LEDE_ROUTER,
        "meta": "OpenWrt 24.10 and 25.12 on 64-bit ARM, 32-bit ARM Cortex and x86_64. MIPS, ARMv5/v6 and 32-bit x86 routers are not covered yet.",
        "steps": [
            ("Install", [
                ("p", "As root on the router:"),
                ("cmd", "wget -O- https://mesh-town.github.io/meshtown-openwrt/install.sh | sh"),
                ("p", "The service starts at boot."),
            ], None),
            router_join("/etc/init.d/meshtown stop", "/etc/meshtown/config.json"),
            ROUTER_DEVICES,
        ],
        "after": None,
        "maintain": ("Update", [
            ("label", "OpenWrt 24.10"), ("cmd", "opkg update && opkg upgrade meshtown"),
            ("label", "OpenWrt 25.12"), ("cmd", "apk update && apk upgrade meshtown"),
        ]),
        "trouble": [
            ("My router has a MIPS chip", "MIPS, ARMv5/v6 and 32-bit x86 routers are not covered yet."),
            ("Where is the settings file?", "`/etc/meshtown/config.json`. Keep it private."),
        ],
        "docs": [DOCS_ROUTER, DOCS_INSTALL, DOCS_USAGE],
    },
    {
        "slug": "keenetic", "name": "Keenetic",
        "title": "Install Mesh Town on a Keenetic router (experimental)",
        "description": "Experimental: install Mesh Town on a Keenetic router with Entware.",
        "lede": LEDE_ROUTER,
        "meta": "Keenetic routers with Entware, MIPS and 64-bit ARM.",
        "steps": [
            ("Install", [
                ("warn", "Experimental. The package has not been tested on a live KeeneticOS router yet."),
                ("p", "Entware must be installed on the router. Over SSH:"),
                ("cmd", "wget -O- https://mesh-town.github.io/meshtown-keenetic/install.sh | sh"),
                ("p", "The node runs as the service `/opt/etc/init.d/S99meshtown`."),
            ], None),
            router_join("/opt/etc/init.d/S99meshtown stop", "/opt/etc/meshtown/config.json"),
            ROUTER_DEVICES,
        ],
        "after": None,
        "maintain": ("Update", [("cmd", "opkg update && opkg upgrade meshtown")]),
        "trouble": [
            ("The script stops with exit code 1", "Entware is not installed."),
            ("The script stops with exit code 2", "The router's architecture is not supported."),
            ("Where is the settings file?", "`/opt/etc/meshtown/config.json`. Keep it private."),
        ],
        "docs": [DOCS_INSTALL, DOCS_USAGE],
    },
]

INDEX = {
    "title": "Install Mesh Town",
    "description": "Pick your system and install Mesh Town: macOS, Windows, Linux, Android, OpenWrt or Keenetic.",
    "lede": "Pick your system. Each guide covers the install, the node page and joining your network.",
    "cards": [
        ("macos", "macOS", "Menu bar app · Apple silicon and Intel"),
        ("windows", "Windows", "Tray app · 64-bit x86"),
        ("linux", "Linux", "Tray app or service · x86 and ARM"),
        ("android", "Android", "App from a file · Android 7.0 or newer"),
        ("openwrt", "OpenWrt", "Router service · OpenWrt 24.10 and 25.12"),
        ("keenetic", "Keenetic", "Router service · Entware, experimental"),
    ],
    "after": [
        "There is no app for iPhone or iPad; they can use Mesh Town on a router: see [connecting devices](openwrt/index.html#devices).",
        "Checksums and all release files are in the [downloads repository](https://github.com/mesh-town/meshtown-dist); files without a version in the name are always the latest build.",
    ],
}
