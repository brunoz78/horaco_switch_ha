"""Make the scraper importable without Home Assistant.

custom_components/horaco_switch/__init__.py imports homeassistant, so the
package is registered here as a bare namespace; scraper.py and const.py only
need aiohttp and beautifulsoup4.
"""
import pathlib
import sys
import types

COMPONENT = pathlib.Path(__file__).resolve().parent.parent / "custom_components" / "horaco_switch"

if "horaco_switch" not in sys.modules:
    pkg = types.ModuleType("horaco_switch")
    pkg.__path__ = [str(COMPONENT)]
    sys.modules["horaco_switch"] = pkg
