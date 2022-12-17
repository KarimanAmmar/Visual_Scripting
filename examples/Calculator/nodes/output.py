from qtpy.QtWidgets import QLabel
from qtpy.QtCore import Qt
from examples.Calculator.calc_conf import register_node, OP_NODE_OUTPUT
from examples.Calculator.calc_node_base import CalcNode, CalcGraphicsNode
from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions


class CalcOutputContent(AllContentWidgetFunctions):
    def createContentWidget(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[])

    def getInnerClasses(self):
        self.content = CalcOutputContent(self)
        self.grNode = CalcGraphicsNode(self)

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        if finput_port is not None:
            self.nodeEvaluation()  # eval() ely fo2 3ala tol de, to be evaluated automaticlly when all inputs are connected!!

        else:
            self.markReady()

    def evaluationImplementation(self):
        input_socket = self.getInput(0)
        if not input_socket:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        val = input_socket.nodeEvaluation()

        if val is None:
            self.grNode.setToolTip("Input is NaN")
            self.markInvalid()
            return

        if int(val):
            self.content.lbl.setText(f"{val}")
            self.markInvalid(False)
            self.markReady(False)
            self.grNode.setToolTip("")

        elif not int(val):
            self.content.lbl.setText(f"{val}")
            self.markInvalid(False)
            self.markReady(False)
            self.grNode.setToolTip("")

        return val
