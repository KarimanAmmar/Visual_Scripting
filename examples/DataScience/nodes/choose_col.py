import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLabel, QComboBox, QVBoxLayout
from iconify.qt import QtCore

from examples.DataScience.datascience_conf import register_node, OP_NODE_CHOOSE_COL
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent


# Class To Make Combobx Checkable
class CheckableComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self._changed = False

        self.view().pressed.connect(self.handleItemPressed)

#Method to make combobox checkable
    def setItemChecked(self, index, checked=False):
        item = self.model().item(index, self.modelColumn())  # QStandardItem object

        if checked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)

#Method to make multiple check in combobox
    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)

        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self._changed = True

#Method to make the dropdown list always open
    def hidePopup(self):
        if not self._changed:
            super().hidePopup()
        self._changed = False


    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == Qt.Checked

class DataScienceGraphicalChooseCol(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 210
        self.height = 130


class DataScienceContentChooseCol(DataScienceContent):

    def createContentWidget(self):

        mainLayout = QVBoxLayout()

        self.lbl = QLabel("Choose The Column Name", self)
        mainLayout.addWidget(self.lbl)
        self.lbl.move(18, 20)
        self.lbl.setStyleSheet("font: bold 13px;")


        self.combo_box = CheckableComboBox()
        mainLayout.addWidget(self.combo_box)
        self.combo_box.setStyleSheet("background-color: #5885AF;"
                                     "border-radius: 10px;"
                                     "font: bold 14px;"
                                     "padding: 6px;")
        self.combo_box.move(30, 60)
        self.combo_box.resize(150, 28)

        self.combo_box.currentIndexChanged.connect(self.know_the_change)

        self.setLayout(mainLayout)

        self.combo_box.currentIndexChanged.connect(self.selectionchange)

        self.checked_items = []

    def selectionchange(self):
        current_index = self.combo_box.currentIndex()
        current_text = self.combo_box.currentText()

        if self.combo_box.itemChecked(current_index):
            self.checked_items.append(current_text)
        elif current_text in self.checked_items:
            self.checked_items.remove(current_text)

        print("Checked items:", self.checked_items)
        return self.checked_items



        # for i in range(self.combo_box.count()):
        #     print('Index: {0} is checked {1}'.format(i, self.combo_box.itemChecked(i)))
        # print("////////////////////////////////////////////////")

    def get_combobox_changed_text(self):
        selected = self.combo_box.currentText()
        return selected

    def know_the_change(self,index):
        old_item = self.combo_box.itemText(index - 1) if index > 0 else self.combo_box.itemText(0)
        new_item = self.combo_box.currentText()

        if old_item == new_item:
            return False
        else:
            return True

@register_node(OP_NODE_CHOOSE_COL)
class DataScienceNodeChooseCol(DataScienceNode):
    # icon = "icons/drop.png"
    op_code = OP_NODE_CHOOSE_COL
    op_title = "Choose Column"
    content_label = "CC"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def getInnerClasses(self):
        self.content = DataScienceContentChooseCol(self)
        self.grNode = DataScienceGraphicalChooseCol(self)

    def evaluationImplementation(self):
        super().evaluationImplementation()
        first_input = self.getInput(0)

        dataframe = pd.DataFrame(first_input.value)

        if first_input is None:
            self.markInvalid()
            self.grNode.setToolTip("Please connect all inputs")
            return None

        else:
            val = self.evaluationOperation(first_input.nodeEvaluation())
            self.value = val

            if dataframe.empty:
                self.grNode.setToolTip("Empty Data Frame")
                self.markInvalid(True)

                self.markDescendantsInvalid()
                self.markDescendantsReady(False)

                return self.value


            elif not self.content.know_the_change(self.content.combo_box.currentIndex()):
                self.markReady()
                self.markInvalid(False)
                self.grNode.setToolTip("")

                self.markDescendantsInvalid(False)
                self.markDescendantsReady()

                return self.value

            elif self.content.know_the_change(self.content.combo_box.currentIndex()):

                self.markReady()
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

        for i in range(self.content.combo_box.count()):
            self.content.combo_box.setItemChecked(i,False)

        chosen_cols = self.content.selectionchange()
        # index = [dataframe.columns.get_loc(col_name) for col_name in chosen_cols]
        selected_df = dataframe.loc[:, chosen_cols]
        # print(index)


        return selected_df



    def onStatuesChange(self):
        self.markReady()

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
