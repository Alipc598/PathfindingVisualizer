import sys
import os

src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)

from app import PathfindingVisualizerApp

if __name__ == '__main__':
    app = PathfindingVisualizerApp()
    app.run()
