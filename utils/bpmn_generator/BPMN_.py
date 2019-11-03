import xml.etree.ElementTree as ET

class BPMNClass:

    def getRootBPMNFromFile(self, inputFileName):
        treeInput = ET.parse(inputFileName)
        rootBPMN = treeInput.getroot()
        return rootBPMN

    def getTemplateName(self, rootBPMN):
        for process in rootBPMN:
            if "process" in process.tag:
                templateName = process.attrib['id']
                for start in process:
                    if "startEvent" in start.tag:
                        pattern_event_init_value = start.attrib['name']
        return templateName, pattern_event_init_value

    def get_init_id(self, rootBPMN):
        seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}startEvent"
        for startEvent in rootBPMN.findall(seach_tag):
            return startEvent.attrib['id']

    def get_first_activity_name(self, rootBPMN):
        seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"
        for sequenceFlow in rootBPMN.findall(seach_tag):
            if sequenceFlow.attrib['sourceRef'] == self.get_init_id(rootBPMN):
                next_task_id = sequenceFlow.attrib['targetRef']

        seach_tag_service_task = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask"
        for serviceTask in rootBPMN.findall(seach_tag_service_task):
            if serviceTask.attrib['id'] == next_task_id:
                return serviceTask.attrib['name']

    def get_sequeceFlows(self, rootBPMN):
        seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"
        for sequenceFlow in rootBPMN.findall(seach_tag):
            return sequenceFlow

    def get_activityes(self, rootBPMN):
        seach_tag = "./{http://www.omg.org/spec/BPMN/20100524/MODEL}process/{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask"
        return rootBPMN.findall(seach_tag)