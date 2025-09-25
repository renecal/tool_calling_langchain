# Rama Tool Calling 

## Actualizar e instalar dependencias básicas

```bash
sudo apt update
sudo apt upgrade python3
python3 --version
sudo apt install python3-pip
sudo apt install python3-venv
pip3 freeze
```

## Instalar manejador de paquetes y entorno `uv`

```bash
pip3 install uv
uv pip install -r pyproject.toml   # Para instalar dependencias si se clona la rama en otro PC
uv --help
```

## Iniciar uv y agregar dependencias

```bash
uv init
uv add langchain
```

## Instalar langchain, openai y/o google gemini

```bash
uv add langchain-openai
uv add python-dotenv black isort
uv add -U langchain-google-genai
```

## Entendiendo las iteraciones 
En LangChain, las iteraciones se utilizan para la ejecución de agentes que requieren múltiples pasos para llegar a una respuesta final. Esto se debe a que un agente es un modelo de lenguaje que razona sobre qué acciones tomar, y cada acción, como usar una herramienta o hacer una búsqueda, es un paso en un ciclo de "pensar, actuar, observar".

El resultado de la primera invocación (hasta antes de Observation) se obtiene porque representa el primer paso del agente: el pensamiento inicial y la acción que decide tomar. La estructura de un agente se puede ver como:

    Thought (Pensamiento): El agente analiza la entrada y determina el siguiente paso.

    Action (Acción): El agente selecciona una herramienta a usar (como una búsqueda en la web).

    Action Input (Entrada de la Acción): Proporciona la entrada para la herramienta seleccionada.

    Observation (Observación): Este es el resultado de la acción. Es lo que sucede después de que la herramienta se ha ejecutado.

Por lo tanto, en la primera invocación, obtienes el Thought, Action, y Action Input porque son la salida del modelo en un solo paso. La Observation es el resultado de la acción, que aún no ha ocurrido. El ciclo de iteración continúa, usando la Observation como entrada para el siguiente paso del agente hasta que se alcanza la respuesta final.

Proceso iterativo del agente:

    Paso 1:

        Entrada: ¿Cuál es el clima en París?

        Modelo de lenguaje: Thought: Necesito saber el clima, usaré la herramienta de búsqueda. Action: 'search', Action Input: 'clima en París'.

        Salida de la primera invocación: Thought, Action, Action Input.

    Paso 2:

        Se ejecuta la herramienta search con la entrada 'clima en París'.

        Se obtiene la Observation: 'El clima en París es 15°C y soleado'.

        El agente usa esta Observation como entrada para el siguiente paso.

    Paso 3 (iteración 2):

        Entrada: El clima en París es 15°C y soleado.

        Modelo de lenguaje: Thought: Ya tengo la información, puedo dar la respuesta. Final Answer: El clima en París es 15°C y soleado.

        Salida final: La respuesta completa.

Este ciclo Thought/Action -> Observation se repite hasta que el agente considera que tiene la información suficiente para generar la respuesta final. Es la base de los agentes de cadena de pensamiento (ReAct) en LangChain.

## Function Calling vs ReAct
Function Calling y ReAct son dos enfoques diferentes para interactuar con modelos de lenguaje en LangChain, cada uno con sus propias características y casos de uso.

### Function Calling (Tool calling)
Function Calling o tool calling se basa en la idea de que el modelo de lenguaje puede "llamar" a funciones específicas con entradas definidas. Este enfoque es útil cuando se necesita realizar tareas concretas y bien definidas, como buscar información en una base de datos o realizar cálculos. En este caso, el modelo actúa más como un orquestador que dirige el flujo de trabajo hacia funciones específicas. Function Calling es ideal para escenarios donde las acciones son predecibles y el modelo puede beneficiarse de la estructura y precisión que ofrecen las funciones definidas.


### ReAct
Por otro lado, ReAct (Reasoning and Acting) se centra en el razonamiento del modelo sobre qué acciones tomar en función de la entrada del usuario y el contexto. Este enfoque es más flexible y permite al modelo adaptarse a situaciones cambiantes, utilizando un ciclo de pensamiento que incluye la observación de resultados intermedios y la adaptación de acciones futuras en consecuencia. ReAct es especialmente útil en escenarios donde se requiere un alto grado de interacción y adaptación, como en diálogos complejos o tareas de múltiples pasos.

En resumen, mientras que Function Calling es más adecuado para tareas específicas y bien definidas, ReAct ofrece una mayor flexibilidad y capacidad de adaptación en situaciones más complejas.

| Característica | Function Calling | ReAct Prompting |
| :--- | :--- | :--- |
| **Definición** | Un mecanismo pre-entrenado que permite a un LLM identificar cuándo y cómo llamar a una función externa basándose en el lenguaje natural. El modelo devuelve una **llamada a función estructurada** (ej. JSON) que el desarrollador debe ejecutar. | Una técnica de *prompt engineering* que guía al LLM a "pensar" y "actuar" de manera secuencial. El modelo genera un **flujo de texto libre** que incluye un razonamiento explícito (`Thought`), la acción a tomar (`Action`) y la entrada para la acción (`Action Input`). |
| **Mecanismo** | Es una capacidad intrínseca del modelo, a menudo optimizada durante el pre-entrenamiento. El modelo "sabe" que debe generar un JSON en respuesta a una solicitud que requiere una herramienta. | Es una técnica de prompting que se implementa a nivel de la instrucción. Se le pide al modelo que siga un formato específico en su respuesta (por ejemplo, `Pensamiento: ... Acción: ... Entrada de acción: ...`). |
| **Control y flexibilidad** | Generalmente más **simple y directo** para tareas específicas. El desarrollador tiene menos control sobre el proceso de razonamiento interno del modelo. | Ofrece **mayor control y flexibilidad**. El desarrollador puede ver y modificar el razonamiento del modelo, lo que lo hace ideal para tareas complejas o de múltiples pasos. |
| **Casos de uso** | Ideal para tareas donde la lógica es clara y no requiere pasos intermedios, como obtener el pronóstico del tiempo, enviar un correo electrónico o buscar información específica en una base de datos. | Mejor para tareas que requieren **razonamiento complejo y adaptativo**, como la resolución de problemas creativos, la toma de decisiones en tiempo real o la búsqueda de información que requiere múltiples consultas. |
| **Dependencia** | Depende de las funciones y su esquema definidos en la API del modelo. Si no hay una función predefinida, el modelo no puede "llamarse" a sí mismo. | Depende de la calidad del prompt y de la capacidad del modelo para seguir instrucciones. Es más versátil y puede usar herramientas que no están predefinidas de antemano. |
| **Ejemplo de respuesta del LLM** | `{"name": "get_weather", "arguments": {"location": "Santiago"}}` | `Pensamiento: El usuario quiere saber el tiempo en Santiago. Necesito una herramienta para obtener el pronóstico del tiempo.<br>Acción: get_weather<br>Entrada de acción: Santiago` |