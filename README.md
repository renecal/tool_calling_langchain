## Tool Calling
Tool calling is a mechanism that allows a language model to invoke external functions or tools based on the user's input. This approach is particularly useful for tasks that require specific actions, such as retrieving information from a database or performing calculations.

### How Tool Calling Works
1. **User Input**: The process begins with a user query or command that specifies the desired action.
2. **LLM Processing**: The language model processes the input and determines the appropriate tool to call.
3. **Tool Invocation**: The model generates a structured call to the selected tool, including any necessary parameters.
4. **Tool Execution**: The tool is executed, and the results are returned to the model.
5. **Response Generation**: Finally, the model incorporates the tool's output into its response to the user.

### Benefits of Tool Calling
- **Precision**: Tool calling allows for more precise actions by leveraging external functions.
- **Flexibility**: It enables the model to adapt to various tasks and requirements.
- **Efficiency**: By directly invoking tools, the model can streamline complex workflows.

## Useful Links Tool Calling
- [Blog Langchain](https://blog.langchain.com/)
- [Tool Calling with Langchain](http://blog.langchain.dev/tool-calling-with-langchain/)
- [Doc How to do tool/function calling langchain](https://python.langchain.com/docs/how_to/function_calling/)

## Useful Links General
- [Langchain ReAct Documentation](https://python.langchain.com/docs/how_to/migrate_agent/)
- [Langchain Agents Overview](https://python.langchain.com/docs/how_to/#agents)
- [Langchain API Reference render](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.render.render_text_description.html)
- [Tools](https://python.langchain.com/docs/concepts/tools/)
- [Tools Kits](https://python.langchain.com/docs/integrations/tools/)
- [Langchain hub hwchase17](https://smith.langchain.com/hub/hwchase17/react?organizationId=5c031c7d-225f-41cf-9def-21161772e1fa)
- [ReActSingleInputOutputParser](https://python.langchain.com/api_reference/langchain/agents/langchain.agents.output_parsers.react_single_input.ReActSingleInputOutputParser.html)
- [LCEL](https://python.langchain.com/docs/concepts/lcel/)
- [Callbacks](https://python.langchain.com/docs/how_to/#callbacks/)
