import logging
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox
from PySide2.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from functools import partial
from checker import Checker
from figure_widget import FigureWidget

class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.debug("Initializing FunctionPlotter")

        self.min_x = -10
        self.max_x = 10
        self.min_y = -10
        self.max_y = 10
        self.initial_min_x = self.min_x  # Store initial values
        self.initial_max_x = self.max_x  # Store initial values
        self.step_size = 0.1
        self.func = ""
        self.zoom_x = 1.0
        self.zoom_y = 1.0
        self.is_testing_bot = False
        
        self.checker = Checker()
        self.msg_box = None  # Variable to store QMessageBox instance

        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Main widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Layout
        layout = QVBoxLayout(self.main_widget)

        # Function input
        function_layout = QHBoxLayout()
        self.function_label = QLabel("f(x):")
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("e.g., 5*x^3 + 2*x")
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        function_layout.addWidget(self.function_label)
        function_layout.addWidget(self.function_input)
        function_layout.addWidget(self.dark_mode_checkbox)
        layout.addLayout(function_layout)

        # Min and Max x inputs (Horizontal layout)
        min_max_layout = QHBoxLayout()
        self.min_label = QLabel("min value of x:")
        self.min_input = QLineEdit()
        min_max_layout.addWidget(self.min_label)
        min_max_layout.addWidget(self.min_input)

        self.max_label = QLabel("max value of x:")
        self.max_input = QLineEdit()
        min_max_layout.addWidget(self.max_label)
        min_max_layout.addWidget(self.max_input)

        layout.addLayout(min_max_layout)

        # Step size and checkbox (Horizontal layout)
        step_layout = QHBoxLayout()
        self.auto_step_checkbox = QCheckBox("Auto Step Size")
        self.auto_step_checkbox.setChecked(True)  # Default to auto step size
        self.step_label = QLabel("Step Size:")
        self.step_input = QLineEdit()
        step_layout.addWidget(self.auto_step_checkbox)
        step_layout.addWidget(self.step_label)
        step_layout.addWidget(self.step_input)

        layout.addLayout(step_layout)

        # Plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(partial(self.plot_function, new=True))
        layout.addWidget(self.plot_button)

        # Matplotlib Figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Create the custom FigureWidget with toolbar
        #remove the Zoom and Subplots and the button next to it
        figure_widget = FigureWidget(self, self.canvas, exclude_toolbar_items=("Zoom","Customize"))
        layout.addWidget(figure_widget)

        # Zoom buttons layout
        zoom_layout = QHBoxLayout()

        # Zoom in and out buttons for x-axis
        self.zoom_in_x_button = QPushButton("Zoom In X")
        self.zoom_out_x_button = QPushButton("Zoom Out X")
        self.zoom_in_x_button.clicked.connect(partial(self.update_zoom, 'x', 1.2))
        self.zoom_out_x_button.clicked.connect(partial(self.update_zoom, 'x', 0.8))
        zoom_layout.addWidget(self.zoom_in_x_button)
        zoom_layout.addWidget(self.zoom_out_x_button)

        # Zoom in and out buttons for y-axis
        self.zoom_in_y_button = QPushButton("Zoom In Y")
        self.zoom_out_y_button = QPushButton("Zoom Out Y")
        self.zoom_in_y_button.clicked.connect(partial(self.update_zoom, 'y', 1.2))
        self.zoom_out_y_button.clicked.connect(partial(self.update_zoom, 'y', 0.8))
        zoom_layout.addWidget(self.zoom_in_y_button)
        zoom_layout.addWidget(self.zoom_out_y_button)

        # Reset zoom button
        self.reset_zoom_button = QPushButton("Reset Zoom")
        self.reset_zoom_button.clicked.connect(self.reset_zoom)
        zoom_layout.addWidget(self.reset_zoom_button)

        layout.addLayout(zoom_layout)

        self.load_stylesheet('light_mode.qss')  # Load default stylesheet
        self.show()
        logging.debug("FunctionPlotter initialized and shown")

    def load_stylesheet(self, filename):
        """Load a stylesheet from a file."""
        with open(filename, 'r') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

    def toggle_dark_mode(self, state):
        if state == Qt.Checked:
            # Apply dark mode stylesheet
            self.load_stylesheet('dark_mode.qss')
            self.figure.patch.set_facecolor('#333')  # Set figure background color
        else:
            # Apply light mode stylesheet
            self.load_stylesheet('light_mode.qss')
            self.figure.patch.set_facecolor('white')  # Set figure background color

        # Redraw canvas after setting background color
        self.plot_function(new=False)
        self.canvas.draw()

    def plot_function(self, new=True):
        self.msg_box = None  # Reset message box
        
        if new:
            self.func = self.function_input.text()
            self.min_x = self.min_input.text()
            self.max_x = self.max_input.text()
        logging.debug(f"Plotting function: {self.func}")
        if new:
        # Validate the function expression
            validation_result, validation_message = self.checker.validate_function(self.func)
            if not validation_result:
                if new:
                    self.msg_box = QMessageBox(self)
                    self.msg_box.setIcon(QMessageBox.Critical)
                    self.msg_box.setText(f"Function validation error: {validation_message}")
                    self.msg_box.setWindowTitle("Function Error")
                    if not self.is_testing_bot:
                        self.msg_box.exec_()
                logging.error(f"Function validation error: {validation_message}")
                #clear the plot
                self.figure.clear()
                return

        self.func = self.func.replace(" ", "")  # Remove spaces for easier processing
        self.func = self.func.replace("^", "**") # Replace ^ with ** for power
        try:
            # Validate min_x and max_x
            self.min_x = float(self.min_x)
            self.max_x = float(self.max_x)
            if self.min_x >= self.max_x:
                raise ValueError("min_x should be less than max_x")
        except ValueError as e:
            if new:
                self.msg_box = QMessageBox(self)
                self.msg_box.setIcon(QMessageBox.Critical)
                self.msg_box.setText(f"Invalid min or max x values: {e}")
                self.msg_box.setWindowTitle("Input Error")
                if not self.is_testing_bot:
                    self.msg_box.exec_()
            logging.error(f"Invalid min or max x values: {e}")
            return

        # Determine step size
        if self.auto_step_checkbox.isChecked():
            self.step_size = (self.max_x - self.min_x) / 400  # Auto calculate step size
        else:
            if new:
                self.step_size = self.step_input.text()

        try:
            self.step_size = float(self.step_size)
        except ValueError as e:
            if new:
                self.msg_box = QMessageBox(self)
                self.msg_box.setIcon(QMessageBox.Critical)
                self.msg_box.setText(f"Invalid step size: {e}")
                self.msg_box.setWindowTitle("Input Error")
                if not self.is_testing_bot:
                    self.msg_box.exec_()
            logging.error(f"Invalid step size: {e}")
            return

        # Generate x values
        x = np.arange(self.min_x, self.max_x, self.step_size)
        initial_x_len = len(x)

        # Evaluate function and filter out infinite, NaN, or problematic values
        try:
            y = np.array([eval(self.func, {"x": xi, "np": np, "log10": np.log10, "sqrt": np.sqrt}) for xi in x])
            
            # Remove points where y is infinite, NaN, or has division by zero errors
            finite_mask = np.isfinite(y) & (y != np.inf) & (y != -np.inf)
            x = x[finite_mask]
            y = y[finite_mask]

            removed_points = initial_x_len - len(x)
            if removed_points > 0:
                if new:
                    self.msg_box = QMessageBox(self)
                    self.msg_box.setIcon(QMessageBox.Warning)
                    self.msg_box.setText(f"Warning: {removed_points} points were removed due to invalid values.")
                    self.msg_box.setWindowTitle("Warning")
                    if not self.is_testing_bot:
                        self.msg_box.exec_()
                logging.warning(f"Warning: {removed_points} points were removed due to invalid values.")
            
            if len(x) == 0:  # Check if x is empty
                if new:
                    self.msg_box = QMessageBox(self)
                    self.msg_box.setIcon(QMessageBox.Warning)
                    self.msg_box.setText("No valid points to plot.")
                    self.msg_box.setWindowTitle("Warning")
                    if not self.is_testing_bot:
                        self.msg_box.exec_()
                logging.warning("No valid points to plot.")
                return
        
            self.min_x = min(x)
            self.max_x = max(x)
            self.min_y = min(y)
            self.max_y = max(y)

        except ZeroDivisionError as e:
            if new:
                self.msg_box = QMessageBox(self)
                self.msg_box.setIcon(QMessageBox.Critical)
                self.msg_box.setText(f"Division by zero error in function: {e}")
                self.msg_box.setWindowTitle("Math Error")
                if not self.is_testing_bot:
                    self.msg_box.exec_()
            logging.error(f"Division by zero error in function: {e}")
            return
        except Exception as e:
            if new:
                self.msg_box = QMessageBox(self)
                self.msg_box.setIcon(QMessageBox.Critical)
                self.msg_box.setText(f"Error in function: {e}")
                self.msg_box.setWindowTitle("Function Error")
                if not self.is_testing_bot:
                    self.msg_box.exec_()
            logging.error(f"Error in function: {e}")
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title(f"Plot of {self.func}")

        # Apply dark mode styles if enabled
        if self.dark_mode_checkbox.isChecked():
            ax.set_facecolor('#333')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.title.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
        else:
            ax.set_facecolor('white')
            ax.tick_params(colors='black')
            ax.spines['bottom'].set_color('black')
            ax.spines['top'].set_color('black')
            ax.spines['right'].set_color('black')
            ax.spines['left'].set_color('black')
            ax.title.set_color('black')
            ax.xaxis.label.set_color('black')
            ax.yaxis.label.set_color('black')
        
        if len(y) > 0:
            self.min_y = min(y)
            self.max_y = max(y)
        
        # Apply zoom
        self.apply_zoom()

        self.canvas.draw()
        logging.debug("Function plotted")


    def update_zoom(self, axis, factor):
        if axis == 'x':
            self.zoom_x *= factor
        elif axis == 'y':
            self.zoom_y *= factor
        self.apply_zoom()
        logging.debug(f"Zoom {axis} updated to {self.zoom_x if axis == 'x' else self.zoom_y}")

    def reset_zoom(self):
        self.zoom_x = 1.0
        self.zoom_y = 1.0
        self.apply_zoom(reset=True)
        logging.debug("Zoom reset")

    def apply_zoom(self, reset=False):
        ax = self.figure.gca()
        if reset:
            ax.set_xlim(self.min_x, self.max_x)
            ax.set_ylim(auto=True)
        else:
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()

            x_center = (self.max_x + self.min_x) / 2
            y_center = (self.max_y + self.min_y) / 2

            x_range = (self.max_x - self.min_x) / self.zoom_x
            y_range = (self.max_y - self.min_y) / self.zoom_y

            ax.set_xlim(x_center - x_range / 2, x_center + x_range / 2)
            ax.set_ylim(y_center - y_range / 2, y_center + y_range / 2)

        self.canvas.draw()
