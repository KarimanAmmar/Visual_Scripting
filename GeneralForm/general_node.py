from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF
from qtpy.QtWidgets import QLabel

from nodeeditor.base_nodes.func_node import AllNodeFunctions
from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions
from nodeeditor.base_nodes.graphical_node import DrawGraphicalNode
from nodeeditor.base_sockets.func_socket import LEFT_CENTER, RIGHT_CENTER

class NodeGraphicsNode(DrawGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 100
        self.height = 40
        self.edge_roundness = 9
        self.edge_padding = 0
        self.title_horizontal_padding = 6
        self.title_vertical_padding = 10

    def drawingAssets(self):
        super().drawingAssets()

        self.icons = QImage("icons/status_icons.png")

    # to draw the state of every node
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)


        offset = 24.0

        if self.node.isReady(): offset = 0.0

        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class NodeContent(AllContentWidgetFunctions):
    def createContentWidget(self):
        lbl = QLabel(self.node.content_label, self)
        content_label = "{  |  |  | Task#2 | Task#1 }"
        lbl.setObjectName(self.node.content_label_objname)


class GeneralNode(AllNodeFunctions):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    GraphicsNode_class = NodeGraphicsNode
    NodeContent_class = NodeContent

    def __init__(self, scene, inputs=[4,4], outputs=[4]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.value = None


        self.markReady()

    def nodeSettings(self):
        super().nodeSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER