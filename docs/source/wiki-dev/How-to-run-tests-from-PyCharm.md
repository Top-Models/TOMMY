# How to run tests from PyCharm


## Creating a configuration
To run the tests from PyCharm, a new configuration needs to be created. This is done in the following way:
- In the bar at the top, press the current configuration next to the `Run` button to open a drop-down
- Select `Edit Configurations...`
- In the topright, press the `+` button (the text `Add New Configuration` appears when hovering over the button)
- Scroll down until you find the tab called `Python tests` and select `pytest` under that tab
- For `Script path`, select the `test` folder
- For `Working directory`, select the `tommy` folder
- Select the correct python interpreter (make sure it is python 3.12 and that it is in your virtual environment)
- (Optionally) give the configuration a name
- Press `OK`

## Running the tests
Once the configuration is configured (pun not intended), simply select it from the dropdown next to the run button. Now press the run button and the test results should appear at the bottom of your screen.