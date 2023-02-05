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
        self.width = 210
        self.height = 120
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

class DataScienceINPUTContent(AllContentWidgetFunctions):

    def createContentWidget(self):
        self.lbl = QLabel("READY TO LOAD ANY CSV File", self)
        self.lbl.move(10,40)
        self.lbl.setWordWrap(True)

        self.edit = QPushButton("PRESS HERE TO LOAD DATA FRAME", self)

        if self.edit.clicked.connect(self.showDialog):
            self.new_dataframe = self.showDialog()
            print("WWWWWWWW222222222WWWWWWWWWWWWWWW")
            print(self.new_dataframe)

        print(self.new_dataframe)
        # self.new_dataframe = self.hehe
        print("WWWWWWWWWWWWWWWWWWWWWWW")

        print(self.new_dataframe)


    def showDialog(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]

            # Read the data from the CSV file into a data frame
            df = pd.read_csv(file_path)
            print(df)

            self.lbl.setText("LOADED THE CSV")
            # return df
            print("NOPE")
            # self.new_dataframe2 = df

            # print("the new dataframe value in dialog method")
            # print(self.new_dataframe2)
            # self.process_data(df)

        else:
            self.lbl.setText("CANT LOAD")

    # def process_data(self, dataframe):
    #     print("FIRST LINE OF THE PROCESS METHOD")
    #     print(dataframe.shape)
    #     print(dataframe.temperature.mean())
    #     print(dataframe['temperature'].std())



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

        # user_input = self.content.edit.text()
        # constrainted_value = int(user_input)
        # self.value = constrainted_value

        user_input = self.content.new_dataframe
        self.value = user_input


        if self.value:
            self.markReady(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")
        else:
            self.markInvalid()



        # self.markDescendantsInvalid(False)
        # self.markDescendantsReady()

        self.grNode.setToolTip("")

        self.nodeChildrenEvaluation()

        return self.value

    def onInputChanged(self, socket=None):
        super().onInputChanged()
        self.nodeEvaluation()
