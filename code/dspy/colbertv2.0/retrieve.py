from ragatouille import RAGPretrainedModel
from rich import print

query = "ColBERT my dear ColBERT, who is the fairest document of them all?"

RAG = RAGPretrainedModel.from_index("/home/mike/git/colbertv2.0/.ragatouille/colbert/indexes/my_index")
#results = RAG.search(query)

results = RAG.search(["What manga did Hayao Miyazaki write?",
"Who are the founders of Ghibli?"
"Who is the director of Spirited Away?"],)
print(results)