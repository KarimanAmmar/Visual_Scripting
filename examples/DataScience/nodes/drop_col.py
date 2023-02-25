import pandas as pd
from PyQt5.QtWidgets import QLabel, QComboBox

from examples.DataScience.datascience_conf import register_node, OP_NODE_DROP_COL_BY_NAME
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent


class DataScienceGraphicalDropColName(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 210
        self.height = 130


class DataScienceContentDropColName(DataScienceContent):

    def createContentWidget(self):
        df = pd.DataFrame({})

        self.lbl = QLabel("Choose The Column Name", self)
        self.lbl.move(18, 20)
        self.lbl.setStyleSheet("font: bold 13px;")

        self.combo_box = QComboBox(self)
        self.combo_box.setStyleSheet("background-color: #5885AF;"
                                     "border-radius: 10px;"
                                     "font: bold 14px;"
                                     "padding: 6px;")
        self.combo_box.move(30, 60)
        self.combo_box.resize(150, 28)

        self.combo_box.currentIndexChanged.connect(self.get_selected_text)

    def get_selected_text(self):
        # get the selected item from the combo box
        self.selected = self.combo_box.currentText()

        return self.selected


@register_node(OP_NODE_DROP_COL_BY_NAME)
class DataScienceNodeDropColName(DataScienceNode):
    # icon = "icons/in.png"
    op_code = OP_NODE_DROP_COL_BY_NAME
    op_title = "Drop Column By Name"
    content_label = "DC"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def getInnerClasses(self):
        self.content = DataScienceContentDropColName(self)
        self.grNode = DataScienceGraphicalDropColName(self)

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

            if self.content.get_selected_text():
                self.markReady(True)
                # self.markInvalid(False)
            else:
                self.markReady(False)
                self.markInvalid(False)

            self.grNode.setToolTip("")

            return val

    def evaluationOperation(self, input1, **kwargs):

        dataframe = pd.DataFrame(input1)

        for col in dataframe.columns:

            self.content.combo_box.addItem(col)

        print("ODD")
        print(self.content.selected)

        return dataframe

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port or foutput_port is None:
            self.markInvalid()

        elif finput_port and foutput_port is None:
            self.markReady()
