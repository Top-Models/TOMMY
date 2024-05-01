# Writing unit tests with PyTest

_If the Tests can't be found then try the steps written in [How to run tests from PyCharm](How-to-run-tests-from-PyCharm)_

**Import the class that needs to be tested**

When wanting to test a class, it first needs to be imported into the test file. It is also useful to import pytest and Qt. The example import statements can be found in the figure below: 
```python
import pytest
from PySides6.QtCore import Qt
from interactive_topic_modeling.display.model_params_display import ModelParamsDisplay
```
 
**Initialize object to perform tests on**

Unit tests that will be performed (usually) make use of a fixture. If tests do not have to be run on the same object, fixtures are not strictly necessary. For this example, fixture code will be shown for both non-qt as well as qt objects. For the UI it is useful for all test to use the same instance of an object, and thus use a fixture. If you repeatedly have to create instances of the non-Qt object, fixtures can also be useful. A fixture an initial condition of a piece of code that will be tested. For example, if we want to test the model_parameter_display, we will first setup an initial parameter_display tagged as a fixture. This fixture will then be used in further unit tests. Fixtures would only have to written once for all tests for that object. For non-Qt objects, the fixture can be made like in the figure below, but to reiterate, with non frontend objects, this in not necessary as new instances can be made every test. If you don’t want to make a new instance every test, a fixture can be used.   
```python
@pytest.fixture
def gensim_lda_model():
    # Prepare sample term lists and other required parameters
    term_lists = [["word1", "word2", "word3"], ["word4", "word5", "word6"]l]
    num_topics = 2
    
    # Instantiate the model
    model = GensimLdaModel(term_lists, num_topics)
    
    return model 
```
Qt objects work a bit differently. When working with testing UI, we will most likely use bots to simulate the user interacting with the UI. The widget that we want to test needs to be linked to the bot. The widget also needs to be returned so it can be used in tests. An example of a Qt fixture is visible in the figure below:
```python
@pytest.fixture

def parameter_display(qtbot):
    # Create and return your parameter_display object here
    parameter_display = ModelParamsDisplay()
    # Attach the widget to the bot that will simulate the user
    qtbot.addWidget(parameter_display)
    return parameter_display
``` 

**Write unit tests**
 
Now that the objects have been made, they can be tested. The goal with a unit test is that one ‘unit’ of code is tested at a time. This could for example be the initialization of the object, the functionality of the object or the interaction of the object. Every test should be a ‘def’, where the parameter is the instance of the object that was made in the fixture. Some kind of assertion will be made in the test, determining if the code does what it has to do or not. An example of a unit test can be seen in the figure below:  
```python
def test_model_params_display_user_interaction(parameter_display, qtbot):
    # Set some kind of input
    parameter_display.topic_input.setText("10")
    # Have the user simulate the action of validating the input
    qtbot.keyPress(parameter_display.topic_input, Qt.Key_Return)
    # See if the result is the same as expected
    assert parameter_display.fetch_topic_num() == 10
```
These example tests can also be checked in the repository. The Qt test can be seen in example_test2. The non Qt test can be seen in example_test3