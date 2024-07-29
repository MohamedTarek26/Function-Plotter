# Function Plotter

A Python GUI application for plotting user-entered functions using PySide2 and Matplotlib. This application features input validation, dark mode, zooming, panning, and the ability to save plots. It also includes functionality to handle and display warnings about removed points to satisfy the domain of the function.

## Features

- **Plot Mathematical Functions**: Enter a function with variable `x` to be plotted.
- **Input Validation**: Ensures correct function syntax, valid `x` values, and appropriate step size.
- **Dark Mode**: Toggle between light and dark themes for better visibility.
- **Zooming**: Adjust the x and y axes dynamically.
- **Panning**: Explore different sections of the plot.
- **Save Plot**: Save the plot as an image file.
- **Warning Notifications**: Receive notifications about removed points necessary to fit the valid domain of the function.
- **Auto and Manual Step Size**: Choose between automatic and manual step size adjustment.

## Supported Operators

The following operators are supported:
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Exponentiation: `^`
- Logarithm base 10: `log10()`
- Square root: `sqrt()`

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/MohamedTarek26/function-plotter.git
    cd function-plotter
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```sh
    python function_plotter.py
    ```

2. **Enter Function Details**:
    - Provide a function, minimum and maximum `x` values, and step size.
    - Use the zoom sliders and panning feature to adjust the view.

3. **Plot the Function**:
    - Click "Plot" to visualize the function.
    - Zoom in/out on both x and y axes, and reset if needed.
    - Pan through the plot using the move button.

4. **Save the Plot**:
    - Click the "Save" button.
    - Choose the file format (e.g., PNG, JPG).
    - Select the location to save and click "Save."

5. **Light/Dark Modes**:
    - **Dark Mode**: Toggle to dark mode for low-light environments and reduced eye strain.
    - **Light Mode**: Switch back to light mode for bright environments.

## Demo GIFs

### General Demo with Valid Cases

Watch the GIF for a demonstration of the Function Plotter handling valid cases:

![General Demo](media/allok.gif)

### Wrong Cases

Watch the GIF to see how the Function Plotter handles incorrect inputs:

![Wrong Cases](media/allwrong.gif)

### Warning Cases

Watch the GIF to see how the application displays warnings when points are removed to fit the domain:

![Warning Cases](media/allwarning.gif)

### Dark Mode, Zoom, and Panning

Explore the Function Plotter's dark mode, zoom sliders, and panning features in this GIF:

![Dark Mode and Zoom](media/zoom_dark.gif)

### Saving Plots

Watch the GIF to see how the Function Plotter allows saving plots:

![Saving Plots](media/save.gif)

## Tests

To run automated tests, use pytest:
```sh
pytest
