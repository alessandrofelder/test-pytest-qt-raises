# test-pytest-qt-raises

Documenting my experiments to understand how to write negative tests for errors raised inside Qt event loop.

The key code snippet of the solution is sketched out below
```python
# using qtbot.capture_exceptions is the way to do it!  
def test_raising_widget_capture_exceptions(qtbot, widget):
    with qtbot.capture_exceptions() as exceptions:
        qtbot.mouseClick(widget.raise_button, Qt.LeftButton)
    # exception is a list of sys.exc_info tuples
    assert len(exceptions) == 1
    _, exception, collected_traceback = exceptions[0] # ignore type
    assert isinstance(exception, AssertionError)
    assert "_on_button_pressed" in traceback.format_tb(collected_traceback)[0] # the function name that is expected to raise
```
