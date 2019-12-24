from AIML_NOVO import AIMLClassNovo
from BPMN_NOVO import BPMNClassNovo
import xml.etree.ElementTree as ET


class ControladorNovo:

    def generateAIML(self, inputBPMNFileName):
        # generate necessary variables for integration from BPMN
        bpmnObject = BPMNClassNovo()
        rootBPMN = bpmnObject.getRootBPMNFromFile(inputBPMNFileName)
        templateName, pattern_event_init_value = bpmnObject.getTemplateName(rootBPMN)
        firstActivityName = bpmnObject.get_first_activity_name(rootBPMN)
        activityOne = bpmnObject.get_activityes(rootBPMN)[1].attrib['name']
        activityTwo = bpmnObject.get_activityes(rootBPMN)[2].attrib['name']
        # generate aiml from bpmn using generated variables
        aimlObject = AIMLClassNovo()
        rootAIML = aimlObject.addCategoryInit(pattern_event_init_value, templateName)
        topicAIML = aimlObject.addTopic(rootAIML, templateName)
        aimlObject.addCategoryTopic(topicAIML, 'STEP_' + str(pattern_event_init_value).upper(), firstActivityName)
        aimlObject.addCategoryFlow(topicAIML, '*', firstActivityName, 'resultado', 'sim', 'STEP_SIM','nao', 'STEP_NAO')
        aimlObject.addCategoryTopic(topicAIML, 'STEP_SIM', activityOne)
        aimlObject.addCategoryTopic(topicAIML, 'STEP_NAO', activityTwo)
        return rootAIML

    def outputBPMNFile(self, filename, rootAIML):
        file = open(filename, 'wb')
        tree = ET.ElementTree(rootAIML)
        tree.write(file)
        file.close()


if __name__ == '__main__':
    # Integration between BPMN and AIML
    controladorNovo = ControladorNovo()
    rootAIML = controladorNovo.generateAIML('input/estudo.bpmn')
    # Generate AIML file
    controladorNovo.outputBPMNFile('output/estudo.aiml', rootAIML)
    # controladorNovo.outputBPMNFile('../../storagedepressao/categories/pizza.aiml', rootAIML)