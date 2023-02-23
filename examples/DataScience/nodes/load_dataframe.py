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
        self.lbl.move(30,60)
        self.lbl.setStyleSheet("font: bold 13px;")

        self.button = QPushButton("Load CSV file", self)
        self.button.clicked.connect(self.showDialog)
        self.button.move(23, 15)
        self.button.resize(150, 28)
        self.button.setStyleSheet("background-color: #5885AF;"
                                "border-radius: 10px;"
                                "font: bold 14px;")
                                # "padding: 6px;")


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

    def serialize(self):
        res = super().serialize()
        res['value'] = self.button.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.button.setText(value)
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
        self.nodeEvaluation()

    def getInnerClasses(self):
        self.content = DataScienceINPUTContent(self)
        self.grNode = DataScienceGraphicalINPUT(self)

    def evaluationImplementation(self): # evalImplementation which is in eval which become nodeEvaluations to override the calculatorEvaluationImp of the calculator node base

        if self.content.data_frame.empty:
            self.markReady(True)
            self.grNode.setToolTip("Please load any CSV file")

        else:
            self.markReady(False)
            self.markInvalid(False)

            self.markDescendantsInvalid(False)
            self.markDescendantsReady()

            self.grNode.setToolTip("")

            self.value = self.content.data_frame
            return self.value

        return self.value

    def onInputChanged(self, socket=None):
        super().onInputChanged()
        self.nodeEvaluation()
