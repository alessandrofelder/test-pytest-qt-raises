
from qtpy.QtWidgets import QWidget, QPushButton, QVBoxLayout

class RaisingWidget(QWidget):
	def __init__(self, parent: QWidget=None):
		super().__init__(parent)
		self.setLayout(QVBoxLayout())
		self.raise_button = QPushButton()
		self.raise_button.clicked.connect(self._on_button_pressed)
		self.raise_button.setText("I will raise if you press me")
		self.layout().addWidget(self.raise_button)

	def _on_button_pressed(self):
		assert -3 > 0 # fail on purpose


