import pandas as pd
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QImage, QFont, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QLineEdit

from examples.DataScience.datascience_conf import register_node, OP_NODE_PRINT_OUTPUT
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent


class DataScienceGraphicalCalcMean(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 210
        self.height = 100
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10


class DataScienceCalcMeanContent(DataScienceContent):

    def createContentWidget(self):
        self.lbl = QLabel(self)
        self.lbl.move(30, 10)
        self.lbl.setStyleSheet("font: bold 13px;")


@register_node(OP_NODE_PRINT_OUTPUT)
class DataScienceNodeCalcMean(DataScienceNode):
    # icon = "icons/rename.png"
    op_code = OP_NODE_PRINT_OUTPUT
    op_title = "Showing Output"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def getInnerClasses(self):
        self.content = DataScienceCalcMeanContent(self)
        self.grNode = DataScienceGraphicalCalcMean(self)


    def evaluationImplementation(self):

        input_socket = self.getInput(0)

        if input_socket is None:
            self.markReady()
            self.grNode.setToolTip("Input is not connected")
            return

        val = input_socket.nodeEvaluation()


        # elif input_socket.value.empty:
        #     self.markInvalid()
        #     self.grNode.setToolTip("No Output to be shown")
        #
        #     self.markDescendantsInvalid()
        #     self.markDescendantsReady(False)
        #
        #     return

        if val is None:
            self.grNode.setToolTip("Input is NaN")

            self.markInvalid()

            return

        elif val:
            self.content.lbl.setText(val)
            self.content.lbl.adjustSize()
            self.markInvalid(False)

            self.markReady(False)

            self.grNode.setToolTip("")

        # if int(val):
        #
        #     self.content.lbl.setText(f"{val}")
        #
        #     self.markInvalid(False)
        #
        #     self.markReady(False)
        #
        #     self.grNode.setToolTip("")
        #
        #
        # elif not int(val):
        #
        #     self.content.lbl.setText(val)
        #
        #     self.markInvalid(False)
        #
        #     self.markReady(False)
        #
        #     self.grNode.setToolTip("")

        return val

    # def evaluationOperation(self, input1, **kwargs):
    #     self.lbl



    def onStatuesChange(self):
        self.markReady()

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port or foutput_port is None:
            self.markInvalid()

        elif finput_port and foutput_port is None:
            self.markReady()