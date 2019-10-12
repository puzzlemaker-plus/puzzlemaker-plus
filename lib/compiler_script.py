import os
import sys

commands = {'linux':
    {'fast': '''~/.steam/steamapps/common/Portal\ 2/bin/vbsp_linux -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vvis_linux -fast -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vrad_linux -bounce 2 -noextra -game Portal\ 2 export.vmf
cp export.bsp ~/.steam/steamapps/common/Portal\ 2/
~/.steam/steamapps/common/Portal\ 2/portal2_linux -dev -game Portal\ 2 +map export.bsp +sv_lan 1''',

    'default': '''~/.steam/steamapps/common/Portal\ 2/bin/vbsp_linux -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vvis_linux -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vrad_linux -game Portal\ 2 export.vmf
cp export.bsp ~/.steam/steamapps/common/Portal\ 2/
~/.steam/steamapps/common/Portal\ 2/portal2_linux -dev -game Portal\ 2 +map export.bsp +sv_lan 1''',

    'full': '''~/.steam/steamapps/common/Portal\ 2/bin/vbsp_linux -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vvis_linux -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vrad_linux -both -final -textureshadows -StaticPropLighting -StaticPropPolys -game Portal\ 2 export.vmf
cp export.bsp ~/.steam/steamapps/common/Portal\ 2/
~/.steam/steamapps/common/Portal\ 2/portal2_linux -dev -game Portal\ 2 +map export.bsp +sv_lan 1'''},


        'darwin': {'fast': '''~/.steam/steamapps/common/Portal\ 2/bin/vbsp_osx -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vvis_osx -fast -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vrad_osx -bounce 2 -noextra -game Portal\ 2 export.vmf
cp export.bsp ~/.steam/steamapps/common/Portal\ 2/
~/.steam/steamapps/common/Portal\ 2/portal2_osx -dev -game Portal\ 2 +map export.bsp +sv_lan 1''',

    'default': '''~/.steam/steamapps/common/Portal\ 2/bin/vbsp_osx -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vvis_osx -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vrad_osx -game Portal\ 2 export.vmf
cp export.bsp ~/.steam/steamapps/common/Portal\ 2/
~/.steam/steamapps/common/Portal\ 2/portal2_osx -dev -game Portal\ 2 +map export.bsp +sv_lan 1''',

    'full': '''~/.steam/steamapps/common/Portal\ 2/bin/vbsp_osx -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vvis_osx -game Portal\ 2 export.vmf
~/.steam/steamapps/common/Portal\ 2/bin/vrad_osx -both -final -textureshadows -StaticPropLighting -StaticPropPolys -game Portal\ 2 export.vmf
cp export.bsp ~/.steam/steamapps/common/Portal\ 2/
~/.steam/steamapps/common/Portal\ 2/portal2_osx -dev -game Portal\ 2 +map export.bsp +sv_lan 1'''},

            
        'win32':
            {'fast': r'''"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\bin\vbsp.exe" -game "Portal 2" export.vmf
"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\bin\vvis.exe" -fast -game "Portal 2" export.vmf
"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\bin\vrad.exe" -bounce 2 -noextra -game "Portal 2" export.vmf
copy export.bsp "C:\Program Files (x86)\Steam\steamapps\common\Portal 2"
"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\portal2.exe" -dev -game "Portal 2" +map export.bsp +sv_lan 1''',

'default': r'''"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\bin\vbsp.exe" -game "Portal 2" export.vmf
"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\bin\vvis.exe" -game "Portal 2" export.vmf
"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\bin\vrad.exe" -game "Portal 2" export.vmf
copy export.bsp "C:\Program Files (x86)\Steam\steamapps\common\Portal 2"
"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\portal2.exe" -dev -game "Portal 2" +map export.bsp +sv_lan 1''',

'full': r'''"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\bin\vbsp.exe" -game "Portal 2" export.vmf
"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\bin\vvis.exe" -game "Portal 2" export.vmf
"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\bin\vrad.exe" -both -final -textureshadows -StaticopyropLighting -StaticopyropPolys -game "Portal 2" export.vmf
copy export.bsp "C:\Program Files (x86)\Steam\steamapps\common\Portal 2"
"C:\Program Files (x86)\Steam\steamapps\common\Portal 2\portal2.exe" -dev -game "Portal 2" +map export.bsp +sv_lan 1'''}}

def load(vmf, power = 'default'):
    os.system(commands[sys.platform][power])
