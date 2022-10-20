try:
    from server.settings.local import *
except ImportError:
    from server.settings.default import *
