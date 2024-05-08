# New algorithm settings

When a new topic modelling algorithm is added to the software, new parameters should be added to the Settings view. The AbstractSettings class already provides a template of the settings, as specified in the `initialize_parameter_widgets` function, where the k-value and amount of topic words to be displayed are rendered.

```python
    def initialize_parameter_widgets(self, scroll_layout: QVBoxLayout) -> None:
        """
        Initialize the parameter widgets
        This method should be overridden by the child class
        to add the model specific widgets to the view

        :return: None
        """
        self._scroll_layout = scroll_layout
        self.add_header_label("Algemeen", 17)
        self.initialize_topic_amount_field()
        self.initialize_amount_of_words_field()
        self.add_margin(10)
``` 

## Re-implement `initialize_parameter_widgets`

When creating settings for a new topic modelling algorithm, a new class should be added within the _abstract_settings_ folder, which should inherit from the AbstractSettings class. New controls for model-specific settings should be added within this class, as well as the linked event handlers. A **strict requirement** is that the child class should re-implement the `initialize_parameter_widgets`. The re-implementation should call the method's version from the base class, and add rendering of the new model-specific widgets. For example, the LdaSettings class has the following re-implementation of the `initialize_parameter_widgets` function. 

```python
    def initialize_parameter_widgets(self,
                                     scroll_layout: QVBoxLayout) -> None:
        """
        Initialize the parameter widgets

        :return: None
        """
        super().initialize_parameter_widgets(scroll_layout)
        self.add_header_label("Hyperparameters", 17)
        self.initialize_alpha_field()
        self.initialize_beta_field()
        self.initialize_auto_calculate_alpha_beta_checkbox()
        self.add_margin(10)
```

## Styling options

As is visible in the implementation of `initialize_parameter_widgets` above, styling functions can be used for creating separate sections of parameters within the Settings view. Currently, the software supports the following styling methods:

- `add_margin(self, height: int) -> None`: Add a margin to the settings view
- `add_header_label(self, header_text: str, size: int) -> None`: Add a header label to the settings view