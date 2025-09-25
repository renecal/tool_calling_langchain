from typing import List, Union

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool, tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from callbacks import AgentCallbackHandler  # Importa el manejador de callbacks personalizado

load_dotenv()  # Carga las variables de entorno desde el archivo .env


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")  # Muestra el texto recibido para depuración
    text = text.strip("'\n").strip('"')  # Elimina comillas y saltos de línea del texto
    return len(text)  # Retorna la longitud del texto


def main():
    print("Hello from react-langchain!")  # Mensaje de bienvenida

    tools = [get_text_length]  # Define la lista de herramientas disponibles

    # Crea el prompt para tool calling
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the following tools to answer questions."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # Inicializa el modelo de lenguaje de Google Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        callbacks=[AgentCallbackHandler()]
    )

    # Crea el agente de tool calling
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Ejecuta el agente con la pregunta
    result = agent_executor.invoke({"input": "What is the length of the word: DOG"})
    print(result)


if __name__ == "__main__":
    main()  # Ejecuta la función principal
