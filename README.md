
# Pathfinding Visualizer

PathfindingVisualizer is an interactive tool built with the Kivy framework, designed to demonstrate the workings of A* and Branch and Bound algorithms. It provides a visually engaging and intuitive way to understand pathfinding algorithms based on scenarios from the Pathfinding project.

## Features

- **Interactive menu**: Click to create predefined obstacles, start points, and end points on a grid.
- **Algorithm Selection**: Choose between A* and Branch and Bound algorithms. (More algorithms may be added in the future)
- **Real-Time Visualization**: Watch the algorithms in action as they search for the shortest path.
- **Performance Metrics**: View the number of nodes explored and the time taken for each algorithm run.

## Modular File Structure

The project is structured into several modular files for better organization and maintainability:

- `algorithms.py`: Contains the implementation of the A* and Branch and Bound algorithms.
- `app.py`: The main application file that initializes and runs the Kivy application.
- `constants.py`: Defines various constants used throughout the project.
- `grid_components.py`: Manages the grid components, including obstacles, start points, and end points.
- `main.py`: The entry point of the application, responsible for setting up and starting the app.
- `utilities.py`: Provides utility functions used across the project.

## Downloading the Release

Download the latest version of PathfindingVisualizer from the Releases section of this repository. The release includes a standalone executable file that you can run on your system.

## Installation

To run PathfindingVisualizer from source:

1. Clone the repository.
2. Install the required dependencies.
3. Run `main.py`.

## Contributing

Contributions to the PathfindingVisualizer are welcome. Please read the contributing guidelines before making a pull request.

## License

PathfindingVisualizer is licensed under [MIT License](LICENSE).

## Acknowledgments

Special thanks to all contributors and supporters of the Pathfinding Visualizer project.
