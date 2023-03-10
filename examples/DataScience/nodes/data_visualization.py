import pandas as pd
from PyQt5.QtWidgets import QPushButton, QWidget, QMessageBox, QCheckBox, QVBoxLayout, QGridLayout

from examples.DataScience.datascience_conf import register_node, OP_NODE_DATA_VISUALIZATION
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent

from nodeeditor.base_system_properties.utils_no_qt import dumpException

import matplotlib.pyplot as plt


class DataScienceGraphicalShow(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 300
        self.height = 150


class DataScienceShowContent(DataScienceContent):
    def createContentWidget(self):

        # Create checkbox widgets
        self.checkbox1 = QCheckBox("Plot Histogram", self)
        self.checkbox1.setStyleSheet("QCheckBox::indicator:checked {background-color: yellow;}")
        self.checkbox2 = QCheckBox("Plot Scatter", self)
        self.checkbox3 = QCheckBox("Plot Pie Chart", self)
        self.checkbox4 = QCheckBox("Plot Line", self)
        self.checkbox5 = QCheckBox("Plot Vertical bar", self)
        self.checkbox6 = QCheckBox("Plot Area", self)
        self.checkbox7 = QCheckBox("Plot Area", self)

        # Create grid layout
        layout = QGridLayout()
        layout.addWidget(self.checkbox1, 0, 0)
        layout.addWidget(self.checkbox2, 0, 1)
        layout.addWidget(self.checkbox3, 0, 2)
        layout.addWidget(self.checkbox4, 1, 0)
        layout.addWidget(self.checkbox5, 1, 1)
        layout.addWidget(self.checkbox6, 1, 2)
        layout.addWidget(self.checkbox7, 2, 0)

        # # Create button to retrieve selected checkboxes
        # btn = QPushButton("Get Selected Options", self)
        # btn.clicked.connect(self.get_selected_options)
        # layout.addWidget(btn, 2, 0, 1, 3)

        self.setLayout(layout)

    def get_selected_options(self):
        selected_options = []

        if self.checkbox1.isChecked():
            selected_options.append(self.checkbox1.text())
        if self.checkbox2.isChecked():
            selected_options.append(self.checkbox2.text())
        if self.checkbox3.isChecked():
            selected_options.append(self.checkbox3.text())
        if self.checkbox4.isChecked():
            selected_options.append(self.checkbox4.text())
        if self.checkbox5.isChecked():
            selected_options.append(self.checkbox5.text())
        if self.checkbox6.isChecked():
            selected_options.append(self.checkbox6.text())
        if self.checkbox7.isChecked():
            selected_options.append(self.checkbox7.text())

        return selected_options

@register_node(OP_NODE_DATA_VISUALIZATION)
class DataScienceNodeShow(DataScienceNode):
    icon = "icons/show.png"
    op_code = OP_NODE_DATA_VISUALIZATION
    op_title = "Visualization"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3], outputs=[])
        self.nodeEvaluation()

    def getInnerClasses(self):
        self.content = DataScienceShowContent(self)
        self.grNode = DataScienceGraphicalShow(self)

    def evaluationImplementation(self):
        super().evaluationImplementation()
        first_input = self.getInput(0)

        dataframe = pd.DataFrame(first_input.value)

        if first_input is None:
            self.markInvalid()
            self.grNode.setToolTip("Please connect all inputs")
            return None

        else:
            if dataframe.empty:
                self.grNode.setToolTip("Empty Data Frame")
                self.markInvalid(True)

                self.markDescendantsInvalid()
                self.markDescendantsReady(False)


            elif not self.content.get_selected_options():
                self.markReady()
                self.markInvalid(False)
                self.grNode.setToolTip("empty selection")

                self.markDescendantsInvalid(False)
                self.markDescendantsReady()


            elif self.content.get_selected_options():
                self.markReady(False)
                self.markInvalid(False)
                self.grNode.setToolTip("")

                chosen_box = self.content.get_selected_options()
                for value in chosen_box:
                    if value == self.content.checkbox1.text():
                        plt.hist(dataframe.columns, rwidth=0.8, color="Red")  # by default number of bins is set to 10
                        plt.show()
                        self.content.checkbox1.setChecked(False)
                        self.markReady()

                    elif value == self.content.checkbox2.text():
                        plt.scatter(dataframe.columns,dataframe.columns,edgecolors="Black")
                        plt.show()
                        self.content.checkbox2.setChecked(False)
                        self.markReady()

                self.markDescendantsInvalid(False)
                self.markDescendantsReady()

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        self.markReady()

        if finput_port is None:
            self.markReady()
