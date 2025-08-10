from ragatouille import RAGPretrainedModel

import json

#document_ids = []
documents = []
document_metadatas = []

with open("/home/mike/tmp/eformat-sent-mail.json", "r") as f:
    for line in f:
        data = json.loads(line)
        document_metadatas.append([
            {"entity": "from", "source": data["from"]},
            {"entity": "to", "source": data["to"]},
            {"entity": "date", "source": data["date"]},
            {"entity": "subject", "source": data["subject"]},
        ])
        documents.append(data["message"])

RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
indexer = RAG.index(
    index_name="eformat-sent-mail",
    collection=documents,
    document_metadatas=document_metadatas,
)

# document_ids=document_ids,
# max_document_length=1000,
# split_documents=False,
