import sys
from aioframe.loaders import get_app_modules

sys.path.insert(0,'..')

__all__ = get_app_modules(__name__)
