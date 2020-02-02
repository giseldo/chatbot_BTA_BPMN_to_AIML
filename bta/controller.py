from bta.bpmn_simplifier import transform_bpmn_to_simple_bpmn
from bta.bpmn_to_finite_state_bpmn import transform_bpmn_to_finite_state_bpmn
from bta.bpmn_to_aiml import transform_bpmn_to_aiml


def converter_bpmn_aiml(filename):

    simple_bpmn_file_name = transform_bpmn_to_simple_bpmn(filename)

    finite_state_bpmn_file_name = transform_bpmn_to_finite_state_bpmn(simple_bpmn_file_name)

    transform_bpmn_to_aiml(finite_state_bpmn_file_name)

# converter_bpmn_aiml("bpmn_files\modelo.bpmn")