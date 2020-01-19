## Título
Ari: um chatbot em AIML com fluxo de dialogo escrito em BPMN.

## Resumo
Chatbot são programas de computador onde um ser humano conversa 
com o programa utilizando linguagem natural.
Existem diversas tecnologias associadas a construção de 
chatterbots  uma que se destaca é o AIML.
Desenhar fluxos em AIML é trabalhoso e por vezes 
não intuitivo devido a caracteristicas intrísicas do XML e do AIML.
Contruir fluxos utilizando uma linguagem visual é intuitivo. 
Existe uma linguagem que define os componentes visuais e
 a sua especificação em XML é utilizada para mapeamento de processos de negócio.
É possível mapear a notação BPMN em AIML e aproveitar todos os recursos
visuais oferecidos por uma linguagem de notação visual como o BPMN. 
Foi desenvolvido um módulo em python que converte um diagrama 
BPMN em AIML. Dois estudos de caso foram implementados, um que 
fala sobre depressão e um que ensina ética. A conversão do fluxo de BPMN para AIML dura alguns segundos. Logo é possível construir vários fluxos. O resultado esperado é disseminar o uso de AIML por uma quantidade cada vez maior de pessoas.

## Introdução

Chatbots são programas de computador.

BPMN é uma linguagem de mapeamento de processos.

O problema é que construir diagramas em AIML é difícil.

### Objetivo Principal

Desenhar fluxos de diálogo em AIML a partir do BPMN para que a construção de chatbots
seja mais intuitiva. 

### Objetivo Secundário

Desenvolver uma ferramenta visual para construção de fluxo de 
diálogos.

## Estudo de caso

Foi desenvolvido um estudo de caso sobre depressão baseado no trabalho de BECK.

## Arquitetura

Python 3.7, program-y, xml.etree.elementtree, aiml 2.0

## Resultados

O chatbot foi apresentado a turma de alunos que testaram o aplicativo.

## Referências

- TURING
- ELIZA
- ALICE
- AIML
- PROGRAM-Y

## Instalação

- Baixe o projeto e instale as depedências

$git clone https://github.com/giseldo/chatbot_ari_bpmn_to_aiml.git 

$pip install -r requirements
- Execute o arquivo cliente_web.py
- Veja alguns exemplos de diagrama em https://github.com/giseldo/chatdepressao/tree/master/exemplos/inicio
- Faça um diagrama bpmn no site http://bpmn.io
- Carrege o diagrama no chatbot.

## Contato 

Está com dúvidas ou quer participar do projeto entre em contato comigo, responderei todas as mensagens.

giseldo@gmail.com

Skype: giseldo

![tela](./tela_chatbot.png)


