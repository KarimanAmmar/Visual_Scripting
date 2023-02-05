import pandas as pd
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel, QTableWidget, QTableWidgetItem
from qtpy.QtCore import Qt
from examples.DataScience.datascience_conf import register_node, OP_NODE_SHOW_CSV
from examples.DataScience.datascience_node_base import DataScienceNode,DataScienceGraphicalNode

from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions
from nodeeditor.base_system_properties.utils_no_qt import dumpException

class DataScienceGraphicalOUTPUT(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 600
        self.height = 400
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10


class DataScienceOUTPUTContent(AllContentWidgetFunctions):
    def createContentWidget(self):
        self.edit = QLabel()

        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]

            # Read the data from the CSV file into a data frame
            df = pd.read_csv(file_path)

            # Create a table widget
            table_widget = QTableWidget(self)
            table_widget.setRowCount(df.shape[0])
            table_widget.setColumnCount(df.shape[1])
            table_widget.setHorizontalHeaderLabels(list(df.columns))
            table_widget.resize(900,1200)
            # table_widget.setWordWrap(True)
            # table_widget.showMaximized()

            # Populate the table widget with data from the data frame
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QTableWidgetItem(str(df.iloc[row, col]))
                    table_widget.setItem(row, col, item)


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

@register_node(OP_NODE_SHOW_CSV)
class DataScienceNodeOUTPUT(DataScienceNode):
    icon = "icons/out.png"
    op_code = OP_NODE_SHOW_CSV
    op_title = "Show The Data Frame"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3], outputs=[])
        self.nodeEvaluation()  # eval() from the calculator node base

    def getInnerClasses(self):
        self.content = DataScienceOUTPUTContent(self)
        self.grNode = DataScienceGraphicalOUTPUT(self)

    def evaluationImplementation(self):  # evalImplementation which is in eval which become nodeEvaluations to override the calculatorEvaluationImp of the calculator node base

        user_input = self.content.edit.text()
        constrainted_value = int(user_input)
        self.value = constrainted_value

        self.markReady(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsReady()

        self.grNode.setToolTip("")

        self.nodeChildrenEvaluation()

        return self.value

    def onInputChanged(self, socket=None):
        super().onInputChanged()
        # self.nodeEvaluation()
