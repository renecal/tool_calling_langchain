from langchain.callbacks.base import BaseCallbackHandler

class AgentCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for agent events."""

    def on_llm_start(self, serialized, prompts, **kwargs):
        print("---")
        print("🤖 Starting the call to the LLM model ...")
        print("Prompts sender:")
        for i, prompt in enumerate(prompts):
            print(f"Prompt {i+1}:\n{prompt}\n")
        print("---")

    def on_llm_end(self, response, **kwargs):
        print("LLM finished with response:", response)
        print("****** end on_llm_end ******")
        print('\n')