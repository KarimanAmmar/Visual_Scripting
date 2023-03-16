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

        self.combo_box.currentIndexChanged.connect(self.know_the_change)

    def get_combobox_changed_text(self):
        selected = self.combo_box.currentText()
        return selected

    def know_the_change(self, index):
        old_item = self.combo_box.itemText(index - 1) if index > 0 else self.combo_box.itemText(0)
        new_item = self.combo_box.currentText()

        if old_item == new_item:
            return False
        else:
            return True


@register_node(OP_NODE_DROP_COL_BY_NAME)
class DataScienceNodeDropColName(DataScienceNode):
    icon = "icons/drop.png"
    op_code = OP_NODE_DROP_COL_BY_NAME
    op_title = "Drop Column"
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
            self.grNode.setToolTip("Please connect all inputs")
            return None

        else:
            val = self.evaluationOperation(first_input.nodeEvaluation())
            self.value = val

            if val.empty:
                self.grNode.setToolTip("Empty Data Frame")
                self.markInvalid(True)

                self.markDescendantsInvalid()
                self.markDescendantsReady(False)

                return self.value


            elif not self.content.know_the_change(self.content.combo_box.currentIndex()):
                self.markReady(False)
                self.markInvalid(False)
                self.grNode.setToolTip("")

                self.markDescendantsInvalid(False)
                self.markDescendantsReady()

                return self.value

            elif self.content.know_the_change(self.content.combo_box.currentIndex()):

                self.markReady(False)
                self.markInvalid(False)
                self.grNode.setToolTip("")

                self.markDescendantsInvalid(False)
                self.markDescendantsReady()

                return self.value

            return self.value

    def evaluationOperation(self, input1, **kwargs):

        dataframe = pd.DataFrame(input1)

        self.col_names = list(dataframe.columns)

        if self.content.combo_box.count() == 0:

            self.content.combo_box.addItems(self.col_names)

        else:
            pass

        chosen_col = self.content.get_combobox_changed_text()

        chosen_col_index = dataframe.columns.get_loc(chosen_col)

        new_dataframe = dataframe.drop(dataframe.columns[chosen_col_index], axis=1)

        self.content.combo_box.currentTextChanged.connect(self.onStatuesChange)

        return new_dataframe

    def onStatuesChange(self):
        self.markReady()

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        self.content.combo_box.clear()
        self.markReady()

        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port is None:
            self.markInvalid()
            self.grNode.setToolTip("Connect input with dataframe")


        elif finput_port and foutput_port is None:
            self.markReady()
