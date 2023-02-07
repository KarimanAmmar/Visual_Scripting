import os

import pandas as pd

from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel, QTableWidget, QTableWidgetItem

from qtpy.QtCore import Qt
from examples.DataScience.datascience_conf import register_node, OP_NODE_READ_CSV
from examples.DataScience.datascience_node_base import DataScienceNode,DataScienceGraphicalNode

from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions
from nodeeditor.base_system_properties.utils_no_qt import dumpException

class DataScienceGraphicalINPUT(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 210
        self.height = 130

class DataScienceINPUTContent(AllContentWidgetFunctions):

    def createContentWidget(self):

        self.data_frame = pd.DataFrame({})

        self.lbl = QLabel("Ready to load CSV file.", self)
        self.lbl.move(10,40)

        self.edit = QPushButton("Load CSV file", self)
        self.edit.clicked.connect(self.showDialog)


    def showDialog(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)

        if file_dialog.exec_():

            self.edit.hide()
            file_path = file_dialog.selectedFiles()[0]

            file_name = os.path.basename(file_path)

            self.r_data_frame = pd.read_csv(file_path)
            self.data_frame = self.r_data_frame

            self.lbl.setText("Successfully Loaded The CSV file.\n"+file_name)
            self.lbl.adjustSize()

        else:
            self.lbl.setText("Didn't Load The CSV file.\nplease try again.")
            self.lbl.adjustSize()

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_READ_CSV)
class DataScienceNodeINPUT(DataScienceNode):
    icon = "icons/in.png"
    op_code = OP_NODE_READ_CSV
    op_title = "Load The Data Frame"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.nodeEvaluation()  # eval() from the calculator node base

    def getInnerClasses(self):
        self.content = DataScienceINPUTContent(self)
        self.grNode = DataScienceGraphicalINPUT(self)

    def evaluationImplementation(self): # evalImplementation which is in eval which become nodeEvaluations to override the calculatorEvaluationImp of the calculator node base

        if self.content.data_frame.empty:
            self.markReady(True)
            self.grNode.setToolTip("Please load any CSV file")

        else:
            print(self.content.data_frame.shape)
            print(self.content.data_frame.iloc[2:5, :-1])
            print(self.content.data_frame)
            print(self.content.data_frame.columns)

            self.value = self.content.data_frame

            self.markReady(False)
            self.markInvalid(False)

            return self.value

        # # self.markDescendantsInvalid(False)
        # # self.markDescendantsReady()
        #
        # self.grNode.setToolTip("")
        #
        # self.nodeChildrenEvaluation()
        #
        return self.value

    def onInputChanged(self, socket=None):
        super().onInputChanged()
        self.nodeEvaluation()
