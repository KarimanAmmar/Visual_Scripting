import pandas as pd
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QImage, QFont, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QLineEdit

from examples.DataScience.datascience_conf import register_node, OP_NODE_CALC_STD
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent


class DataScienceGraphicalCalcStd(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 250
        self.height = 100
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10


class DataScienceCalcStdContent(DataScienceContent):

    def createContentWidget(self):
        self.lbl = QLabel("Choose A Column: ", self)
        self.lbl.move(35, 10)
        self.lbl.setStyleSheet("font: bold 13px;")

        self.combobox = QComboBox(self)
        self.combobox.move(30, 35)
        self.combobox.resize(150, 28)
        self.combobox.setStyleSheet("background-color: #5885AF;"
                                    "border-radius: 10px;"
                                    "font: bold 14px;"
                                    "padding: 6px;")

        self.combobox.currentIndexChanged.connect(self.know_the_change)

    def get_combobox_changed_text(self):
        selected = self.combobox.currentText()
        return selected

    def know_the_change(self, index):
        old_item = self.combobox.itemText(index - 1) if index > 0 else self.combobox.itemText(0)
        new_item = self.combobox.currentText()

        if old_item == new_item:
            return False
        else:
            return True


@register_node(OP_NODE_CALC_STD)
class DataScienceNodeCalcMean(DataScienceNode):
    icon = "icons/calculator.png"
    op_code = OP_NODE_CALC_STD
    op_title = "Calculating StandardDeviation"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def getInnerClasses(self):
        self.content = DataScienceCalcStdContent(self)
        self.grNode = DataScienceGraphicalCalcStd(self)

    def evaluationImplementation(self):
        super().evaluationImplementation()
        first_input = self.getInput(0)

        if first_input is None:
            self.markInvalid()
            self.grNode.setToolTip("Please connect all inputs")
            return None

        else:
            val = self.evaluationOperation(first_input.nodeEvaluation())
            self.value = val

            if first_input is None:
                self.markInvalid()
                self.grNode.setToolTip("Please connect all inputs")
                return None

            else:
                val = self.evaluationOperation(first_input.nodeEvaluation())
                self.value = val

                if self.content.know_the_change(self.content.combobox.currentIndex()):
                    self.markReady(False)
                    self.markInvalid(False)
                    self.grNode.setToolTip("QQQQQQ")

                    self.markDescendantsInvalid(False)
                    self.markDescendantsReady()

                    return self.value

                elif not self.content.know_the_change(self.content.combobox.currentIndex()):

                    self.markReady(False)
                    self.markInvalid(False)
                    self.grNode.setToolTip("SSSSSSS")

                    self.markDescendantsInvalid(False)
                    self.markDescendantsReady()

                    return self.value

                return self.value

    def evaluationOperation(self, input1, **kwargs):

        dataframe = pd.DataFrame(input1)

        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

        newDataFrame = dataframe.select_dtypes(include=numerics)

        self.col_names = list(newDataFrame.columns)

        if self.content.combobox.count() == 0:
            self.content.combobox.addItems(self.col_names)
        else:
            pass

        selected_item = self.content.get_combobox_changed_text()
        column_std = newDataFrame[selected_item].std()
        self.content.combobox.currentTextChanged.connect(self.onStatuesChange)
        return column_std

    def onStatuesChange(self):
        self.markReady()

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        self.content.combobox.clear()
        self.markReady()

        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port is None:
            self.markInvalid()
            self.grNode.setToolTip("Connect input with dataframe")


        elif finput_port and foutput_port is None:
            self.markReady()
