from .version import VERSION
import sys
import os

__version__ = VERSION

# We need to import some modules in the root form other parts of the library.
# Like config.py, etc
sys.path.append(os.path.join(os.getcwd(), "caprice")) 
