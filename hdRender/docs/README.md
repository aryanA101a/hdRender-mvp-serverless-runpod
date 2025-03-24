# Steps to deploy(VAST.ai)

1. Download Blender
`wget https://mirror.freedif.org/blender/release/Blender4.2/blender-4.2.0-linux-x64.tar.xz`

2. `tar -xvf blender-4.2.0-linux-x64.tar.xz`

3. Install Blender dependencies
`sudo apt install libx11-dev libxxf86vm-dev libxfixes-dev libxi-dev libxkbcommon-dev libsm-dev libgl-dev`

4. Add blender to path.

5. `git clone https://github.com/Remsy2027/HD_Render_Code && cd HD_Render_Code`

6. Setup venv
```
python3 -m venv .venv
source .venv/bin/activate
```

7. `pip install -r requirements.txt`

8. Install pm2

9. `pm2 --name=hdrender start "gunicorn -c gunicorn_config.py main:app"`

 
