## Título
Ari: um chatbot em AIML com fluxo de dialogo escrito em BPMN.

## Resumo
Chatbots são programas de computador onde um ser humano conversa 
com o programa utilizando linguagem natural.
Existem diversas tecnologias associadas a construção de 
chatterbots  uma que se destaca é o AIML.
Desenhar fluxos em AIML é trabalhoso e por vezes 
não intuitivo devido a características intrínsecas do XML e do AIML.
Construir fluxos utilizando uma linguagem visual é intuitivo. 
Existe uma linguagem que define os componentes visuais e
 a sua especificação em XML é utilizada para mapeamento de processos de negócio.
É possível mapear a notação BPMN em AIML e aproveitar todos os recursos
visuais oferecidos por uma linguagem de notação visual como o BPMN. 
Foi desenvolvido um módulo em python que converte um diagrama 
BPMN em AIML. Dois estudos de caso foram implementados, um que 
fala sobre depressão e um que ensina ética. A conversão do fluxo de BPMN para AIML dura alguns segundos. Logo é possível construir vários fluxos. O resultado esperado é disseminar o uso de AIML por uma quantidade cada vez maior de pessoas.

## Introdução

Chatbots são programas de computador que conversam em linguagem natural com um ser humano.

BPMN é uma linguagem para mapeamento de processos de negócio.

O problema é que construir diagramas em AIML é difícil.

## Objetivo 

### Principal
Desenhar fluxos de diálogo em AIML a partir de diagramas BPMN para que a construção de chatbots
seja mais intuitiva. 

### Secundário

Desenvolver uma ferramenta para converter os fluxos diálogos.
Desenvolver um chatbot como prova de conceito.

## Estudo de caso

Foi desenvolvido um estudo de caso sobre depressão baseado no trabalho de BECK onde todos os diálogos foram mapeados em BPMN.

## Arquitetura

Python 3.7, program-y, xml.etree.elementtree, aiml 2.0

## Resultados

Usuários que conheciam e não conheciam AIML construiram fluxos de diálogo e os carregaram em um chatbot.

## Referências

- TURING, ELIZA, ALICE, AIML, PROGRAM-Y

## Instalação

- Baixe o projeto, instale as dependências e execute:

$git clone https://github.com/giseldo/chatbot_ari_bpmn_to_aiml.git 

$pip install -r requirements

$python.exe client_web.py  (recomendo o pycharm)

## Próximos passos
- Acesse a wiki do projeto [Wiki](https://github.com/giseldo/chatbot_ari_bpmn_to_aiml/wiki)
- Veja alguns exemplos de diagrama em [Exemplos](https://github.com/giseldo/chatdepressao/tree/master/exemplos)
- Faça um diagrama bpmn no site http://bpmn.io ou no [Bizagi Modeler](https://www.bizagi.com/pt)
- Carregue o diagrama no seu chatbot.

## Contato 

Se está com dúvidas ou quer participar do projeto entre em contato. Respondo rapidamente.

giseldo@gmail.com

Skype: giseldo

![tela do chatbot](./tela_chatbot.png)

![Diagrama BPM](./viewer.png)

