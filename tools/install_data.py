"""Data for the install pages of the Mesh Town site (one-off generator input).

Blocks are tuples: ("h3", text) ("p", text) ("cmd", code) ("warn", text) ("ol", [text, ...]).
Inline markup inside text: `code` and [label](url).
"""

BLOB = "https://github.com/mesh-town/meshtown/blob/main/"
DIST = "https://github.com/mesh-town/meshtown-dist/raw/main/"
DOCS_INSTALL = ("Install reference", BLOB + "docs/INSTALL.md")
DOCS_USAGE = ("Usage reference", BLOB + "docs/USAGE.md")
DOCS_CONFIG = ("Settings file", BLOB + "docs/CONFIG-FILE.md")
DOCS_BUILD = ("Building from source", BLOB + "docs/BUILDING.md")
DOCS_ROUTER = ("Router notes", BLOB + "platforms/linux/build/openwrt/README.md")

def desktop_check(first):
    return [
    ("p", first),
    ("cmd", "Mesh Town page: http://127.0.0.1:7777/?token=…"),
    ("p", "On the first visit, the page asks you to set a password. The sign-in link works once and for 10 minutes; after that, sign in with that password."),
    ]


DESKTOP_CHECK_MAC = desktop_check("The node page opens from the menu bar icon, or with the sign-in link printed at start:")
DESKTOP_CHECK_TRAY = desktop_check("The node page opens from the tray icon, or with the sign-in link printed at start:")

DESKTOP_NETWORK = [
    ("p", "On the node page, press Create a new network and give it a name, for example `home-lab`. You become its first administrator; making a second administrator soon is a good idea."),
    ("p", "To add a device or a person, press Invite a member. You get a single-use string, valid for a day, that does not contain the network key. Hand it over in person. The node page shows the invite as a link and a QR code; on Android, the Scan QR button reads it."),
    ("p", "On the new device, press Join with an invite and paste the string. In a terminal:"),
    ("cmd", "meshtown run --invite mesh-invite2-…"),
    ("p", "If no member is online yet, the node shows that it is waiting for network members."),
]

DESKTOP_OPEN = [
    ("p", "On the device with the web interface, open the network's Shared services (ports) tab and publish the port, shared with all members or selected ones. Only programs running on that device itself can be shared."),
    ("p", "Each device has a name: two random words by default, such as finch-unwary. The Ports shared with you tab shows the exact link. To use a short name such as nas, set node.name in the settings file."),
    ("p", "On your computer, in your system's proxy settings, turn on automatic proxy configuration and paste `http://127.0.0.1:1080/proxy.pac` (Firefox: Settings → General → Network Settings → Automatic proxy configuration URL). Then type the address with http://, for example `http://nas.meshtown`. The Ports shared with you tab shows each link. Ordinary sites go through the node while Mesh Town runs and open directly while it is stopped; `*.meshtown` addresses work only through the node."),
    ("p", "For SSH, RDP and other programs, use Open on this computer: a member's port gets a local port, for example 22 becomes `127.0.0.1:2022`."),
]

ANDROID_NETWORK = [
    ("p", "Ask a member of your network to press Invite a member on their node page and give you the single-use string. Open Mesh Town on the phone and join with it: paste the link, or press Scan QR and photograph the QR code shown on their node page."),
    ("p", "On the first connect Android may ask for permission to show notifications (Android 13 and newer). It then shows a system window asking to allow the app to set up a connection: press OK. Once, it also shows a screen about running in the background and battery use; allow it so the connection is not stopped."),
]
ANDROID_OPEN = [
    ("p", "The phone is a member of the network like any other device. For details, see the [usage reference](" + BLOB + "docs/USAGE.md)."),
]
def router_network(stop, cmd):
    return [
    ("p", "A router node usually joins a network you already have. Ask a member for a single-use invite (Invite a member on their node page), then run this once" + stop + ":"),
    ("cmd", cmd),
    ("p", "The command saves the network to the settings file, so after a restart the service stays in the network without the invite. Stop it with Ctrl+C once it reports joining, then start the service. To share the router's web panel with the network, see the router notes."),
    ("p", "[Router notes](" + DOCS_ROUTER[1] + ") · [Usage reference](" + BLOB + "docs/USAGE.md" + ")"),
    ]


ROUTER_NETWORK = router_network(" while the service is stopped", "/etc/init.d/meshtown stop\nmeshtown run --config /etc/meshtown/config.json --invite mesh-invite2-…")
KEENETIC_NETWORK = router_network(" while the service is stopped", "/opt/etc/init.d/S99meshtown stop\nmeshtown run --config /opt/etc/meshtown/. --invite mesh-invite2-…")

