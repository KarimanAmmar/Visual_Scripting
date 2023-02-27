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

        self.df = pd.DataFrame({})



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

        # self.combo_box.activated[str].connect(self.get_selected_text)
        # self.combo_box.currentIndexChanged.connect(self.handle_combobox_change)

        self.combo_box.currentIndexChanged.connect(self.know_the_change)

        # self.combo_box.currentTextChanged.connect(self.handle_combobox_change)

        self.lbl_t = QLabel(self.combo_box.itemText(0), self)
        self.lbl_t.move(18, 5)
        self.lbl_t.setStyleSheet("font: bold 13px;")

        # self.combo_box.setMaxVisibleItems(3)


    def handle_combobox_change(self):

        selected = self.combo_box.currentText()

        self.lbl_t.setText(self.combo_box.currentText())

        return selected



    def know_the_change(self,index):

        old_item = self.combo_box.itemText(index - 1) if index > 0 else self.combo_box.itemText(0)
        # old_item = self.combo_box.itemText(0)

        new_item = self.combo_box.currentText()
        # print(f"Selected item changed from '{old_item}' to '{new_item}'")

        if old_item == new_item:
            # print("F")
            # print(self.combo_box.currentIndex())
            return False
        else:
            # print("T")
            # print(self.combo_box.currentIndex())
            return True

    # def get_selected_text(self):
    #     # get the selected item from the combo box
    #     self.selected = self.combo_box.currentText()
    #
    #     return self.selected


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
                self.grNode.setToolTip("Empty Data Frame")
                self.markInvalid(True)

            # elif self.content.combo_box.currentText() != self.content.combo_box.itemText(0):
            #     self.markReady(True)
            #     self.grNode.setToolTip("HAHA")
            #
            # elif self.content.combo_box.currentText() == self.content.combo_box.itemText(0):
            #     self.markReady(True)
            #     self.markInvalid(False)
            #     self.grNode.setToolTip("xa")

            # elif self.content.lbl_t == self.content.combo_box.currentText():
            # # elif not self.content.know_the_change(self.content.combo_box.currentIndex()):
            #     self.markReady(False)
            #     self.markInvalid(False)
            #     self.grNode.setToolTip("")
            #
            #     return self.value

            elif self.content.lbl_t != self.content.combo_box.currentText():
            # elif self.content.know_the_change(self.content.combo_box.currentIndex()):

                self.markReady(False)
                self.markInvalid(False)
                self.grNode.setToolTip("")

                return self.value

            return self.value

    def evaluationOperation(self, input1, **kwargs):

        dataframe = pd.DataFrame(input1)

        self.col_names = list(dataframe.columns)

        if self.content.combo_box.count() == 0:

            self.content.combo_box.addItems(self.col_names)

        else:
            pass

        ep_value = self.content.handle_combobox_change()

        index = dataframe.columns.get_loc(ep_value)

        new_dataframe = dataframe.drop(dataframe.columns[index] , axis = 1)

        self.content.combo_box.currentTextChanged.connect(self.new)

        return new_dataframe

    def new(self):
        self.markReady()
        # if self.content.combo_box.count() == 0:
        #
        #     self.content.combo_box.addItem(self.col_names)
        #
        # else:
        #     # self.content.combo_box.clear()
        #     self.content.combo_box.addItems(self.col_names)

        # if self.content.combo_box.itemText(0) is None:
        #     self.content.combo_box.addItems(self.col_names)
        #
        # elif self.content.combo_box.itemText(0) is not None:
        #     pass
        #     # self.content.combo_box.clear()
        #     # self.content.combo_box.addItems(self.col_names)

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        self.content.combo_box.clear()
        self.markReady()

        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port or foutput_port is None:
            self.markInvalid()

        elif finput_port and foutput_port is None:
            self.markReady()
