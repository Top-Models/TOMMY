import os.path

import matplotlib.figure
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import numpy as np

from tommy.controller.result_interfaces.correlation_matrix_interface import (
    CorrelationMatrixInterface)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, ProcessedCorpus)

from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)


class WelcomeScreen(AbstractVisualization):
    """
    A class for constructing a welcome screen for the user.
    """
    _required_interfaces = []
    name = 'Welkom bij TOMMY'
    short_tab_name = 'Welkom'
    vis_group = VisGroup.CORPUS  # Irrelevant, as this can only be seen when
    # it's alone.
    needed_input_data = []

    def _create_figure(self, **kwargs) -> matplotlib.figure.Figure:
        """
        Constructs a welcome screen for the user.
        """

        # Import the image
        image_path = os.path.abspath('../assets/tommy_welcome_screen.png')
        image = plt.imread(image_path)

        # Create the figure
        fig, ax = plt.subplots()
        ax.imshow(image)
        ax.axis('off')
        fig.tight_layout()
        return fig

    def is_possible(self, metadata_available: bool,
                    topic_runner: TopicRunner) -> bool:
        return not bool(metadata_available)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
