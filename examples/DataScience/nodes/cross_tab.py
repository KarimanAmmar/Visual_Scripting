import pandas as pd
from PyQt5 import Qt
from PyQt5.QtWidgets import QLabel, QComboBox, QCheckBox

from examples.DataScience.datascience_conf import register_node, OP_NODE_CROSS_TAB
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent

class DataScienceGraphicalCrossTab(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 210
        self.height = 230
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

class DataScienceCrossTabContent(DataScienceContent):

    def createContentWidget(self):

        self.lbl = QLabel("Choose Index: ", self)
        self.lbl.move(30, 10)
        self.lbl.setStyleSheet("font: bold 13px;")

        self.combobox1 = QComboBox(self)
        self.combobox1.move(25, 35)
        self.combobox1.resize(150, 28)
        self.combobox1.setStyleSheet("background-color: #5885AF;"
                                    "border-radius: 10px;"
                                    "font: bold 14px;"
                                    "padding: 6px;")

        self.lbl = QLabel("Choose Column : ", self)
        self.lbl.move(30, 80)
        self.lbl.setStyleSheet("font: bold 13px;")


        self.combobox2 = QComboBox(self)
        self.combobox2.move(25, 105)
        self.combobox2.resize(150, 28)
        self.combobox2.setStyleSheet("background-color: #5885AF;"
                                       "border-radius: 10px;"
                                       "font: bold 14px;"
                                        "padding: 6px;")

        self.checkbox = QCheckBox('Margins', self)
        self.checkbox.move(25, 150)
        self.checkbox.resize(150, 28)
        self.checkbox.setStyleSheet(

            "background-color: #5885AF;"
            "border-radius: 10px;"
            "font: 12px;"
            "padding: 6px;"
        )



        self.combobox1.currentIndexChanged.connect(self.know_the_changeCombo1)
        self.combobox2.currentIndexChanged.connect(self.know_the_changeCombo2)
        self.checkbox.stateChanged.connect(self.know_the_changeCombo2)




    def printSelectedColumnsCombo1(self):
        column1 = self.combobox1.currentText()
        return column1

    def printSelectedColumnsCombo2(self):
        column2 = self.combobox2.currentText()
        return column2

    def know_the_changeCombo1(self, index):
        old_item = self.combobox1.itemText(index - 1) if index > 0 else self.combobox1.itemText(0)
        new_item = self.combobox1.currentText()

        if old_item == new_item:
            return False
        else:
            return True

    def know_the_changeCombo2(self, index):
        old_item = self.combobox2.itemText(index - 1) if index > 0 else self.combobox2.itemText(0)
        new_item = self.combobox2.currentText()

        if old_item == new_item:
            return False
        else:
            return True

    def know_the_changeCheck1(self, index):
        pass


    # def know_the_changeCheck1(self, index):
    #     # old_item = self.checkbox.itemText(index - 1) if index > 0 else self.checkbox.itemText(0)
    #     # new_item = self.checkbox.currentText()
    #
    #     old_item = index != Qt.Unchecked  # get the old state
    #     new_item = self.checkbox.isChecked()  # get the new state
    #
    #     if old_item == new_item:
    #         return False
    #     else:
    #         return True





@register_node(OP_NODE_CROSS_TAB)
class DataScienceNodeCrossTab(DataScienceNode):
    icon = "icons/slicing.png"
    op_code = OP_NODE_CROSS_TAB
    op_title = "Cross Tab"


    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def getInnerClasses(self):
        self.content = DataScienceCrossTabContent(self)
        self.grNode = DataScienceGraphicalCrossTab(self)

    def evaluationImplementation(self):
        # super().evaluationImplementation()
        first_input = self.getInput(0)

        if first_input is None:
            self.markInvalid()
            self.markDescendantsInvalid()
            self.grNode.setToolTip("Please connect all inputs")

            return None

        else:
            val = self.evaluationOperation(first_input.nodeEvaluation())
            self.value = val

            if val.empty:
                self.grNode.setToolTip("Can not perform at this data frame.")
                self.markInvalid(True)

                self.markDescendantsInvalid()
                self.markDescendantsReady(False)

                return self.value

            elif self.content.know_the_changeCombo1(
                    self.content.combobox1.currentIndex()) and self.content.know_the_changeCombo2(
                    self.content.combobox2.currentIndex()):

                self.markReady(False)
                self.markInvalid(False)
                self.grNode.setToolTip("")

                self.markDescendantsInvalid(False)
                self.markDescendantsReady()

                return self.value

            elif not self.content.know_the_changeCombo1(
                    self.content.combobox1.currentIndex()) and not self.content.know_the_changeCombo2(
                    self.content.combobox2.currentIndex()):

                self.markReady(False)
                self.markInvalid(False)
                self.grNode.setToolTip("")

                self.markDescendantsInvalid(False)
                self.markDescendantsReady()

                return self.value

            elif self.content.know_the_changeCombo1(
                    self.content.combobox1.currentIndex()) and not self.content.know_the_changeCombo2(
                    self.content.combobox2.currentIndex()):

                self.markReady(False)
                self.markInvalid(False)
                self.grNode.setToolTip("")

                self.markDescendantsInvalid(False)
                self.markDescendantsReady()

                return self.value

            elif not self.content.know_the_changeCombo1(
                    self.content.combobox1.currentIndex()) and self.content.know_the_changeCombo2(
                    self.content.combobox2.currentIndex()):

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

        if self.content.combobox1.count() == 0:

            self.content.combobox1.addItems(self.col_names)
            self.content.combobox2.addItems(self.col_names)


        else:
            pass

        chosen_col1 = self.content.printSelectedColumnsCombo1()
        chosen_col2 = self.content.printSelectedColumnsCombo2()


        index1 = dataframe.columns.get_loc(chosen_col1)
        index2 = dataframe.columns.get_loc(chosen_col2)

        if self.content.checkbox.isChecked():

            df_crosstab = pd.crosstab(dataframe.iloc[:, index1], dataframe.iloc[:, index2], margins=True )

        else:
            df_crosstab = pd.crosstab(dataframe.iloc[:, index1], dataframe.iloc[:, index2])



        self.content.combobox1.currentIndexChanged.connect(self.onStatuesChange)
        self.content.combobox2.currentIndexChanged.connect(self.onStatuesChange)
        self.content.checkbox.stateChanged.connect(self.onStatuesChange)

        print(index2)
        print(index1)
        print(df_crosstab)

        return df_crosstab

    def onStatuesChange(self):
        self.markReady()

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        self.content.combobox1.clear()
        self.content.combobox2.clear()

        self.markReady()

        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port or foutput_port is None:
            self.markInvalid()

        elif finput_port and foutput_port is None:
            self.markReady()