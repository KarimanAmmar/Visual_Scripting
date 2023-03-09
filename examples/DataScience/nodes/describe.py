import pandas as pd

from examples.DataScience.datascience_conf import register_node, OP_NODE_DROP_NANS, OP_NODE_DESCRIBE
from examples.DataScience.datascience_node_base import DataScienceNode

@register_node(OP_NODE_DESCRIBE)
class DataScienceNodeDescribe(DataScienceNode):
    # icon = "icons/in.png"
    op_code = OP_NODE_DESCRIBE
    op_title = "Describe"
    content_label = "Describe"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def evaluationImplementation(self):
        super().evaluationImplementation()
        first_input = self.getInput(0)

        if first_input is None:
            self.markInvalid()
            self.markDescendantsInvalid()
            self.grNode.setToolTip("Please connect all inputs")

            return None

        else:
            val = self.evaluationOperation(first_input.nodeEvaluation())
            self.value = val

            # to paint the Evaluated State with the green sign
            self.markReady(False)
            self.markInvalid(False)

            self.grNode.setToolTip("")

            return val

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port or foutput_port is None:
            self.markInvalid()

        elif finput_port and foutput_port is None:
            self.markReady()

    def evaluationOperation(self, input1, **kwargs):

        f_dataframe = pd.DataFrame(input1)

        new_df = f_dataframe.describe()
        print(new_df)


        return new_df
