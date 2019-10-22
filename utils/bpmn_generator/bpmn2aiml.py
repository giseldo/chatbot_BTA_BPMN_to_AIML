import xml.etree.ElementTree as ET

templateName = ""

treeInput = ET.parse("input/pmbok.bpmn")

rootDefinition = treeInput.getroot()
definitionTagName = rootDefinition.tag
# templateName = process.ID
# pattern_event_init_value = startEvent.Name
for process in rootDefinition:
    if "process" in process.tag:
        templateName = process.attrib['id']
        for start in process:
            if "startEvent" in start.tag:
                pattern_event_init_value = startEventName = start.attrib['name']


def get_init_id(root):
    seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}startEvent"
    for startEvent in root.findall(seach_tag):
        return startEvent.attrib['id']


# get first activity
def get_first_activity_name(root):
    seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"
    for sequenceFlow in root.findall(seach_tag):
        if sequenceFlow.attrib['sourceRef'] == get_init_id(root):
            next_task_id = sequenceFlow.attrib['targetRef']

    seach_tag_service_task = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask"
    for serviceTask in root.findall(seach_tag_service_task):
        if serviceTask.attrib['id'] == next_task_id:
            return serviceTask.attrib['name']


# get first activity
def get_sequeceFlows(root):
    seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"
    for sequenceFlow in root.findall(seach_tag):
        return sequenceFlow
# print(get_sequeceFlows(rootDefinition))

# get first activity
def get_activityes(root):
    seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask"
    return root.findall(seach_tag)
# print(get_activityes(rootDefinition))



def addCategoryTopic(root, patternText, templateText):
    category = ET.SubElement(root, 'category')
    pattern = ET.SubElement(category, 'pattern')
    pattern.text = patternText
    template = ET.SubElement(category, 'template')
    template.text = templateText


# inicio das tags
aiml = ET.Element('aiml')
category = ET.SubElement(aiml, 'category')
pattern = ET.SubElement(category, 'pattern')
pattern.text = str(pattern_event_init_value).upper()
template = ET.SubElement(category, 'template')
think = ET.SubElement(template, 'think')
set = ET.SubElement(think, 'set')
set.text = str(templateName).upper()
set.attrib = {'name': 'topic'}
srai = ET.SubElement(template,'srai')
srai.text = 'STEP_' + str(pattern_event_init_value).upper()


# inicio das tags topic
topic = ET.SubElement(aiml,"topic")
topic.attrib['name'] = str(templateName).upper()


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


addCategoryTopic(topic, 'STEP_' + str(pattern_event_init_value).upper(), get_first_activity_name(rootDefinition))
addCategoryFlow(topic, '*', get_first_activity_name(rootDefinition), 'resultado', 'sim', 'STEP_SIM','nao', 'STEP_NAO')
addCategoryTopic(topic ,'STEP_SIM', get_activityes(rootDefinition)[1].attrib['name'])
addCategoryTopic(topic ,'STEP_NAO', get_activityes(rootDefinition)[2].attrib['name'])

file = open('output/pmbok.aiml', 'wb')
tree = ET.ElementTree(aiml)
tree.write(file)
file.close()

file = open('../../storagedepressao/categories/ari/pmbok.aiml', 'wb')
tree = ET.ElementTree(aiml)
tree.write(file)
file.close()
