# mesh-town.github.io

**[Mesh Town](https://mesh-town.github.io/)** — reach your home server, NAS or office PC from anywhere: no port forwarding, no central server, no accounts.

The website of Mesh Town: reach the services on your devices from anywhere.

Plain static files, no build step, no external resources.

Open locally:
- open `index.html` in a browser, or
- run `python3 -m http.server 8000` in this folder and go to http://localhost:8000/

The app itself lives at https://github.com/mesh-town/meshtown.

The install pages (`install/**/index.html`) are generated: edit `tools/install_data.py`, then run
`python3 -I tools/gen_install.py .` from this folder and commit the regenerated pages together with the data.
