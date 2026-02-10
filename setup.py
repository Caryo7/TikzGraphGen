content = """[Desktop Entry]
Comment[fr_FR]=Une simple interface pour créer des courbes Tikz
Comment=
Exec={path}/TikzGraphGen
GenericName[fr_FR]=
GenericName=
Icon={path}/image.png
MimeType=
Name[fr_FR]=TikzGraphGen
Name=TikzGraphGen
Path={path}
StartupNotify=true
Terminal=false
TerminalOptions=
Type=Application
X-KDE-SubstituteUID=false
X-KDE-Username=
"""

import os
path = os.path.abspath('.')
f = open('tikzgraphgen.desktop', 'w')
f.write(content.format(path = path))
f.close()
