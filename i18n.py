import gettext
import os

LOCALEDIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
TRANSLATE = gettext.translation('status_light_controller', LOCALEDIR,
                                fallback=True)

_ = TRANSLATE.gettext