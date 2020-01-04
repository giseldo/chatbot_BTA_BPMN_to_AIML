import xml.etree.ElementTree as ET
import os
import re


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


def get_arestas_from_gateway(root_bpmn, gateway):
    arestas = []
    for aresta in root_bpmn.findall("edge"):
        if aresta.attrib["ant"] == gateway.attrib["id"]:
            arestas.append(aresta)
    return arestas


def is_phase_with_variable(phrase):
    match = re.search(r"[$]\w*\w", phrase)
    return match

def get_end_out_topic(phrase):
    saida = '<think><set name="topic"></set></think>{}'.format(phrase)
    return saida

def transform_condition_if_exists(root_bpmn, pos):
    phrase = pos.attrib['nome']
    match = is_phase_with_variable(phrase)
    if match:
        variavel = match[0].replace('_', '').replace('(', '').replace(')', '').replace('$', '')
        arestas = get_arestas_from_gateway(root_bpmn, pos)
        condition_begin = '''<condition name="{}">'''.format(variavel)
        condition_li_values = ""
        for aresta in arestas:
            srai_name_task = aresta.attrib["nome"].replace('_', '').replace('(', '').replace(')', '').replace('$', '')
            srai_redirect = aresta.attrib["pos"].replace('_', '').replace('(', '').replace(')', '').replace('$', '')
            condition_li_values = condition_li_values + '<li value="{}"><srai>{}</srai></li>'.format(srai_name_task, srai_redirect)
        condition_end = '''</condition>'''
        phrase = condition_begin + condition_li_values + condition_end
    return phrase


def create_category(root_aiml, topic_name, pattern_text, template_text, that_text, srai_text, set_name, set_value):
    if topic_name is not None:
        topic = ET.SubElement(root_aiml, 'topic')
        topic.set("name", topic_name)
    category = ET.SubElement(root_aiml, 'category')
    pattern = ET.SubElement(category, 'pattern')
    pattern.text = pattern_text.upper().replace('_', '').replace('(', '').replace(')', '')
    if that_text is not None:
        that = ET.SubElement(category, 'that')
        that.text = that_text.upper().replace('?', '').replace('(', '').replace(')', '')
    template = ET.SubElement(category, 'template')
    template.text = template_text.upper() + '-'
    if set_name is not None:
        think_tag = ET.SubElement(template, 'think')
        set_tag = ET.SubElement(think_tag, 'set')
        set_tag.set('name', set_name.upper().replace('_', '').replace('(', '').replace(')', '').replace('$', ''))
        set_tag.text = set_value.upper()
    if srai_text is not None:
        srai = ET.SubElement(template, 'srai')
        srai.text = srai_text.upper().replace('_', '').replace('(', '').replace(')', '')

def get_topic_id(root_bpmn):
    for child in root_bpmn:
        if child.tag == 'edge':
            ant = get_ant_vertice(root_bpmn, child)
            if ant.tag == 'start_event':  # testar depois task ou esclusive gateway
                return ant.attrib["id"].upper().replace('_', '').replace('(', '').replace(')', '') # pegar o id do start event
    return "ID_NAO_ENCONTRADO"


def convert_bpmn_to_aiml(root_bpmn, root_aiml):
    topic = ET.SubElement(root_aiml, 'topic')
    topic.set("name",get_topic_id(root_bpmn))
    for child in root_bpmn: # refatorar utiliznado findall("edge")
        srai_text = None
        that_text = None
        topic_name = None
        pattern_text = None
        template_text = None
        set_name = None
        set_value = None
        if child.tag == 'edge':
            ant = get_ant_vertice(root_bpmn, child)
            pos = get_pos_vertice(root_bpmn, child)
            if ant.tag == 'start_event':  # testar depois task ou esclusive gateway
                pattern_text = ant.attrib['nome']
                topic_name = ant.attrib['id'].upper().replace('_', '').replace('(', '').replace(')', '')
                template_text = '<think><set name="topic">{}</set></think>{}'.format(topic_name, pos.attrib["nome"])
                if pos.tag == 'task':
                    srai_text = pos.attrib['id']
            if ant.tag == 'task' and pos.tag == 'task':
                pattern_text = ant.attrib['id']
                template_text = get_template_text_with_variable(pos.attrib['nome'])
                srai_text = pos.attrib['id']
            if pos.tag == 'end_event':
                pattern_text = ant.attrib['id']
                template_text = '<think><set name="topic"></set></think>{}'.format(pos.attrib['nome'])
                root_aiml = topic
            if ant.tag == 'task' and pos.tag == 'exclusive_gateway':
                pattern_text = ant.attrib['id']
                template_text = transform_condition_if_exists(root_bpmn, pos)
                root_aiml = topic
            if ant.tag == 'exclusive_gateway' and pos.tag == 'task':
                match_variable_gateway = is_phase_with_variable(ant.attrib["nome"])
                if match_variable_gateway:
                    pattern_text = pos.attrib['id']
                    template_text = pos.attrib['nome']
                else:
                    pattern_text = child.attrib['nome']
                    that_text = '* ' + ant.attrib['nome']
                    template_text = pos.attrib['nome']
                srai_text = pos.attrib['id']
                association_node = get_association_node(root_bpmn, ant)
                if association_node is not None:
                    text_association_node = get_node(root_bpmn, association_node.attrib['pos'])
                    set_name = text_association_node.attrib['nome']
                    set_value = child.attrib['nome']
                root_aiml = topic
            create_category(root_aiml, topic_name, pattern_text, template_text, that_text, srai_text, set_name, set_value)


def lower_case_some_tags(input_file_name, output_file_name):
    file = open(input_file_name, 'r', encoding="utf-8")
    regexp = re.compile(r'(NAME|SET|GET|CONDITION|LI VALUE|SRAI|THINK|TOPIC|&lt;|&gt;|&lt;LI|LI&gt;)')
    replacement_map = {
                        'NAME': 'name',
                        'SET':'set',
                        'GET': 'get',
                        'CONDITION': 'condition',
                        'LI VALUE': 'li value',
                        'SRAI': 'srai',
                        'THINK': 'think',
                        'TOPIC': 'topic',
                        '&lt;LI': '<li',
                        'LI&gt;': 'li>',
                        '&lt;': '<',
                        '&gt;': '>',
                       }  # a dict to map a character to the replacement value.
    text = regexp.sub(lambda match: replacement_map[match.group(0)], file.read())
    file = open(output_file_name, 'w', encoding="UTF-8")
    file.write(text)


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

    # coloca algumas tags em minusculos
    lower_case_some_tags(output_file_name_xml, output_file_name_aiml)
