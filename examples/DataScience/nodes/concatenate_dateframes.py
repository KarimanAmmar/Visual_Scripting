import pandas as pd

from examples.DataScience.datascience_conf import register_node, OP_NODE_CONCATENATE_CSV
from examples.DataScience.datascience_node_base import DataScienceNode


@register_node(OP_NODE_CONCATENATE_CSV)
class DataScienceNodeConcate(DataScienceNode):
    # icon = "icons/in.png"
    op_code = OP_NODE_CONCATENATE_CSV
    op_title = "Concatenate Frames"
    content_label = "CONCATENATE"

    def evaluationOperation(self, input1, input2):

        f_dataframe = pd.DataFrame(input1)

        s_dataframe = pd.DataFrame(input2)

        frames = [f_dataframe, s_dataframe]

        result = pd.concat(frames,axis=1)

        return result

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        sinput_port = self.getInput(1)
        foutput_port = self.getOutputs(0)

        if finput_port and sinput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port or sinput_port or foutput_port is None:
            self.markInvalid()

        elif finput_port and sinput_port and foutput_port is None:
            self.markReady()