from GeneralForm.nodes_configuration import register_node, OP_NODE_GREATER, OP_NODE_EQUAL, OP_NODE_LESS, OP_NODE_ADD, \
    OP_NODE_SUB, OP_NODE_MUL, OP_NODE_DIV
from examples.Calculator.calc_node_base import CalcNode


@register_node(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = "icons/add.png"
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_objname = "calc_node_bg"

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        sinput_port = self.getInput(1)
        foutput_port = self.getOutputs(0)

        if finput_port and sinput_port and foutput_port is not None:
            self.nodeEvaluation()  # eval() ely fo2 3ala tol de, to be evaluated automaticlly when all inputs are connected!!

        elif finput_port or sinput_port or foutput_port is None:
            self.markInvalid()
        elif finput_port and sinput_port and foutput_port is None:
            self.markReady()

    def evaluationOperation(self, input1, input2):
        return input1 + input2


@register_node(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    icon = "icons/sub.png"
    op_code = OP_NODE_SUB
    op_title = "Substract"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        sinput_port = self.getInput(1)

        if finput_port and sinput_port is not None:
            self.nodeEvaluation()  # eval() ely fo2 3ala tol de, to be evaluated automaticlly when all inputs are connected!!

        else:
            self.markInvalid()

    def evaluationOperation(self, input1, input2):
        return input1 - input2


@register_node(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    icon = "icons/mul.png"
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_objname = "calc_node_mul"

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        sinput_port = self.getInput(1)

        if finput_port and sinput_port is not None:
            self.nodeEvaluation()  # eval() ely fo2 3ala tol de, to be evaluated automaticlly when all inputs are connected!!

        else:
            self.markInvalid()

    def evaluationOperation(self, input1, input2):
        # print('foo')
        return input1 * input2


@register_node(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    icon = "icons/divide.png"
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_objname = "calc_node_div"

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        sinput_port = self.getInput(1)

        if finput_port and sinput_port is not None:
            self.nodeEvaluation()  # eval() ely fo2 3ala tol de, to be evaluated automaticlly when all inputs are connected!!

        else:
            self.markInvalid()

    def evaluationOperation(self, input1, input2):
        return input1 / input2

# # INTEGER DIV // (5//2) , EXPONENTIATION ** (5**2) , REMINDER % (5%2)
# @register_node(OP_NODE_DIV)
# class CalcNode_Div(CalcNode):
#     icon = "icons/divide.png"
#     op_code = OP_NODE_DIV
#     op_title = "Divide"
#     content_label = "/"
#     content_label_objname = "calc_node_div"
#
#     def evalOperation(self, input1, input2):
#         return input1 / input2
#
# @register_node(OP_NODE_DIV)
# class CalcNode_Div(CalcNode):
#     icon = "icons/divide.png"
#     op_code = OP_NODE_DIV
#     op_title = "Divide"
#     content_label = "/"
#     content_label_objname = "calc_node_div"
#
#     def evalOperation(self, input1, input2):
#         return input1 / input2
#
# @register_node(OP_NODE_DIV)
# class CalcNode_Div(CalcNode):
#     icon = "icons/divide.png"
#     op_code = OP_NODE_DIV
#     op_title = "Divide"
#     content_label = "/"
#     content_label_objname = "calc_node_div"
#
#     def evalOperation(self, input1, input2):
#         return input1 / input2


# way how to register by function call
# register_node_now(OP_NODE_ADD, CalcNode_Add)
