"""
Inicializador del módulo de configuración.

Por defecto se cargan los settings de desarrollo.
En producción, este archivo puede modificarse
o sobreescribirse mediante DJANGO_SETTINGS_MODULE.
"""

from .dev import *
from .base import *
from .mongo import init_mongo

init_mongo()
