from ragatouille import RAGPretrainedModel

import json

#document_ids = []
documents = []
document_metadatas = []

with open("/home/mike/git/colbertv2.0/dev-red-rag.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)
        if "title" in data:
            document_metadatas.append([
                {"entity": "url", "source": data["url"]},
                {"entity": "title", "source": data["title"]},
            ])
            documents.append(data["title"])
        if "paragraph" in data:
            document_metadatas.append([
                {"entity": "url", "source": data["url"]},
                {"entity": "title", "source": data["title"]},
            ])
            documents.append(data["paragraph"])
        if "code" in data:
            document_metadatas.append([
                {"entity": "url", "source": data["url"]},
                {"entity": "title", "source": data["title"]},
            ])
            documents.append(data["code"])

RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
indexer = RAG.index(
    index_name="dev-red-rag",
    collection=documents,
    document_metadatas=document_metadatas,
)

# document_ids=document_ids,
# max_document_length=1000,
# split_documents=False,
