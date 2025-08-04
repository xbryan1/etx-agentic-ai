# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rich.pretty import pprint
import mlflow
import dspy
import os

mlflow.set_tracking_uri("http://localhost:5500")
mlflow.set_experiment("20_days_dspy")
mlflow.dspy.autolog()

# mlflow.dspy.autolog(
#     log_compiles=True,    # Track optimization process
#     log_evals=True,       # Track evaluation results
#     log_traces_from_compile=True  # Track program traces during optimization
# )

# 1. Configure the Language Model
#    Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key.
#    You can also set it as an environment variable: export OPENAI_API_KEY='your_key_here'
#    If using a local LM with Ollama or SGLang, adjust api_base and api_key accordingly.

LLM_URL=os.getenv('LLM_URL', 'http://localhost:8080/v1')
API_KEY=os.getenv('API_KEY', 'fake')
LLM_MODEL=os.getenv('LLM_MODEL', 'openai/models/Llama-3.2-3B-Instruct-Q8_0.gguf')
MAX_TOKENS=os.getenv('MAX_TOKENS', 3000)
TEMPERATURE=os.getenv('TEMPERATURE', 0.2)
dspy.enable_logging()

lm = dspy.LM(model=LLM_MODEL,
             api_base=LLM_URL,
             api_key=API_KEY,
             temperature=TEMPERATURE,
             model_type='chat',
             stream=False,
             cache=False)
dspy.configure(lm=lm)
dspy.settings.configure(track_usage=True)

server_params = StdioServerParameters(
    command="python",
    args=["mcp-proxy.py"],
)

class PodLogsSummarize(dspy.Signature):
    """You are an expert OpenShift administrator. Your task is to analyze pod logs and summarize the error. Review the OpenShift logs for the pod 'java-app-build-run-bad-80uy3b-build-pod' in the 'demo-pipeline' namespace. If the logs indicate an error, create a summary message with the category and explanation of the error."""

    user_request: str = dspy.InputField()
    process_result: str = dspy.OutputField(
        desc=(
            "Summary message with the category and explanation of the error"
        )
    )

async def run(user_request):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools = await session.list_tools()

            # Convert MCP tools to DSPy tools
            dspy_tools = []
            for tool in tools.tools:
                dspy_tools.append(dspy.Tool.from_mcp_tool(session, tool))

            print(f"Number of Tools: {len(dspy_tools)}")
            #pprint(dspy_tools)

            # Create the agent
            react = dspy.ReAct(PodLogsSummarize, tools=dspy_tools)

            result = await react.acall(user_request=user_request)
            pprint(result)

            dspy.inspect_history()

if __name__ == "__main__":
    import asyncio
    #(1) summarize pod logs error
    # asyncio.run(run("""You are an expert OpenShift administrator. Your task is to analyze pod logs and summarize the error. Review the OpenShift logs for the pod 'java-app-build-run-bad-80uy3b-build-pod' in the 'demo-pipeline' namespace. If the logs indicate an error, create a summary message with the category and explanation of the error."""))
    #(2) summarize, search for solution (with only mcp::github, mcp::openshift - agent uses mcp::github_search_issues)
    asyncio.run(run("""You are an expert OpenShift administrator. Your task is to analyze pod logs and summarize the error. Review the OpenShift logs for the pod 'java-app-build-run-bad-80uy3b-build-pod' in the 'demo-pipeline' namespace. If the logs indicate an error, search for the top OpenShift solution. Create a summary message with the category and explanation of the error."""))
