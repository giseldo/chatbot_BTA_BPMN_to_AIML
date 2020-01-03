import xml.etree.ElementTree as ET
import os

def convert_bpmn_to_finite_state_bpmn(bpmn):

    # identificar os edges com gateway de junção e colocar em um vetor mudar os dest para a proxima destes edges task
    # cria um lista com as arestas que tem gateway de juncao
    lista_arestas_juncao = getListaArestasComGatewayJuncao(bpmn)

    # monta um dicionario com a aresta que tem gateway de juncao e a proximo vertice (que é o gateway)
    dicionario_aresta_juncao_e_prox_vertice = get_dicionario_aresta_juncao_e_prox_vertice(bpmn, lista_arestas_juncao)

    # altera o pos da aresta com juncao para o prox vertice depois do gateway
    # mas se for outro gateway procura uma proxima task ou end event
    for aresta, vertice in dicionario_aresta_juncao_e_prox_vertice.items():
        next_aresta = get_next_aresta(bpmn, vertice)
        next_node = get_node(bpmn, next_aresta.attrib['pos'])
        while next_node.tag == "exclusive_gateway":
            next_aresta = get_next_aresta(bpmn, next_node)
            next_node = get_node(bpmn, next_aresta.attrib['pos'])
        else:
            aresta.attrib['pos'] = next_aresta.attrib['pos']

    # apaga o gateway que estava apontando para a aresta
    # apaga o vertice que ligava o gateway ao proximo vertice
    for aresta, vertice in dicionario_aresta_juncao_e_prox_vertice.items():
        # remove o vertice
        try:
            bpmn.getroot().remove(vertice)
            next_aresta = get_next_aresta(bpmn, vertice)
            bpmn.getroot().remove(next_aresta)
        except ValueError:
            print('item nao existe')

    return bpmn


def get_next_aresta(bpmn, vertice):
    for aresta in bpmn.findall("edge"):
        if vertice.attrib['id'] == aresta.attrib['ant']:
            return aresta


def change_dest_from_edge(edge, new_vertice):
    edge.attrib['pos'] = new_vertice.attrib['id']


def get_next_vertice(bpmn, aresta):
    # verificar porque esta fazendo o loop em todos os elementos
    for vertice in bpmn.getroot():
        if vertice.attrib['id'] == aresta.attrib['pos']:
            return vertice


def get_node(bpmn, node_id):
    for node in bpmn.getroot():
        if node.attrib['id'] == node_id:
            return node


def get_dicionario_aresta_juncao_e_prox_vertice(bpmn, lista_arestas_juncao):
    dicionario_aresta_juncao_e_prox_vertice = {}
    for aresta in lista_arestas_juncao:
        next_vertice = get_next_vertice(bpmn, aresta)
        dicionario_aresta_juncao_e_prox_vertice[aresta] = next_vertice
    return dicionario_aresta_juncao_e_prox_vertice


def getListaArestasComGatewayJuncao(bpmn):
    lista_arestas_juncao = []
    for aresta in bpmn.findall("edge"):
        if is_aresta_juncao(bpmn, aresta):
            lista_arestas_juncao.append(aresta)
    return lista_arestas_juncao


def is_aresta_juncao(bpmn, aresta):
    for gateway in bpmn.findall("exclusive_gateway"):
        # so pesquise se a aresta apontar para um gateway
        if aresta.attrib['pos'] == gateway.attrib['id']:
            # para todas as arestas
            for aresta_inner in bpmn.findall("edge"):
                # verifique se tem mais de uma aresta apontando para o mesmo pos ( no caso gateway )
                if aresta_inner.attrib['pos'] == aresta.attrib['pos'] and aresta_inner.attrib['id'] != aresta.attrib['id']:
                    return True
    return False


def transform_bpmn_to_finite_state_bpmn(input_file_name):
    bpmn = ET.parse(input_file_name, ET.XMLParser(encoding='utf-8'))

    new_bpmn = convert_bpmn_to_finite_state_bpmn(bpmn)
    # get output file name
    list_file_name = input_file_name.split('/')
    only_last_name = list_file_name[-1]
    output_file_name = os.path.join("bpmn_finite_state/" + only_last_name)

    tree_finite_state = ET.ElementTree(new_bpmn)
    tree_finite_state.getroot().write(output_file_name)

    return output_file_name




