import pytest

from raising_widget import RaisingWidget
from qtpy.QtCore import Qt

@pytest.fixture
def widget(qtbot):
    "depend on qtbot to start Qt event loop"
    return RaisingWidget()

def test_raising_callback(widget):
    with pytest.raises(AssertionError):
        widget._on_button_pressed()

def testing_raising_mouseclick(widget, qtbot): 
    with pytest.raises(AssertionError):
        qtbot.mouseClick(widget.raise_button, Qt.LeftButton)