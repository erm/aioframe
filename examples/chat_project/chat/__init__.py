import sys
from aioframe.apps.loaders import get_app_modules

sys.path.insert(0,'..')

__all__ = get_app_modules(__name__)
