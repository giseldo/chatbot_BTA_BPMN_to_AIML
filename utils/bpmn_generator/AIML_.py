import xml.etree.ElementTree as ET

class AIMLClass:

    def addCategoryTopic(self, root, patternText, templateText):
        category = ET.SubElement(root, 'category')
        pattern = ET.SubElement(category, 'pattern')
        pattern.text = patternText
        template = ET.SubElement(category, 'template')
        template.text = templateText

    def addCategoryInit(self, pattern_event_init_value, templateName):
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

    def addTopic(self, rootAIML, templateName):
        # inicio das tags topic
        topic = ET.SubElement(rootAIML,"topic")
        topic.attrib['name'] = str(templateName).upper()
        return topic

    def addCategoryFlow(self, root, patternValue, templateValue, varname, optionKeyA, optionValueA, optionKeyB, optionValueB):
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

