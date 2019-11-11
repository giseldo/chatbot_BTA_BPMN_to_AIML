import xml.etree.ElementTree as ET


############################# LOAD FILE #############################


def getRootBPMNFromFile(inputFileName):
    treeInput = ET.parse(inputFileName)
    rootBPMN = treeInput.getroot()
    return rootBPMN


def getTemplateName(rootBPMN):
    for process in rootBPMN:
        if "process" in process.tag:
            templateName = process.attrib['id']
            for start in process:
                if "startEvent" in start.tag:
                    pattern_event_init_value = start.attrib['name']
    return templateName, pattern_event_init_value


def get_init_id(rootBPMN):
    seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}startEvent"
    for startEvent in rootBPMN.findall(seach_tag):
        return startEvent.attrib['id']


# get first activity
def get_first_activity_name(rootBPMN):
    seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"
    for sequenceFlow in rootBPMN.findall(seach_tag):
        if sequenceFlow.attrib['sourceRef'] == get_init_id(rootBPMN):
            next_task_id = sequenceFlow.attrib['targetRef']

    seach_tag_service_task = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask"
    for serviceTask in rootBPMN.findall(seach_tag_service_task):
        if serviceTask.attrib['id'] == next_task_id:
            return serviceTask.attrib['name']


# get first activity
def get_sequeceFlows(rootBPMN):
    seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"
    for sequenceFlow in rootBPMN.findall(seach_tag):
        return sequenceFlow
# print(get_sequeceFlows(rootDefinition))

# get first activity
def get_activityes(rootBPMN):
    seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask"
    return rootBPMN.findall(seach_tag)
# print(get_activityes(rootDefinition))


############################################### CREATE FILE #############################


def addCategoryTopic(root, patternText, templateText):
    category = ET.SubElement(root, 'category')
    pattern = ET.SubElement(category, 'pattern')
    pattern.text = patternText
    template = ET.SubElement(category, 'template')
    template.text = templateText


def addCategoryInit(pattern_event_init_value, templateName):
    # inicio das tags
    rootAIML = ET.Element('aiml')
    category = ET.SubElement(rootAIML, 'category')
    pattern = ET.SubElement(category, 'pattern')
    pattern.text = str(pattern_event_init_value).upper()
    template = ET.SubElement(category, 'template')
    think = ET.SubElement(template, 'think')
    set = ET.SubElement(think, 'set')
    set.text = str(templateName).upper()
    set.attrib = {'name': 'topic'}
    srai = ET.SubElement(template,'srai')
    srai.text = 'STEP_' + str(pattern_event_init_value).upper()

    return rootAIML


def addTopic(rootAIML, templateName):
    # inicio das tags topic
    topic = ET.SubElement(rootAIML,"topic")
    topic.attrib['name'] = str(templateName).upper()
    return topic


def addCategoryFlow(root, patternValue, templateValue, varname, optionKeyA, optionValueA, optionKeyB, optionValueB):
    # fluxos
    category = ET.SubElement(root, 'category')
    pattern = ET.SubElement(category, 'pattern')
    pattern.text = patternValue
    that = ET.SubElement(category, 'that')
    that.text = templateValue
    templatetopic1 = ET.SubElement(category, 'template')
    thinktopic1 = ET.SubElement(templatetopic1, 'think')
    settopic1 = ET.SubElement(thinktopic1, 'set')
    settopic1.attrib = {'name': varname} # verificar valor da variavel resultado
    startopic1 = ET.SubElement(settopic1, 'star')
    conditiontopic1 = ET.SubElement(templatetopic1, 'condition')
    conditiontopic1.attrib = {'name': varname}
    litopic1 = ET.SubElement(conditiontopic1, 'li')
    litopic1.attrib = {'value': optionKeyA} # verificar
    litopic2 = ET.SubElement(conditiontopic1, 'li')
    litopic2.attrib = {'value': optionKeyB}
    # colocar em um loop
    sraitopic1 = ET.SubElement(litopic1, 'srai')
    sraitopic1.text =  optionValueA
    sraitopic2 = ET.SubElement(litopic2, 'srai')
    sraitopic2.text = optionValueB


def outputBPMNFile(filename, rootAIML):
    file = open(filename, 'wb')
    tree = ET.ElementTree(rootAIML)
    tree.write(file)
    file.close()

### controlador

def generateAIML(rootBPMN):
    ### generate necessary variables for integration
    templateName, pattern_event_init_value = getTemplateName(rootBPMN)
    firstActivityName = get_first_activity_name(rootBPMN)
    activityOne = get_activityes(rootBPMN)[1].attrib['name']
    activityTwo = get_activityes(rootBPMN)[2].attrib['name']
    ## generate aiml from bpmn using generated variables
    rootAIML = addCategoryInit(pattern_event_init_value, templateName)
    topicAIML = addTopic(rootAIML, templateName)
    addCategoryTopic(topicAIML, 'STEP_' + str(pattern_event_init_value).upper(), firstActivityName)
    addCategoryFlow(topicAIML, '*', firstActivityName, 'resultado', 'sim', 'STEP_SIM','nao', 'STEP_NAO')
    addCategoryTopic(topicAIML, 'STEP_SIM', activityOne)
    addCategoryTopic(topicAIML, 'STEP_NAO', activityTwo)
    return rootAIML

### principal

if __name__ == '__main__':
    ### Carrega BPMN
    rootBPMN = getRootBPMNFromFile('input/carro.bpmn')
    ### Integration between BPMN and AIML
    rootAIML = generateAIML(rootBPMN)
    ### Generate AIML file
    outputBPMNFile('output/carro.aiml', rootAIML)
    outputBPMNFile('../../storagedepressao/categories/ari/carro.aiml', rootAIML)
