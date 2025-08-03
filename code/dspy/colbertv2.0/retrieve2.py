from ragatouille import RAGPretrainedModel
from rich import print

query = "tell me about small models and Neural Magic"
RAG = RAGPretrainedModel.from_index("/home/mike/git/colbertv2.0/.ragatouille/colbert/indexes/dev-red-rag")
results = RAG.search(query)
print(results)