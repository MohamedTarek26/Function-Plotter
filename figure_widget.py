from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

class FigureWidget(QWidget):
    """Figure widget used by different views

    Parameters
    ----------
    parent : Qt parent
       Qt parent object
    canvas : FigureCanvas
       the figure canvas class
    exclude_toolbar_items : tuple
       elements to exclude from the toolbar
    """
    def __init__(self, parent=None, canvas=None, exclude_toolbar_items=()):
        super().__init__(parent)

        self.canvas = canvas
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)

        if isinstance(canvas, FigureCanvas):
            # Define a custom NavigationToolbar excluding specific items
            class _SimpleNavigationToolbar(NavigationToolbar):
                toolitems = [t for t in NavigationToolbar.toolitems if
                             t[0] not in exclude_toolbar_items]
            self.toolbar = _SimpleNavigationToolbar(self.canvas, self.canvas)

            self.layout.addWidget(self.toolbar)
        else:
            self.toolbar = None

        self.setLayout(self.layout)
