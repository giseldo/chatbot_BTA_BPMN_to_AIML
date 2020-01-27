## Título | Title

Arichatbot: Um chatbot em AIML com sua base de conhecimento escrito em BPMN para uso em fluxo de dialogo.
Arichatbot: An AIML chatbot with its knowledge base written in BPMN for use in a dialogue flow.

## Resumo | Resume

Chatbots são programas de computador onde um ser humano conversa com o programa utilizando linguagem natural.
Existem diversas tecnologias associadas a construção de chatterbots  uma que se destaca é o AIML.
Desenhar fluxos em AIML é trabalhoso e por vezes não intuitivo devido a características intrínsecas do XML e do AIML.
Mas construir fluxos de diálogos utilizando uma linguagem visual é bem mais intuitivo. 
Existe uma linguagem utilizada para mapeamento de processos de negócio chamada BPMN que define componentes visuais.
É possível converter a notação BPMN em AIML e aproveitar todos os recursos visuais oferecidos por uma linguagem de notação visual como o BPMN. 
Para validar esta hipótese foi desenvolvido um aplicativo em python que converte um diagrama BPMN em AIML. 
Um estudo de caso foi implementado onde todos os dialogos de um chatbot que fala sobre depressão, desenvolvido em chatscript, foram mapeados em BPMN. 
Um resultado encontrado foi uma velocidade maior para desenhar os fluxos de dialógo de um chatbot em BPMN do que escrever em AIML. 
Um outro resultado foi permitir que pessoas que não conheçam AIML escrevam os fluxos de diálogos para seus chatbots.
Indiretamente espera-se disseminar o uso de chatbots em AIML por uma quantidade cada vez maior de pessoas.

Chatbots are computer programs where a human being talks to the program using natural language.
There are several technologies associated with the construction of chatterbots, one that stands out is AIML.
Designing flows in AIML is laborious and sometimes not intuitive due to the intrinsic characteristics of XML and AIML.
But building dialog flows using a visual language is much more intuitive.
There is a language used for mapping business processes called BPMN that defines visual components.
It is possible to convert BPMN notation to AIML and take advantage of all the visual features offered by a visual notation language such as BPMN.
To validate this hypothesis, a python application was developed that converts a BPMN diagram to AIML.
A case study was implemented where all the dialogues of a chatbot that talks about depression, developed in chatscript, were mapped in BPMN.
One result found was a faster speed to draw the dialog flows of a chatbot in BPMN than to write in AIML.
Another result was to allow people who don't know AIML to write the dialogue flows for their chatbots.
Indirectly it is expected to spread the use of chatbots in AIML to an increasing number of people.

## Instalação | Installation

$ git clone https://github.com/giseldo/chatbot_ari_bpmn_to_aiml.git 

$ pip install -r requirements

$ python.exe client_web.py  (pycharm recomended)

## Arquitetura | Arquitecture

Python 3.7, program-y, xml.etree.elementtree, aiml 2.0, BPMN 2.0

## Próximos passos | Usage

- Make a diagram following the restrictions and premises below. You can use [http://bpmn.io](https://www.bizagi.com/pt) or [Bizagi Modeler](https://www.bizagi.com/pt)

- See some [Examples](https://github.com/giseldo/chatdepressao/tree/master/exemplos)

- Load the BPMN diagram in a chatbot that supports AIML. This project come with a bundle chatbot namede ARI that use program-y. 

- You can acess the [Wiki](https://github.com/giseldo/chatbot_ari_bpmn_to_aiml/wiki) of the project for more informations.


## Restriction and premisse

in progress

## Contato | contact

If you are in doubt, want to participate in the project, found a bug or even found the idea interesting contact us or open an issue, this will help the project a lot.
 
e-mail: giseldo@gmail.com
skype: giseldo

![tela do chatbot](./tela_chatbot.png)

![Diagrama BPM](./viewer.png)

