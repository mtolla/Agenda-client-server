import sys
import os

project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)
from server.index import *

index.run()