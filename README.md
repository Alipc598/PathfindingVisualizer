
# Pathfinding Visualizer

PathfindingVisualizer is an interactive built with the Kivy framework. It's designed to demonstrate the workings of A* and Branch and Bound, in a visually engaging and intuitive way based on scenarios of my Pathfinding project.

## Features

- **Interactive menu**: Click to create predefined obstacles, start points, and end points on a grid.
- **Algorithm Selection**: Choose between A* and Branch and Bound algorithms to see how each one navigates the grid. (Will probably add more later)
- **Real-Time Visualization**: Watch the algorithm in action as it searches for the shortest path.
- **Performance Metrics**: View the number of nodes explored and the time taken for each algorithm run.

## Downloading the Release

You can download the latest version of PathfindingVisualizer from the Releases section of this repository. The release includes a standalone executable file that you can run on your system.

### Latest Release

Download the latest release of PathfindingVisualizer [here](https://github.com/Alipc598/PathfindingVisualizer/releases/latest).

### Requirements to Run the Executable

To run the PathfindingVisualizer executable, ensure you have the following installed on your system:

- **Windows Operating System**: The provided `.exe` file is compatible with Windows. If you're using a different OS, you'll need to run the application from the source code.

- **Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017, and 2019**: Some users might need to install this if it's not already present on their system. It can be downloaded from [Microsoft's official site](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads).

After downloading the executable, double-click on it to run the application. No additional installation is necessary.


## Installation

To run PathfindingVisualizer, you need Python and Kivy installed on your system. Follow these steps to set up the environment:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Alipc598/PathfindingVisualizer.git
   ```
   
2. **Install Dependencies**:
   Navigate to the cloned directory and install the required packages:
   ```bash
   pip install pyinstaller
   ```

3. **Run the Application**:
   ```bash
   python Pathfinding-Visualizer.py
   ```

## Usage

After launching PathfindingVisualizer, use the following steps to interact with the application:

1. **Select a Grid Layout**: Choose a pre-defined grid layout.
2. **Choose an Algorithm**: Select the algorithm you want to visualize from the dropdown menu.
3. **Run the Visualizer**: Click the 'Run' button to start the pathfinding process. The path, along with performance metrics, will be displayed.

## Contributing

Contributions to KivyPathfinder are welcome! If you have suggestions for improvement or want to contribute to the code, please feel free to create a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Kivy](https://kivy.org/) - The open-source Python library for developing multitouch applications.
---

© 2024 Ali Ghaedi. All Rights Reserved.
