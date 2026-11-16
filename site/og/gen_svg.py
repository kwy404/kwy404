import base64, os, sys
here = os.path.dirname(os.path.abspath(__file__))
site = os.path.dirname(here)
sys.path.insert(0, site)
import art
b64 = base64.b64encode(open(os.path.join(site, 'assets', 'avatar.jpg'), 'rb').read()).decode()
open(os.path.join(here, 'og.svg'), 'w').write(art.og_svg(214, 59, 'data:image/jpeg;base64,' + b64))
