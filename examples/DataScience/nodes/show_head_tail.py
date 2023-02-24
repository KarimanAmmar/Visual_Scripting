from examples.DataScience.datascience_conf import register_node, OP_NODE_SHOW_TAIL_CSV , OP_NODE_SHOW_HEAD_CSV
from examples.DataScience.nodes.show_dataframe import DataScienceNodeOUTPUT, DataScienceOUTPUTContent, \
    DataScienceGraphicalOUTPUT

class DataScienceGraphicalShowTail(DataScienceGraphicalOUTPUT):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 900
        self.height = 250

class DataScienceShowTailContent(DataScienceOUTPUTContent):

    def createContentWidget(self):
        super().createContentWidget()
        self.table.resize(900,224)

    def update_table(self, dataframe):
        super().update_table(dataframe)

@register_node(OP_NODE_SHOW_HEAD_CSV)
class DataScienceNodeShowTail(DataScienceNodeOUTPUT):
    # icon = "icons/out.png"
    op_code = OP_NODE_SHOW_HEAD_CSV
    op_title = "Show The Head of Data Frame"

    def getInnerClasses(self):
        self.content = DataScienceShowTailContent(self)
        self.grNode = DataScienceGraphicalShowTail(self)

    def evaluationImplementation(self):

        input_socket = self.getInput(0)

        if input_socket is None:
            self.markReady()
            self.grNode.setToolTip("Input is not connected")
            return

        elif input_socket.value.empty:
            self.markInvalid()
            self.grNode.setToolTip("Empty Data Frame")
            return

        elif input_socket.value is not None:
            self.content.update_table(input_socket.value.head())
            self.grNode.setToolTip("")

            self.markInvalid(False)
            self.markReady(False)
            return


@register_node(OP_NODE_SHOW_TAIL_CSV)
class DataScienceNodeShowTail(DataScienceNodeOUTPUT):
    # icon = "icons/out.png"
    op_code = OP_NODE_SHOW_TAIL_CSV
    op_title = "Show The Tail of Data Frame"

    def getInnerClasses(self):
        self.content = DataScienceShowTailContent(self)
        self.grNode = DataScienceGraphicalShowTail(self)

    def evaluationImplementation(self):

        input_socket = self.getInput(0)

        if input_socket is None:
            self.markReady()
            self.grNode.setToolTip("Input is not connected")
            return

        elif input_socket.value.empty:
            self.markInvalid()
            self.grNode.setToolTip("Empty Data Frame")
            return

        elif input_socket.value is not None:
            self.content.update_table(input_socket.value.tail())
            self.grNode.setToolTip("")

            self.markInvalid(False)
            self.markReady(False)
            return

