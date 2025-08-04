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
TAVILY_API_KEY=os.getenv('TAVILY_API_KEY', 'fake')
URL = "https://mcp.tavily.com/mcp/?tavilyApiKey=" + TAVILY_API_KEY

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

colbertv2 = dspy.ColBERTv2(
    url="http://127.0.0.1:8081/api/search"
)
dspy.settings.configure(rm=colbertv2)

class RAGQA(dspy.Signature):
    """Answer questions based on the provided context."""

    context = dspy.InputField(desc="relevant passages from a knowledge base")
    question = dspy.InputField()
    answer = dspy.OutputField()

class BasicRAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)  # Retrieve top-k passages
        self.generate_answer = dspy.ChainOfThought(
            RAGQA
        )  # Generate answer using ChainOfThought

    def forward(self, question):
        # Perform retrieval
        context = self.retrieve(question).passages
        # Generate answer using the retrieved context
        prediction = self.generate_answer(context=context, question=question)
        return prediction

# Instantiate and run the Basic RAG program
rag_program = BasicRAG()

question_rag_1 = "Is RHOAI ready to use for Agentic AI"
prediction_rag_1 = rag_program(question=question_rag_1)

pprint(f"Question: {question_rag_1}")
pprint(f"Retrieved Context (first 2 passages):")
for i, passage in enumerate(rag_program.retrieve(question_rag_1).passages[:2]):
    pprint(f"  [{i + 1}] {passage}")
pprint(f"Reasoning: {prediction_rag_1.reasoning}")
pprint(f"Answer: {prediction_rag_1.answer}")

# Optional: Inspect history
pprint("\n--- Inspecting LM History")
dspy.inspect_history()
