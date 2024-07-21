import sys
import logging
from PySide2.QtWidgets import QApplication
from function_plotter import FunctionPlotter

# Configure logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    logging.debug("Starting application")
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    sys.exit(app.exec_())
