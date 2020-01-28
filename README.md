## BPMN to AIML. Draw a dialogue flow in BPMN for use in AIML chatbots.

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

## Usage

- Make a BPMN diagram following the restrictions and premises below. For this you can use [http://bpmn.io](https://www.bizagi.com/pt) or [Bizagi Modeler](https://www.bizagi.com/pt)

- See some [Examples](https://github.com/giseldo/chatdepressao/tree/master/exemplos) if necessary.

- Load the BPMN diagram in a chatbot that supports AIML. This project come with a bundle chatbot that use program-y. 

- You can acess the [Wiki](https://github.com/giseldo/chatbot_ari_bpmn_to_aiml/wiki) of the project for more informations.

## Restriction and premisse

in progress

## Installation

$ git clone https://github.com/giseldo/chatbot_ari_bpmn_to_aiml.git 

$ pip install -r requirements

$ python.exe client_web.py  (pycharm recomended)

## contact

If you are in doubt, want to participate in the project, found a bug or even found the idea interesting contact us or open an issue, this will help the project a lot.
 
e-mail: giseldo@gmail.com

skype: giseldo

![tela do chatbot](./tela_chatbot.png)

![Diagrama BPM](./viewer.png)

