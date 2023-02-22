import pandas as pd
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel, QTableWidget, QTableWidgetItem, QTableView, QHeaderView
from qtpy.QtCore import Qt
from examples.DataScience.datascience_conf import register_node, OP_NODE_SHOW_CSV
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode

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

        df = pd.DataFrame({})

        self.model = QStandardItemModel(df.shape[0], df.shape[1])

        # Set horizontal header labels
        self.model.setHorizontalHeaderLabels(df.columns)

        # Add data to QStandardItemModel
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[i, j]))
                self.model.setItem(i, j, item)

        # Create QTableView and set model
        table = QTableView(self)
        table.setModel(self.model)

        # Set table properties
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)

        # table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # table.verticalHeader().setDefaultSectionSize(50)

        table.setEditTriggers(QTableView.NoEditTriggers)
        table.setSelectionBehavior(QTableView.SelectRows)
        table.setSelectionMode(QTableView.SingleSelection)

        table.setWordWrap(True)
        table.setShowGrid(False)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        table.resize(599,399)



    def update_table(self, dataframe):
        # Read data from CSV file and create DataFrame
        df = pd.DataFrame(dataframe)

        # Clear current data in model
        self.model.clear()

        # Set horizontal header labels
        self.model.setHorizontalHeaderLabels(df.columns)

        # Add data to model
        for i in range(df.shape[0]):
            row_items = []
            for j in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[i, j]))
                row_items.append(item)
            self.model.appendRow(row_items)

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

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        if finput_port is not None:
            # self.nodeEvaluation()  # eval() ely fo2 3ala tol de, to be evaluated automaticlly when all inputs are connected!!
            self.markReady()

        else:
            self.markReady()

    def evaluationImplementation(self):
        self.markReady()

        input_socket = self.getInput(0)


        if input_socket is None:
            self.markReady()
            self.grNode.setToolTip("Input is not connected")
            return

        elif input_socket.content.data_frame.empty:
            self.markInvalid()
            self.grNode.setToolTip("Empty Data Frame")
            return

        elif input_socket.content.data_frame is not None:
            self.content.update_table(input_socket.content.data_frame)
            self.grNode.setToolTip("")
            self.markInvalid(False)
            self.markReady(False)
            return




