import pytest

from raising_widget import RaisingWidget
from qtpy.QtCore import Qt

@pytest.fixture
def widget(qtbot):
    "depend on qtbot to start Qt event loop"
    return RaisingWidget()

# works as expected, but is not inside qt event loop
def test_raising_callback(widget):
    with pytest.raises(AssertionError):
        widget._on_button_pressed()

# using qtbot.capture_exceptions is the way to do it!  
def test_raising_widget_capture_exceptions(qtbot, widget):
    with qtbot.capture_exceptions() as exceptions:
        qtbot.mouseClick(widget.raise_button, Qt.LeftButton)
    # exception is a list of sys.exc_info tuples
    assert len(exceptions) == 1
    _, exception, collected_traceback = exceptions[0] # ignore type and traceback
    assert isinstance(exception, AssertionError)
    assert "_on_button_pressed" in traceback.format_tb(collected_traceback)[0]

# attempts below were naive, and fail, so marking with XFAIL

# assertion error raised in Qt event loop, and therefore not caught by pytest.raises
@pytest.mark.xfail
def testing_raising_mouseclick(widget, qtbot): 
    with pytest.raises(AssertionError):
        qtbot.mouseClick(widget.raise_button, Qt.LeftButton)

# try to manually re-raise any error to test it is an assertion error as expected
# fails the same way
@pytest.mark.xfail
def testing_raising_mouseclick_try_except(widget, qtbot): 
    with pytest.raises(AssertionError):
        try:
            qtbot.mouseClick(widget.raise_button, Qt.LeftButton)
        except Exception as e:
            raise e

# use a custom excepthook - doesn't work for me 
import sys
import traceback

@pytest.fixture
def patch_qt_excepthook(qtbot):
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
        qtbot.quit() # re-raise exception after quitting event loop
        raise exc_type(exc_value)
    actual_excepthook = sys.excepthook
    sys.excepthook = excepthook
    yield
    sys.excepthook = actual_excepthook

@pytest.mark.xfail
def testing_raising_mouseclick_try_except_outside_loop(widget, qtbot, patch_qt_excepthook):
    with pytest.raises(AssertionError):
        qtbot.mouseClick(widget.raise_button, Qt.LeftButton)


