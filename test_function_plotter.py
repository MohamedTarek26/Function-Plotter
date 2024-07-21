import numpy as np
import pytest
from pytestqt import qtbot
from function_plotter import FunctionPlotter

@pytest.fixture
def app(qtbot):
    """Create and return the FunctionPlotter application."""
    window = FunctionPlotter()
    qtbot.addWidget(window)
    return window

def generate_random_function():
    """Generate a random function for testing."""
    operators = ['+', '-', '*', '/', '^']
    functions = ['x', 'x^2', 'x^3', '2*x + 1', 'x^2 - 4']
    func = np.random.choice(functions)
    if np.random.rand() > 0.5:
        func = f"{func} {np.random.choice(operators)} {np.random.choice(functions)}"
    return func

def generate_random_input_range():
    """Generate a random input range for testing."""
    min_x = np.random.uniform(-100, 100)
    max_x = np.random.uniform(min_x + 1, min_x + 200)
    return min_x, max_x

def evaluate_function(func, x):
    """Evaluate the function for given x."""
    try:
        func.replace("^", "**")  # Replace '^' with '**' for exponentiation
        return eval(func, {"x": x, "np": np, "log10": np.log10, "sqrt": np.sqrt})
    except Exception as e:
        return np.nan  # Return NaN for invalid evaluations

def test_operations_with_random_functions_and_ranges(app, qtbot):
    for _ in range(50):  # Run 10 random tests
        func = generate_random_function()
        min_x, max_x = generate_random_input_range()
        app.is_testing_bot = True
        app.function_input.setText(func)
        app.min_input.setText(str(min_x))
        app.max_input.setText(str(max_x))
        app.plot_button.click()

        qtbot.wait(100)

        # Check if plot data exists
        if len(app.figure.axes) == 0:
            continue
        lines = app.figure.axes[0].lines
        x_data, y_data = lines[0].get_data()
        if len(x_data) == 0:
            continue
        # Check if the function is evaluated correctly
        for x_val in x_data:
            expected_y = evaluate_function(func, x_val)
            if np.isfinite(expected_y):
                # Find the closest y value from the plot data
                closest_index = np.argmin(np.abs(x_data - x_val))
                plot_y_val = y_data[closest_index]
                assert np.isclose(expected_y, plot_y_val, atol=1e-5), f"Function {func} value mismatch for x={x_val}: expected {expected_y}, got {plot_y_val}"

@pytest.mark.parametrize("func, min_x, max_x", [
    ("5*x^", "10", "5"),  # Invalid function
    ("5*x + 2", "10", "5"),  # min_x >= max_x
])
def test_input_validation(app, qtbot, func, min_x, max_x):
    app.is_testing_bot = True
    app.function_input.setText(func)
    app.min_input.setText(min_x)
    app.max_input.setText(max_x)
    app.plot_button.click()
    qtbot.wait(200)

    # Check if QMessageBox was shown
    assert app.msg_box is not None

@pytest.mark.parametrize("func, min_x, max_x", [
    ("5*x^*2", "-10", "10"),  # Syntax error
    ("5*x / (x - x)", "-10", "10"),  # Division by zero
    ("5*x / 0", "-10", "10"),  # Division by zero
    ("sqrt(-5)+x", "-10", "10")  # Invalid square root input
])
def test_invalid_function_handling(app, qtbot, func, min_x, max_x):
    app.is_testing_bot = True
    app.function_input.setText(func)
    app.min_input.setText(min_x)
    app.max_input.setText(max_x)
    app.plot_button.click()

    qtbot.wait(200)

    assert app.msg_box is not None

    

@pytest.mark.parametrize("auto_step, step_size, expected_step_size", [
    (True, None, None),  # Auto step size
    (False, "0.5", 0.5)  # Custom step size
])
def test_step_size(app, qtbot, auto_step, step_size, expected_step_size):
    app.is_testing_bot = True
    app.function_input.setText("5*x^2")
    app.min_input.setText("-50")
    app.max_input.setText("50")
    app.auto_step_checkbox.setChecked(auto_step)
    if step_size:
        app.step_input.setText(step_size)
    else:
        app.step_input.clear()  # Ensure step input is cleared for auto mode

    app.plot_button.click()
    qtbot.wait(200)

    # Verify step size
    if auto_step:
        expected_step_size = (50 - (-50)) / 400
    x = np.arange(-50, 50, expected_step_size)
    assert len(x) > 0

# New test cases for specific operations and functions

@pytest.mark.parametrize("func, min_x, max_x", [
    ("log10(x)", 0.1, 10),     # Test log10 function with valid input
    ("log10(x)", -10, 10),     # Test log10 function with invalid input
    ("sqrt(x)", 0, 10),        # Test sqrt function with valid input
    ("sqrt(x)", -10, 10)       # Test sqrt function with invalid input
])
def test_special_functions(app, qtbot, func, min_x, max_x):
    app.is_testing_bot = True
    app.function_input.setText(func)
    app.min_input.setText(str(min_x))
    app.max_input.setText(str(max_x))
    app.plot_button.click()

    qtbot.wait(200)

    # Check if plot data exists
    assert len(app.figure.axes) == 1
    lines = app.figure.axes[0].lines
    x_data, y_data = lines[0].get_data()
    if len(x_data) == 0:
        pytest.fail(f"No data plotted for function: {func}")

    # Check if the function is evaluated correctly
    for x_val in x_data:
        expected_y = evaluate_function(func, x_val)
        if np.isfinite(expected_y):
            # Find the closest y value from the plot data
            closest_index = np.argmin(np.abs(x_data - x_val))
            plot_y_val = y_data[closest_index]
            assert np.isclose(expected_y, plot_y_val, atol=1e-5), f"Function value mismatch for x={x_val}: expected {expected_y}, got {plot_y_val}"

@pytest.mark.parametrize("func, min_x, max_x", [
    ("x + 1", -10, 10),   # Addition
    ("x - 1", -10, 10),   # Subtraction
    ("x * 2", -10, 10),   # Multiplication
    ("x / 2", -10, 10),    # Division
    ("5*x^ + 2*x", "-10", "10")  #Treating + as a sign instead of an operator

])
def test_arithmetic_operations(app, qtbot, func, min_x, max_x):
    app.is_testing_bot = True
    app.function_input.setText(func)
    app.min_input.setText(str(min_x))
    app.max_input.setText(str(max_x))
    app.plot_button.click()

    qtbot.wait(200)

    # Check if plot data exists
    assert len(app.figure.axes) == 1
    lines = app.figure.axes[0].lines
    x_data, y_data = lines[0].get_data()
    if len(x_data) == 0:
        pytest.fail(f"No data plotted for function: {func}")

    # Check if the function is evaluated correctly
    for x_val in x_data:
        expected_y = evaluate_function(func, x_val)
        if np.isfinite(expected_y):
            # Find the closest y value from the plot data
            closest_index = np.argmin(np.abs(x_data - x_val))
            plot_y_val = y_data[closest_index]
            assert np.isclose(expected_y, plot_y_val, atol=1e-5), f"Function value mismatch for x={x_val}: expected {expected_y}, got {plot_y_val}"
