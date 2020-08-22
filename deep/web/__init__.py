# @copyright (c) 2019 dyvniy. All rights reserved.
# encoding: utf-8
"""NVovk msServerEmulator"""

__version__ = "0.0.1."
__package_license__ = "NVovk"
__package_info__ = "Nick Vovk's backend"

__team_email__ = "dyvniy@yandex.ru"
__author_info__ = [
    ("Nikolay Vovk", "dyvniy@yandex.ru"),
]
__service_short_name__ = "logser"

__author__ = ", ".join("{} <{}>".format(*info) for info in __author_info__)

__all__ = [
    "__author__",
    "__version__",
    "__author_info__",
    "__package_info__",
    "__package_license__",
    "__team_email__",
]

from web.main import main
