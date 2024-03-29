import pandas as pd
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QImage, QFont, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QLineEdit

from examples.DataScience.datascience_conf import register_node, OP_NODE_FILTER
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent


class DataScienceGraphicalFilter(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 210
        self.height = 180
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10


class DataScienceFilterContent(DataScienceContent):

    def createContentWidget(self):
        self.lbl = QLabel("Choose Column: ", self)
        self.lbl.move(30, 10)
        self.lbl.setStyleSheet("font: bold 13px;")

        self.combobox = QComboBox(self)
        self.combobox.move(25, 35)
        self.combobox.resize(150, 28)
        self.combobox.setStyleSheet("background-color: #5885AF;"
                                    "border-radius: 10px;"
                                    "font: bold 14px;"
                                    "padding: 6px;")

        self.lbl = QLabel("Enter value : ", self)
        self.lbl.move(30, 80)
        self.lbl.setStyleSheet("font: bold 13px;")

        self.textbox = QLineEdit(self)
        self.textbox.move(25, 105)
        self.textbox.resize(150, 28)
        self.textbox.setPlaceholderText("Variable")
        self.textbox.setStyleSheet(
                                    "background-color: #5885AF;"
                                    "border-radius: 10px;"
                                    "font: 12px;"
                                    "padding: 6px;")



        self.combobox.currentIndexChanged.connect(self.know_the_change)


    def printSelectedColumnsCombo1(self):
        column1 = self.combobox.currentText()
        return column1

    def know_the_change(self,index):
        old_item = self.combobox.itemText(index - 1) if index > 0 else self.combobox.itemText(0)
        new_item = self.combobox.currentText()

        if old_item == new_item:
            return False
        else:
            return True


@register_node(OP_NODE_FILTER)
class DataScienceNodeMelt(DataScienceNode):
    icon = "icons/rename.png"
    op_code = OP_NODE_FILTER
    op_title = "Filter"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def getInnerClasses(self):
        self.content = DataScienceFilterContent(self)
        self.grNode = DataScienceGraphicalFilter(self)

    def evaluationImplementation(self):
        first_input = self.getInput(0)
        text = self.content.textbox.text()




        if first_input is None:
            self.markInvalid()
            self.markDescendantsInvalid()
            self.grNode.setToolTip("Please connect all inputs")
            return None
        else:
            val = self.evaluationOperation(first_input.nodeEvaluation())
            self.value = val

            if val.empty:
                self.markInvalid(True)
                self.grNode.setToolTip("Empty Data Frame")

                self.markDescendantsInvalid()
                self.markDescendantsReady(False)

                return self.value

            elif not self.content.know_the_change(self.content.combobox.currentIndex()) and text:
                self.markReady(False)
                self.markInvalid(False)
                self.grNode.setToolTip("")

                self.markDescendantsInvalid(False)
                self.markDescendantsReady()

                return self.value

            elif self.content.know_the_change(self.content.combobox.currentIndex()) and text:
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

        if self.content.combobox.count() == 0:
            self.content.combobox.addItems(self.col_names)
        else:
            pass

        chosen_col = self.content.printSelectedColumnsCombo1()

        chosen_col_index = dataframe.columns.get_loc(chosen_col)

        text = self.content.textbox.text()


        df_Filtered = dataframe[ dataframe[dataframe.columns[chosen_col_index]] == text]


        self.content.combobox.currentIndexChanged.connect(self.onStatuesChange)

        print(df_Filtered)

        return df_Filtered


    def onStatuesChange(self):
        self.markReady()


    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        self.content.combobox.clear()

        self.content.textbox.clear()

        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port or foutput_port is None:
            self.markInvalid()

        elif finput_port and foutput_port is None:
            self.markReady()

