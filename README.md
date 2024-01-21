
# Pathfinding Visualizer

PathfindingVisualizer is an interactive tool built with the Kivy framework, designed to demonstrate the workings of A* and Branch and Bound algorithms. It provides a visually engaging and intuitive way to understand pathfinding algorithms based on scenarios from the Pathfinding project.

## Features

- **Interactive menu**: Click to create predefined obstacles, start points, and end points on a grid.
- **Algorithm Selection**: Choose between A* and Branch and Bound algorithms. (More algorithms may be added in the future)
- **Real-Time Visualization**: Watch the algorithms in action as they search for the shortest path.
- **Performance Metrics**: View the number of nodes explored and the time taken for each algorithm run.

## Project Structure

The project is organized into two main directories for better organization and maintainability:

- `src`: Contains the source code files.
  - `algorithms.py`: Implementation of the A* and Branch and Bound algorithms.
  - `app.py`: Initializes and runs the Kivy application.
  - `constants.py`: Defines various constants used throughout the project.
  - `grid_components.py`: Manages the grid components, including obstacles, start points, and end points.
  - `utilities.py`: Provides utility functions used across the project.
- Root Directory: Contains the main entry point of the application.
  - `main.py`: Responsible for setting up and starting the app.

## Downloading the Release

Download the latest version of PathfindingVisualizer from the Releases section of this repository. The release includes a standalone executable file that you can run on your system.

## Dependencies

Before running PathfindingVisualizer from the source, ensure you have the following dependencies installed:

- `Kivy`: For the graphical user interface.
- `numpy`: Used for mathematical operations and array manipulations.

You can install these dependencies using pip:

```bash
pip install kivy numpy
```

## Installation

To run PathfindingVisualizer from source:

1. Clone the repository.
2. Install the required dependencies.
3. Navigate to the root directory of the project.
4. Run `main.py` with Python.

## Building Standalone Executable from Source

To create a standalone executable from the source code, you can use PyInstaller with the following command:

```shell
pyinstaller --onefile --windowed --paths=./src main.py
```
This will generate a single executable file in the dist directory.

## Contributing

Contributions to the PathfindingVisualizer are welcome. Please read the contributing guidelines before making a pull request.

## License

PathfindingVisualizer is licensed under [MIT License](LICENSE).
