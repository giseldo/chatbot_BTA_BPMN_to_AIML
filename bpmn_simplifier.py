import lxml.etree as ET
import os


def transform_bpmn_to_simple_bpmn(file_name_input):

    path = os.path.join(file_name_input)
    caminho_absoluto = os.path.abspath(path)

    dom = ET.parse(caminho_absoluto, ET.XMLParser(encoding='utf-8'))
    xslt = ET.parse("xslt/xslt_bpmn_io.xsl")
    transform = ET.XSLT(xslt)
    new_dom = transform(dom)

    base_name = os.path.basename(caminho_absoluto)

    output_file_name = os.path.join("bpmn_simplified/" + base_name)

    path_saida = os.path.join(output_file_name)
    caminho_absoluto_saida = os.path.abspath(path_saida)

    new_dom.write(caminho_absoluto_saida)

    return output_file_name



