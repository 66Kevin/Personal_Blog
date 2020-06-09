# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys
from django.core.wsgi import get_wsgi_application
#
## assuming your django settings file is at '/home/yueyi/mysite/mysite/settings.py'
## and your manage.py is is at '/home/yueyi/mysite/manage.py'
path = '/home/yueyi/Personal_Blog/blogProject'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'blogProject.settings'

application = get_wsgi_application()