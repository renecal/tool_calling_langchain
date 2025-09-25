from typing import List, Union

from dotenv import load_dotenv
from langchain.agents.output_parsers.react_single_input import \
    ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool, render_text_description, tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.format_scratchpad import format_log_to_str
from callbacks import AgentCallbackHandler  # Importa el manejador de callbacks personalizado

load_dotenv()  # Carga las variables de entorno desde el archivo .env


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")  # Muestra el texto recibido para depuración
    text = text.strip("'\n").strip('"')  # Elimina comillas y saltos de línea del texto
    return len(text)  # Retorna la longitud del texto


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    # Busca un tool por su nombre en la lista de tools
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")  # Lanza un error si no se encuentra


def main():
    print("Hello from react-langchain!")  # Mensaje de bienvenida

    tools = [get_text_length]  # Define la lista de herramientas disponibles

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """

    # Crea el prompt usando la plantilla y los nombres de las herramientas
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    # Inicializa el modelo de lenguaje de Google Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        callbacks=[AgentCallbackHandler()]
    ).bind(
        stop=["\nObservation", "Observation"],
    )

    # Inicializa el scratchpad intermedio (vacío al inicio)
    intermediate_steps = []

    # Define el agente combinando el input, el prompt, el modelo y el parser de salida
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        } 
        | prompt 
        | llm 
        | ReActSingleInputOutputParser()
    )
    agent_step = ""

    while not isinstance(agent_step, AgentFinish):
        # Invoca al agente con una pregunta de ejemplo y define el scratchpad para las respuestas intermedias
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {
                "input": "What is the length of the word: DOG",
                "agent_scratchpad": intermediate_steps
            }
        )
        print(f"{agent_step=}")  # Muestra el resultado del agente

        # Si el agente devuelve una acción, ejecuta la herramienta correspondiente
        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool  # Obtiene el nombre de la herramienta a usar
            tool_to_use = find_tool_by_name(tools, tool_name)  # Busca la herramienta por nombre
            tool_input = agent_step.tool_input  # Obtiene el input para la herramienta

            observation = tool_to_use.func(str(tool_input))  # Ejecuta la herramienta con el input
            print(f"{observation=}")  # Muestra la observación (resultado de la herramienta)
            intermediate_steps.append((agent_step, str(observation)))  # Registra el paso intermedio

    # Muestra el resultado final del agente
    print(agent_step)
    print('\n')
    print('\n')

    # Si el agente devuelve un resultado final, lo muestra
    if isinstance(agent_step, AgentFinish):
        print('\n')
        print("### AgentFinish ###")
        print(agent_step.return_values) # Muestra los valores de retorno del agente


if __name__ == "__main__":
    main()  # Ejecuta la función principal
