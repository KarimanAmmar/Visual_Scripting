import pandas as pd

from examples.DataScience.datascience_conf import register_node, OP_NODE_DROP_NANS, OP_NODE_DESCRIBE
from examples.DataScience.datascience_node_base import DataScienceNode


@register_node(OP_NODE_DESCRIBE)
class DataScienceNodeDescribe(DataScienceNode):
    """
      This class represents a Data Science node that show describes statistics the input dataframe.
      Functions:
      init(self, scene, inputs=[3], outputs=[3]): Constructs a DataScienceNodeDescribe object.
      evaluationImplementation(self): Implements the evaluation process of the node.
      onInputChanged(self, socket=None): Called when the input socket of the node changes.
      evaluationOperation(self, input1, **kwargs): Returns a new dataframe object that contains the description of the input dataframe.
      Attributes:
      op_code: An integer representing the operation code of the node.
      op_title: A string representing the title of the node.
      content_label: A string representing the label of the node's content.
      Note:
      This class is registered as a node using the @register_node(OP_NODE_DESCRIBE) decorator.
      The describe() function of pandas.DataFrame is used to generate a new dataframe that contains various summary statistics of the input dataframe.
      """
    # icon = "icons/in.png"
    op_code = OP_NODE_DESCRIBE
    op_title = "Describe"
    content_label = "Describe"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def evaluationImplementation(self):
        """Define a method called evaluationImplementation() for a class, which evaluates a node in a graph"""
        # Call the implementation of this method in any parent classes

        super().evaluationImplementation()

        # Get the first input for the node
        first_input = self.getInput(0)

        # If no input is found, mark the node as invalid and all of its descendants as invalid
        # Set the tooltip to inform the user to connect all inputs
        if first_input is None:
            self.markInvalid()
            self.markDescendantsInvalid()
            self.grNode.setToolTip("Please connect all inputs")

            return None

        # If an input is found, evaluate the node using the evaluationOperation() method
        else:
            # Perform an operation on the input node to compute a result
            val = self.evaluationOperation(first_input.nodeEvaluation())
            # Store the computed value in the node's value attribute
            self.value = val
            # Mark the node as ready and remove any error messages from the tooltip
            self.markReady(False)
            self.markInvalid(False)

            self.grNode.setToolTip("")
            # Return the computed value
            return val

    def onInputChanged(self, socket=None):
        """Define a method called onInputChanged() for a class, which is called when the input to a node changes"""
        # Get the first input and output for the node
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)

        # If both the input and output are connected, evaluate the node
        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        # If either the input or output is not connected, mark the node as invalid
        elif finput_port is None:
            self.markInvalid()

        # If the input is connected but the output is not, mark the node as ready
        elif finput_port and foutput_port is None:
            self.markReady()

    def evaluationOperation(self, input1, **kwargs):
        """This function takes an input and computes the summary describe statistics of the input using pandas"""

        f_dataframe = pd.DataFrame(input1)

        # Compute the summary statistics using the describe function in pandas
        new_df = f_dataframe.describe()
        print(new_df)

        # Return the summary statistics dataframe
        return new_df
