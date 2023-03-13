import pandas as pd
from PyQt5.QtWidgets import QLabel, QComboBox

from examples.DataScience.datascience_conf import register_node, OP_NODE_SHAPE
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent




@register_node(OP_NODE_SHAPE)
class DataScienceNodeShape(DataScienceNode):
    icon = "icons/drop.png"
    op_code = OP_NODE_SHAPE
    op_title = "Shape"
    content_label = "SH"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)


    def evaluationImplementation(self):
        super().evaluationImplementation()
        first_input = self.getInput(0)

        if first_input is None:
            self.markInvalid()
            self.markDescendantsInvalid()
            self.grNode.setToolTip("Please connect all inputs")

            return None

        else:
            val = self.evaluationOperation(first_input.nodeEvaluation())
            self.value = val

            # to paint the Evaluated State with the green sign
            self.markReady(False)
            self.markInvalid(False)

            self.markDescendantsInvalid(False)
            self.markDescendantsReady()

            self.grNode.setToolTip("")

            return val


    def evaluationOperation(self, input1, **kwargs):

        dataframe = pd.DataFrame(input1)

        shape = dataframe.shape

        col_len = len(dataframe.columns)
        rows_len = len(dataframe.index)
        col_len = str(col_len)
        rows_len = str(rows_len)
        shape = (f"numbers of columns "+col_len+"\n numbers of row = "+col_len)


        return shape

    def onStatuesChange(self):
        self.markReady()

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        self.markReady()

        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port is None:
            self.markInvalid()
            self.grNode.setToolTip("Connect input with dataframe")


        elif finput_port and foutput_port is None:
            self.markReady()
