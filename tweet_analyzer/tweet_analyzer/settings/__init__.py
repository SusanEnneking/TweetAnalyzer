import os
from .base import *

if os.environ['DJANGO_ENVIRONMENT'] == 'local':
    pass
elif os.environ['DJANGO_ENVIRONMENT'] == 'dev':
    from .dev import *
else:
    from .prod import *
