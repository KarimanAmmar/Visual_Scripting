import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLabel, QComboBox, QVBoxLayout
from iconify.qt import QtCore

from examples.DataScience.datascience_conf import register_node, OP_NODE_CHOOSE_COL
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent


class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handle_item_pressed)
        self._changed = False
        self._items = []


    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == 2:
            item.setCheckState(0)
            self._items.remove(item.text())
        else:
            item.setCheckState(2)
            self._items.append(item.text())
        self._changed = True


    def hidePopup(self):
        if not self._changed:
            super().hidePopup()
        self._changed = False

    def items(self):
        return self._items

    def selected_indices(self, df):
        return [df.columns.get_loc(item) for item in self._items]

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
        self.combo_box.currentIndexChanged.connect(self.selectionchange)

        self.setLayout(mainLayout)




    def selectionchange(self):
        if self.combo_box._changed:
            print(self.combo_box.items())
            self.combo_box._changed = False


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
    icon = "icons/c.png"
    op_code = OP_NODE_CHOOSE_COL
    op_title = "Show Specific Columns"
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


        chosen_cols = self.content.combo_box.selected_indices(dataframe)
        selected_df = dataframe.iloc[:,chosen_cols]


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
