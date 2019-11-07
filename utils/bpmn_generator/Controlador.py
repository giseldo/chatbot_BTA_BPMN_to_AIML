from AIML_ import AIMLClass
from BPMN_ import BPMNClass
import xml.etree.ElementTree as ET


class Controlador:

    def generateAIML(self, inputBPMNFileName):
        # generate necessary variables for integration from BPMN
        bpmnObject = BPMNClass()
        rootBPMN = bpmnObject.getRootBPMNFromFile(inputBPMNFileName)
        templateName, pattern_event_init_value = bpmnObject.getTemplateName(rootBPMN)
        firstActivityName = bpmnObject.get_first_activity_name(rootBPMN)
        activityOne = bpmnObject.get_activityes(rootBPMN)[1].attrib['name']
        activityTwo = bpmnObject.get_activityes(rootBPMN)[2].attrib['name']
        # generate aiml from bpmn using generated variables
        aimlObject = AIMLClass()
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
    controlador = Controlador()
    rootAIML = controlador.generateAIML('input/carro.bpmn')
    # Generate AIML file
    controlador.outputBPMNFile('output/carro.aiml', rootAIML)
    # controlador.outputBPMNFile('../../storagedepressao/categories/ari/carro.aiml', rootAIML)