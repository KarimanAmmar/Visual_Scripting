import os

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTableView, QHeaderView, QLabel, QPushButton, QFileDialog, QComboBox

from examples.DataScience.datascience_conf import register_node, OP_NODE_DROP_ROW
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode
from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions
from nodeeditor.base_system_properties.utils_no_qt import dumpException


class DataScienceGraphicalDropRow(DataScienceGraphicalNode):
    """
    A class used to represent  Data Science Graphical Node inherited from (DataScienceGraphicalNode)

    ...

    Methods
    -------
    nodeSizes()
        this method to Node width and height

    """
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 210
        self.height = 130

class DataScienceDropRow(AllContentWidgetFunctions):
    """
    A class used to represent Data Science drop rows Graphical widgets Node inherited from (AllContentWidgetFunctions)

    ...

    Methods
    -------
    createContentWidget()
        this method to content widgets on Node
            widgets-->label,combobox

    handle_combobox_change()
         ""return selected""
         select combobox text and handle it

    know_the_change()
         ""return bool""
         to know changes from combobox

    showDialog()
       this function used to file dialog show

     serialize()
       "" return res""

     deserialize()
        ""return res""


    """

    def createContentWidget(self):

        self.df = pd.DataFrame({})

        self.lbl = QLabel("Choose The Row Number", self)
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



        self.lbl_t = QLabel(self.combo_box.itemText(0), self)
        self.lbl_t.move(18, 5)
        self.lbl_t.setStyleSheet("font: bold 13px;")




    def handle_combobox_change(self):

        selected = self.combo_box.currentText()

        self.lbl_t.setText(self.combo_box.currentText())

        return selected


    def know_the_change(self,index):

        old_item = self.combo_box.itemText(index - 1) if index > 0 else self.combo_box.itemText(0)


        new_item = self.combo_box.currentText()


        if old_item == new_item:

            return False
        else:

            return True


    def showDialog(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Select File (*.csv *.xlsx)")
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)

        if file_dialog.exec_():

            self.button.hide()

            file_path = file_dialog.selectedFiles()[0]

            if file_path.endswith('.csv'):
                self.data_frame = pd.read_csv(file_path)

            if file_path.endswith('.xlsx'):
                self.data_frame = pd.read_excel(file_path)

            file_name = os.path.basename(file_path)

            self.lbl.setText("Successfully Loaded\nThe CSV file:\n\n"+file_name)
            self.lbl.move(35,20)
            self.lbl.setStyleSheet("font: bold 13px;")
            self.lbl.adjustSize()

        else:
            self.lbl.setText("Didn't Load The CSV file.\nplease try again.")
            self.lbl.adjustSize()
            self.lbl.move(27,60)
            self.lbl.setStyleSheet("font: bold 13px")

    # def serialize(self):
    #     res = super().serialize()
    #     res['value'] = self.button.text()
    #     return res

    # def deserialize(self, data, hashmap={}):
    #     res = super().deserialize(data, hashmap)
    #     try:
    #         value = data['value']
    #         self.button.setText(value)
    #         return True & res
    #     except Exception as e:
    #         dumpException(e)
    #      return res



@register_node(OP_NODE_DROP_ROW)
# OP_NODE_DROP_ROW = 9

class DataScienceNodeDropNode(DataScienceNode):
    """
    A class used to represent  Data Science Drop row Node

    ...

    Attributes
    ----------
    op code  : int
        a formatted int number  to op code saved in  datascience_conf.py
    on tittle : str
        the tittle of node used as drop node
    content label  : str
        the str that the node content label


    Methods
    -------
    evaluationImplementation()

    onInputChanged()

    getInnerClasses()

    evaluationImplementation()

    new()


    evaluationOperation()

    ""return new_dataframe""
    save rows index from data frame in list and drop rows from dataframe using index

    """

    icon = "icons/drop.png"
    op_code = OP_NODE_DROP_ROW
    icon = "icons/drop.png"
    op_title = "Drop Row"
    content_label = "DR"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def getInnerClasses(self):
            self.content = DataScienceDropRow(self)
            self.grNode = DataScienceGraphicalDropRow(self)

    def createContentWidget(self):

        self.data_frame = pd.DataFrame({})

        self.lbl = QLabel("Ready to load CSV file.", self)
        self.lbl.move(30, 60)
        self.lbl.setStyleSheet("font: bold 13px;")

        self.button = QPushButton("Load CSV file", self)
        self.button.clicked.connect(self.showDialog)
        self.button.move(23, 15)
        self.button.resize(150, 28)
        self.button.setStyleSheet("background-color: #5885AF;"
                                  "border-radius: 10px;"
                                  "font: bold 14px;")


    def evaluationImplementation(self):
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


            elif self.content.lbl_t != self.content.combo_box.currentText():


                self.markReady(False)
                self.markInvalid(False)
                self.grNode.setToolTip("")

                return self.value

            return self.value

    def new(self):
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


    def evaluationOperation(self, input1, **kwargs):

        dataframe = pd.DataFrame(input1)

        rows_count = len(dataframe.index)

        rows_list_int = list(range(1, rows_count))
        rows_list_string =[str(x) for x in rows_list_int]


        if self.content.combo_box.count() == 0:

            self.content.combo_box.addItems(rows_list_string)

        else:
            pass

        combobox_value = self.content.handle_combobox_change()

        rows_number = int( combobox_value)


        new_dataframe = dataframe.drop(rows_number-1, axis=0)

        self.content.combo_box.currentTextChanged.connect(self.new)

        return new_dataframe