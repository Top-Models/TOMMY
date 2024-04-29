import pytest

from tommy.support.event_handler import EventHandler


class FunctionHolder:
    """Holds functions and tracks called functions for use in tests"""
    def __init__(self):
        self.functions_called = []

    def func_str(self, event_arg: str) -> None:
        self.functions_called.append((self.func_str, event_arg))

    def func_int(self, event_arg: int) -> None:
        self.functions_called.append((self.func_int, event_arg))

    def func_tuple(self, event_arg: tuple[str, int]) -> None:
        self.functions_called.append((self.func_tuple, event_arg))

    def func_tuple2(self, event_arg: tuple[str, int]) -> None:
        self.functions_called.append((self.func_tuple2, event_arg))

    def func_tuple3(self, event_arg: tuple[str, int]) -> None:
        self.functions_called.append((self.func_tuple3, event_arg))


fh = FunctionHolder()
@pytest.mark.parametrize("event_handler,functions_to_add,expected_functions", [
    (EventHandler[str](), [], []),
    (EventHandler[int](), [fh.func_int], [fh.func_int]),
    (EventHandler[tuple[str, int]](), [fh.func_tuple, fh.func_tuple],
     [fh.func_tuple, fh.func_tuple])
])
def test_subscribe(event_handler: EventHandler,
                   functions_to_add: list,
                   expected_functions: list):
    """Test adding functions/listeners to the eventhandler"""
    for func in functions_to_add:
        event_handler.subscribe(func)

    assert event_handler.subscribers == expected_functions


@pytest.mark.parametrize("event_handler,"
                         "functions_to_add,"
                         "functions_to_remove,"
                         "expected_functions",
                         [
    (EventHandler[str](), [], [], []),
    (EventHandler[int](), [fh.func_int], [], [fh.func_int]),
    (EventHandler[int](), [fh.func_int], [fh.func_int], []),
    (EventHandler[tuple[str, int]](), [fh.func_tuple, fh.func_tuple], [],
        [fh.func_tuple, fh.func_tuple])
])
def test_unsubscribe(event_handler: EventHandler,
                     functions_to_add: list,
                     functions_to_remove: list,
                     expected_functions: list):
    """Test removing functions/listeners from to the eventhandler"""
    for func in functions_to_add:
        event_handler.subscribe(func)

    for func in functions_to_remove:
        event_handler.unsubscribe(func)

    for func in expected_functions:
        assert func in event_handler.subscribers


fh0 = FunctionHolder()
fh1 = FunctionHolder()
fh2 = FunctionHolder()
fh3 = FunctionHolder()
@pytest.mark.parametrize("event_handler,"
                         "function_holder,"
                         "functions_to_add,"
                         "functions_to_remove,"
                         "function_call_args,"
                         "expected_functions_called",
                         [
    (EventHandler[str](), fh0, [], [], [], []),
    (EventHandler[int](), fh1, [fh1.func_int, fh1.func_int], [fh1.func_int],
        [69, 70], [(fh1.func_int, 69), (fh1.func_int, 70)]),
    (EventHandler[int](), fh2, [fh2.func_int], [fh2.func_int, fh2.func_int], [],
        []),
    (EventHandler[tuple[str, int]](), fh3,
        [fh3.func_tuple2, fh3.func_tuple, fh3.func_tuple3], [fh3.func_tuple2],
        [("call1", 1), ("call3", 3)],
        [(fh3.func_tuple, ("call1", 1)), (fh3.func_tuple3, ("call1", 1)),
         (fh3.func_tuple, ("call3", 3)), (fh3.func_tuple3, ("call3", 3))])
])
def test_publish(event_handler: EventHandler,
                 function_holder: FunctionHolder,
                 functions_to_add: list,
                 functions_to_remove: list,
                 function_call_args: list[tuple[str, int]],
                 expected_functions_called: list):
    """Test triggering the eventhandler"""
    for func in functions_to_add:
        event_handler.subscribe(func)

    for func in functions_to_remove:
        event_handler.unsubscribe(func)

    for arg in function_call_args:
        event_handler.publish(arg)

    assert function_holder.functions_called == expected_functions_called


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
