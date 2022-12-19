from PyQt5.QtGui import QColor, QFont, QPen, QBrush
from PyQt5.QtWidgets import QMessageBox
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from examples.Calculator.calc_conf import register_node, OP_NODE_INPUT
from examples.Calculator.calc_node_base import CalcNode, CalcGraphicsNode
from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions
from nodeeditor.base_system_properties.utils_no_qt import dumpException


class CalcInputContent(AllContentWidgetFunctions):
    def createContentWidget(self):
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)

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


@register_node(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.nodeEvaluation()  # eval() from the calculator node base

    def getInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

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
        self.nodeEvaluation()