NO_DIRECT = "one of the networks may prevent direct connections; try another network"
KEEP = " Keep config.json private."

OSES = [
    {
        "slug": "macos", "name": "macOS",
        "title": "Install Mesh Town on macOS",
        "description": "Install Mesh Town on a Mac with Homebrew or as an app, and connect it to your private network.",
        "lede": "For Macs with Apple silicon or Intel.",
        "install": [
            ("h3", "With Homebrew (recommended)"),
            ("cmd", "brew install mesh-town/meshtown/meshtown\nmeshtown"),
            ("p", "`meshtown` starts the menu bar app; `meshtown-cli` runs the node in a terminal. A Homebrew install is not marked as downloaded from the internet, so macOS does not stop the first launch."),
            ("h3", "As an app"),
            ("p", "Download for [Apple silicon](" + DIST + "macos/MeshTown-macos-arm64.zip) or for [Intel](" + DIST + "macos/MeshTown-macos-x86_64.zip), unzip and move MeshTown.app to Applications."),
            ("warn", "The app is signed ad hoc and is not notarized, so Gatekeeper stops the first launch of a zip downloaded in a browser. Open System Settings → Privacy & Security and press Open Anyway, or run:"),
            ("cmd", "xattr -dr com.apple.quarantine /Applications/MeshTown.app"),
        ],
        "check": DESKTOP_CHECK_MAC, "network": ("3. Create or join a network", DESKTOP_NETWORK),
        "open": ("4. Open a device by its name", DESKTOP_OPEN),
        "update": [("cmd", "brew upgrade meshtown")],
        "remove": [("cmd", "brew uninstall meshtown")],
        "trouble": [
            ("Homebrew refuses the formula after brew tap", "Newer Homebrew versions do not trust a new tap until you run:\n`brew trust mesh-town/meshtown`"),
            ("\"MeshTown\" cannot be opened", "See the Gatekeeper note above: Open Anyway, or remove the quarantine mark."),
            ("Where are the settings and logs?", "`~/Library/Application Support/meshtown/` holds config.json and the logs meshtown.log and meshtown-tray.log." + KEEP),
        ],
        "docs": [DOCS_INSTALL, DOCS_USAGE, DOCS_CONFIG],
    },
    {
        "slug": "windows", "name": "Windows",
        "title": "Install Mesh Town on Windows",
        "description": "Download Mesh Town for Windows and connect your PC to your private network.",
        "lede": "For 64-bit Windows on x86.",
        "install": [
            ("h3", "Download"),
            ("p", "Tray app: [meshtown.exe](" + DIST + "windows/meshtown.exe)"),
            ("p", "Console: [meshtown-cli.exe](" + DIST + "windows/meshtown-cli.exe), for a terminal or a server."),
            ("warn", "The program is not signed, so SmartScreen may warn on the first launch. Choose More info, then Run anyway."),
        ],
        "check": DESKTOP_CHECK_TRAY, "network": ("3. Create or join a network", DESKTOP_NETWORK),
        "open": ("4. Open a device by its name", DESKTOP_OPEN),
        "update": [("p", "Download the file again from the same link; the files without a version in the name are always the latest build.")],
        "remove": [],
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
        "lede": "For 64-bit x86 and ARM. Debian and Ubuntu get an apt package; other distributions use a static build.",
        "install": [
            ("h3", "Debian and Ubuntu (apt)"),
            ("p", "x86_64:"),
            ("cmd", "wget https://mesh-town.github.io/meshtown-dist/linux/debian/meshtown_amd64.deb\nsudo apt install ./meshtown_amd64.deb"),
            ("p", "ARM64:"),
            ("cmd", "wget https://mesh-town.github.io/meshtown-dist/linux/debian/meshtown_arm64.deb\nsudo apt install ./meshtown_arm64.deb"),
            ("p", "The package adds a signed apt repository, so later updates come with apt. It also installs a meshtown service, stopped. On a server, first join your network with an invite from a member (it is saved to the service's settings file), stop it with Ctrl+C once it reports joining, then start the service:"),
            ("cmd", "sudo meshtown run --config /etc/meshtown/config.json --invite mesh-invite2-…"),
            ("cmd", "sudo systemctl enable --now meshtown"),
            ("p", "The service reads `/etc/meshtown/config.json`. On a desktop with the tray app, leave the service off."),
            ("h3", "Any distribution (static build)"),
            ("p", "Tray app: [meshtown-linux-x86_64.tar.gz](" + DIST + "linux/meshtown-linux-x86_64.tar.gz) · [meshtown-linux-aarch64.tar.gz](" + DIST + "linux/meshtown-linux-aarch64.tar.gz)"),
            ("p", "Console only: [meshtown-cli-linux-x86_64.tar.gz](" + DIST + "linux/meshtown-cli-linux-x86_64.tar.gz) · [meshtown-cli-linux-aarch64.tar.gz](" + DIST + "linux/meshtown-cli-linux-aarch64.tar.gz)"),
            ("cmd", "curl -LO https://github.com/mesh-town/meshtown-dist/raw/main/linux/meshtown-linux-x86_64.tar.gz\ntar -xzf meshtown-linux-x86_64.tar.gz"),
            ("p", "Run `meshtown` for the tray app, or `meshtown-cli` in a terminal or on a server."),
        ],
        "check": DESKTOP_CHECK_TRAY, "network": ("3. Create or join a network", DESKTOP_NETWORK),
        "open": ("4. Open a device by its name", DESKTOP_OPEN),
        "update": [("cmd", "sudo apt update && sudo apt upgrade"), ("p", "For a static build, download the archive again.")],
        "remove": [("cmd", "sudo apt remove meshtown")],
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
        "lede": "For 64-bit ARM phones with Android 7.0 or newer. The app is installed from a file.",
        "install": [
            ("ol", [
                "On the phone, download [meshtown.apk](" + DIST + "android/meshtown.apk).",
                "Open the file. Android asks to allow installing apps from this source: allow it.",
                "Start Mesh Town.",
            ]),
        ],
        "check": [("p", "The app opens and shows the Members and Device settings tabs.")],
        "network": ("3. Join your network", ANDROID_NETWORK),
        "open": ("What the phone can do", ANDROID_OPEN),
        "update": [("p", "Download the file again from the same link and install it over the old one.")],
        "remove": [],
        "trouble": [
            ("Android does not offer to install the file", "Allow installing unknown apps for the browser or file manager you opened it from."),
            ("The app does not install", "It needs a 64-bit ARM phone and Android 7.0 or newer."),
            ("No connection on mobile data", "Some mobile operators prevent direct connections between nodes; try Wi-Fi."),
        ],
        "docs": [DOCS_INSTALL, DOCS_USAGE],
    },
    {
        "slug": "openwrt", "name": "OpenWrt",
        "title": "Install Mesh Town on an OpenWrt router",
        "description": "Install Mesh Town on an OpenWrt router so its services join your private network.",
        "lede": "For OpenWrt 24.10 and 25.12 on 64-bit ARM, 32-bit ARM Cortex and x86_64. MIPS, ARMv5/v6 and 32-bit x86 routers are not covered yet.",
        "install": [
            ("p", "As root on the router:"),
            ("cmd", "wget -O- https://mesh-town.github.io/meshtown-openwrt/install.sh | sh"),
            ("p", "The service starts at boot."),
        ],
        "check": [],
        "network": ("2. Join your network", ROUTER_NETWORK),
        "open": None,
        "update": [
            ("p", "OpenWrt 24.10:"), ("cmd", "opkg update && opkg upgrade meshtown"),
            ("p", "OpenWrt 25.12:"), ("cmd", "apk update && apk upgrade meshtown"),
        ],
        "remove": [],
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
        "lede": "For Keenetic routers with Entware, MIPS and 64-bit ARM.",
        "install": [
            ("warn", "Experimental. The package has not been tested on a live KeeneticOS router yet."),
            ("p", "Entware must be installed on the router. Over SSH:"),
            ("cmd", "wget -O- https://mesh-town.github.io/meshtown-keenetic/install.sh | sh"),
            ("p", "The node runs as the service `/opt/etc/init.d/S99meshtown`."),
        ],
        "check": [],
        "network": ("2. Join your network", KEENETIC_NETWORK),
        "open": None,
        "update": [("cmd", "opkg update && opkg upgrade meshtown")],
        "remove": [],
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
    "lede": "Pick your system.",
    "cards": [
        ("macos", "macOS", "Homebrew or app, Apple silicon and Intel"),
        ("windows", "Windows", "64-bit x86"),
        ("linux", "Linux", "apt for Debian and Ubuntu, static builds for x86_64 and ARM64"),
        ("android", "Android", "app from a file, Android 7.0 or newer"),
        ("openwrt", "OpenWrt", "routers on 24.10 and 25.12"),
        ("keenetic", "Keenetic", "routers with Entware (experimental)"),
    ],
    "after": [
        "Mesh Town does not run on iPhone or iPad.",
        "Checksums and all release files are in the [downloads repository](https://github.com/mesh-town/meshtown-dist); files without a version in the name are always the latest build.",
    ],
}
