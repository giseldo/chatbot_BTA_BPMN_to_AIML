import re

def get_template_text_with_variable(phrase):
    matches = re.findall(r"[$]\w*\w", phrase)
    for match in matches:
         variavel = match.replace('_', '').replace('(', '').replace(')', '').replace('$', '')
         phrase = phrase.replace(match, '<get name="' + variavel + '" />')
    return phrase


def main():
    saida = get_template_text_with_variable("isto é uma $var teste e outra $test tambem")
    print(saida)


main()