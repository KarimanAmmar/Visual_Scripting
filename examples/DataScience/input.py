import pandas as pd

from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel

from qtpy.QtCore import Qt
from examples.DataScience.datascience_conf import register_node, OP_NODE_READ_CSV
from examples.DataScience.datascience_node_base import DataScienceNode,DataScienceGraphicalNode

from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions
from nodeeditor.base_system_properties.utils_no_qt import dumpException

class DataScienceGraphicalINPUT(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 230
        self.height = 90
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

class DataScienceINPUTContent(AllContentWidgetFunctions):

    # global df
    # df = pd.DataFrame({})
    def createContentWidget(self):
        self.edit = QPushButton("PRESS HERE TO LOAD DATA FRAME", self)
        self.edit.clicked.connect(self.showDialog)

        self.lbl = QLabel("READY TO LOAD ANY CSV File", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)
        self.lbl.move(10,40)
        self.lbl.setStyleSheet("background-color: transparent;")
        self.lbl.setWordWrap(True)


    def showDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Plase choose CSVs files", " ",
                                                "CSV Files (*.csv)", options=options)
        if files:
            self.dfs = [pd.read_csv(file) for file in files]
            print(self.dfs)
            self.lbl.setText("LOADED THE CSV")
            # df = self.dfs
            # return df

        else:
            self.lbl.setText("CANT LOAD")




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
    op_title = "Input"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.nodeEvaluation()  # eval() from the calculator node base

    def getInnerClasses(self):
        self.content = DataScienceINPUTContent(self)
        self.grNode = DataScienceGraphicalINPUT(self)

    def evaluationImplementation(self):  # evalImplementation which is in eval which become nodeEvaluations to override the calculatorEvaluationImp of the calculator node base

        # self.input = DataScienceINPUTContent(self)
        # self.fInput = self.input.dfs
        #
        # self.ss = df
        # if self.ss:
        #     self.markInvalid(True)


        self.markReady(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsReady()

        self.grNode.setToolTip("")

        self.nodeChildrenEvaluation()

        return self.value

    def onInputChanged(self, socket=None):
        super().onInputChanged()
        self.nodeEvaluation()
