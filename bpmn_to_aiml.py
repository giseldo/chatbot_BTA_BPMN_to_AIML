import xml.etree.ElementTree as ET
import os
import re


def create_category(root_aiml, pattern_text, template_text, that_text, srai_text, set_name, set_value):
    category = ET.SubElement(root_aiml, 'category')
    pattern = ET.SubElement(category, 'pattern')
    pattern.text = pattern_text.upper()

    if that_text is not None:
        that = ET.SubElement(category, 'that')
        that.text = that_text.upper().replace('?', '').replace('(', '').replace(')', '')
    template = ET.SubElement(category, 'template')
    template.text = template_text.upper() + '-'

    if set_name is not None:
        think_tag = ET.SubElement(template, 'think')
        set_tag = ET.SubElement(think_tag, 'set')
        set_tag.set('name', set_name.upper().replace('_', '').replace('(', '').replace(')', '').replace('$', ''))
        # set_tag.text = set_value.upper().replace('_', '').replace('(', '').replace(')', '')
        set_tag.text = set_value.upper()

    if srai_text is not None:
        srai = ET.SubElement(template, 'srai')
        srai.text = srai_text.upper().replace('_', '').replace('(', '').replace(')', '')


def get_next_vertice(bpmn_root, aresta):
    # verificar porque esta fazendo o loop em todos os elementos  ideal seria somente em tasks e gateway e talvez start_event
    for vertice in bpmn_root:
        if vertice.attrib['id'] == aresta.attrib['pos']:
            return vertice


def get_next_aresta(bpmn, vertice):
    for aresta in bpmn.findall("edge"):
        if vertice.attrib['id'] == aresta.attrib['ant']:
            return aresta


def get_ant_vertice(root_bpmn, aresta):
    for vertice in root_bpmn:
        if vertice.attrib['id'] == aresta.attrib['ant']:
            return vertice


def get_pos_vertice(root_bpmn, aresta):
    for vertice in root_bpmn:
        if vertice.attrib['id'] == aresta.attrib['pos']:
            return vertice


def get_node(root_bpmn, node_id):
    for node in root_bpmn:
        if node.attrib['id'] == node_id:
            return node
    return None


def get_association_node(root_bpmn, gateway):
    for node in root_bpmn:
        if node.tag == "association":
            if node.attrib['ant'] == gateway.attrib['id']:
                return node
    return None


def get_template_text_with_variable(phrase):
    match = re.search(r"[$]\w*\w", phrase)
    if match:
        variavel = match[0].replace('_', '').replace('(', '').replace(')', '').replace('$', '')
        phrase = phrase.replace(match[0], '<get name="' + variavel + '" />')
        return phrase
    return phrase


def convert_bpmn_to_aiml(root_bpmn, root_aiml):
    for child in root_bpmn:
        srai_text = None
        that_text = None
        pattern_text = None
        template_text = None
        set_name = None
        set_value = None
        get_name = None
        if child.tag == 'edge':
            ant = get_ant_vertice(root_bpmn, child)
            pos = get_pos_vertice(root_bpmn, child)
            if ant.tag == 'start_event' and pos.tag == 'task':
                pattern_text = ant.attrib['nome']
                template_text = pos.attrib['nome']
                srai_text = pos.attrib['id']
            if ant.tag == 'start_event' and pos.tag == 'exclusive_gateway':
                pattern_text = ant.attrib['nome']
                template_text = pos.attrib['nome']
            if ant.tag == 'task' and pos.tag == 'task':
                pattern_text = ant.attrib['id'].replace('_', '').replace('(', '').replace(')', '')
                template_text = get_template_text_with_variable(pos.attrib['nome'])
                srai_text = pos.attrib['id']
            if ant.tag == 'task' and pos.tag == 'end_event':
                pattern_text = ant.attrib['id'].replace('_', '').replace('(', '').replace(')', '')
                template_text = pos.attrib['nome']
            if ant.tag == 'task' and pos.tag == 'exclusive_gateway':
                pattern_text = ant.attrib['id'].replace('_', '').replace('(', '').replace(')', '')
                template_text = pos.attrib['nome']
            if ant.tag == 'exclusive_gateway' and pos.tag == 'task':
                pattern_text = child.attrib['nome']
                that_text = '* ' + ant.attrib['nome']
                template_text = pos.attrib['nome']
                srai_text = pos.attrib['id']
                # get node text for think and set name
                association_node = get_association_node(root_bpmn, ant)
                if association_node is not None:
                    text_association_node = get_node(root_bpmn, association_node.attrib['pos'])
                    set_name = text_association_node.attrib['nome']
                    set_value = child.attrib['nome']

            create_category(root_aiml, pattern_text, template_text, that_text, srai_text, set_name, set_value)


def transform_bpmn_to_aiml(input_file_name):

    tree_bpmn = ET.parse(input_file_name, ET.XMLParser(encoding='utf-8'))

    root_bpmn = tree_bpmn.getroot()

    element_aiml = ET.Element('aiml')
    tree_aiml = ET.ElementTree(element_aiml)
    root_aiml = tree_aiml.getroot()

    convert_bpmn_to_aiml(root_bpmn, root_aiml)

    # get output file name
    list_file_name = input_file_name.split('/')
    only_last_name = list_file_name[-1]

    output_file_name_xml = os.path.join("categories/" + only_last_name + '.xml')
    output_file_name_aiml = os.path.join("categories/" + only_last_name + '.aiml')

    # escreve o arquivo
    tree_aiml.write(output_file_name_xml, encoding="UTF-8")

    # recria o arquivo convertendo os caracteres < >
    file = open(output_file_name_xml, 'r', encoding="utf-8")
    regexp = re.compile(r'(&lt;|&gt;|GET NAME)')  # here we are making a regex to catch either the character '<' or '>'
    replacement_map = {'&lt;':'<', '&gt;':'>', 'GET NAME':'get name' }  # a dict to map a character to the replacement value.
    text = regexp.sub(lambda match: replacement_map[match.group(0)], file.read())
    file = open(output_file_name_aiml, 'w', encoding="UTF-8")
    file.write(text)




