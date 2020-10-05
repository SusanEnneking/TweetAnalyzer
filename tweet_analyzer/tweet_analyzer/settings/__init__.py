from .base import *
#local, dev...no prod, yet
if os.environ['DJANGO_ENVIRONMENT'] == 'local':
   pass
else:
   from .dev import *