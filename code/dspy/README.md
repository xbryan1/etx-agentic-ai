# 🧪 DSPy experiments 🧪

💥 THIS IS EXPERIMENTAL 💥

An experiment to try out DSPy with our setup.

My plan was to test these use cases out with DSPy

- DSPy -> LlamaStack (model) using openai
- DSPy -> LlamaStack (model) using openai, MCP servers
- DSPy -> LlamaStack (model) using openai, MCP servers, RAG

Tools in use:

[DSPy](https://dspy.ai/) is a declarative framework for building modular AI software. It allows you to iterate fast on structured code, rather than brittle strings, and offers algorithms that compile AI programs into effective prompts and weights for your language models, whether you're building simple classifiers, sophisticated RAG pipelines, or Agent loops.

[ColBERT](https://huggingface.co/colbert-ir/colbertv2.0) is a fast and accurate retrieval model, enabling scalable BERT-based search over large text collections in tens of milliseconds.

If you're looking for the DSP framework for composing ColBERTv2 and LLMs, it's at: https://github.com/stanfordnlp/dsp

[PyLate](https://github.com/lightonai/pylate) PyLate is a library built on top of Sentence Transformers, designed to simplify and optimize fine-tuning, inference, and retrieval with state-of-the-art ColBERT models.

[FastMCP](https://gofastmcp.com/servers/proxy#multi-server-configurations) Use FastMCP to act as an intermediary or change transport for other MCP servers.

[Scrapy](https://docs.scrapy.org/en/latest/intro/overview.html) Scrapy is an application framework for crawling web sites and extracting structured data which can be used for a wide range of useful applications, like data mining, information processing or historical archival.

[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) Beautiful Soup is a Python library for pulling data out of HTML and XML files.

## Getting Started

Install python environment.

DSPy (running dspy experiments)

```bash
cd dspy
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Colbertv2.0 (optional - this is for developing RAG from scratch)

```bash
cd dspy/colbertv2.0
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Scrapy (optional - this is for web scraping developers.redhat.com)

```bash
cd dspy/scrapy
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

MLFLow - we are using this for tracing. Run locally.

```bash
pip install mlflow
mlflow ui --port 5500 &
```

## Local development

We can port forward LLamaStack and MCP servers for local development.

```bash
oc -n llama-stack port-forward svc/llamastack-with-config-service 8321:8321 2>&1>/dev/null &
oc -n agent-demo port-forward svc/ocp-mcp-server 8000:8000 2>&1>/dev/null &
oc -n agent-demo port-forward svc/github-mcp-server 8080:80 2>&1>/dev/null &
```

You can check these work using mcp llama stack client.

```bash
python mcp-llama-stack-client.py
```

## Connect to LLMs using DSPy

Do a Chain of Thought question and answer with remote LLM exposed via LlamaStack.

Export in your environment.

```bash
export LLM_URL=http://localhost:8321/v1/openai/v1  # port forward llama-stack api
export API_KEY=d2...  # you maas key
export LLM_MODEL="openai/llama-4-scout-17b-16e-w4a16"  # llm in maas we using
export MAX_TOKENS=110000
```

Try it out.

```bash
python dspy-llm.py
```

Response

```bash
--- Using dspy.ChainOfThought for Enhanced QA ---
(venv) virt:~/git/etx-agentic-ai/code/dspy ⎇ main#8d809ba$ python dspy-llm.py 

--- Using dspy.ChainOfThought for Enhanced QA ---
Question: What is the primary function of chlorophyll in plants?
Reasoning: To determine the primary function of chlorophyll in plants, we should consider the role of chlorophyll in the process of photosynthesis. Photosynthesis is how plants convert light energy into chemical energy. Chlorophyll is known to absorb light, particularly in the blue and red spectrum, which is crucial for initiating the photosynthetic process.
Answer: Absorb light for photosynthesis

--- Inspecting LM History ---

[2025-08-04T11:29:43.321309]

System message:

Your input fields are:
1. `question` (str):
Your output fields are:
1. `reasoning` (str): 
2. `answer` (str): often between 1 and 5 words
All interactions will be structured in the following way, with the appropriate values filled in.

[[ ## question ## ]]
{question}

[[ ## reasoning ## ]]
{reasoning}

[[ ## answer ## ]]
{answer}

[[ ## completed ## ]]
In adhering to this structure, your objective is: 
        Answer questions with short factoid answers.


User message:

[[ ## question ## ]]
What is the primary function of chlorophyll in plants?

Respond with the corresponding output fields, starting with the field `[[ ## reasoning ## ]]`, then `[[ ## answer ## ]]`, and then ending with the marker for `[[ ## completed ## ]]`.


Response:

[[ ## reasoning ## ]]
To determine the primary function of chlorophyll in plants, we should consider the role of chlorophyll in the process of photosynthesis. Photosynthesis is how plants convert light energy into chemical energy. Chlorophyll is known to absorb light, particularly in the blue and red spectrum, which is crucial for initiating the photosynthetic process.

[[ ## answer ## ]]
Absorb light for photosynthesis

[[ ## completed ## ]]
```

## Connect to LLMs, MCP using DSPy

Connect and list our MCP tools using DSPy. For this we need to proxy the mcp tools directly to DSPy. i cannot seem to use any LLS api's for this.

We using FastMCP to proxy.

```bash
python mcp-dspy.py
```

Results (big list of mcp tools).

```bash
(venv) virt:~/git/etx-agentic-ai/code/dspy ⎇ main#df4d993$ python mcp-dspy.py 


╭─ FastMCP 2.0 ──────────────────────────────────────────────────────────────╮
│                                                                            │
│        _ __ ___ ______           __  __  _____________    ____    ____     │
│       _ __ ___ / ____/___ ______/ /_/  |/  / ____/ __ \  |___ \  / __ \    │
│      _ __ ___ / /_  / __ `/ ___/ __/ /|_/ / /   / /_/ /  ___/ / / / / /    │
│     _ __ ___ / __/ / /_/ (__  ) /_/ /  / / /___/ ____/  /  __/_/ /_/ /     │
│    _ __ ___ /_/    \__,_/____/\__/_/  /_/\____/_/      /_____(_)____/      │
│                                                                            │
│                                                                            │
│                                                                            │
│    🖥️  Server name:     Composite Proxy                                     │
│    📦 Transport:       STDIO                                               │
│                                                                            │
│    📚 Docs:            https://gofastmcp.com                               │
│    🚀 Deploy:          https://fastmcp.cloud                               │
│                                                                            │
│    🏎️  FastMCP version: 2.11.0                                              │
│    🤝 MCP version:     1.12.2                                              │
│                                                                            │
╰────────────────────────────────────────────────────────────────────────────╯


[08/04/25 11:38:34] INFO     Starting MCP server 'Composite Proxy' with transport 'stdio'                                                                                       server.py:1442
Number of Tools: 93
[
│   Tool(
│   │   func=<function convert_mcp_tool.<locals>.func at 0x7fb1f8ff18a0>,
│   │   name='mcp::openshift_configuration_view',
│   │   desc='Get the current Kubernetes configuration content as a kubeconfig YAML',
│   │   args={
│   │   │   'minified': {
│   │   │   │   'description': 'Return a minified version of the configuration. If set to true, keeps only the current-context and the relevant pieces of the configuration for that context. If set to false, all contexts, clusters, auth-infos, and users are returned in the configuration. (Optional, default true)',
│   │   │   │   'type': 'boolean'
│   │   │   }
│   │   },
│   │   arg_types={'minified': <class 'bool'>},
│   │   arg_desc={
│   │   │   'minified': 'Return a minified version of the configuration. If set to true, keeps only the current-context and the relevant pieces of the configuration for that context. If set to false, all contexts, clusters, auth-infos, and users are returned in the configuration. (Optional, default true)'
│   │   },
│   │   has_kwargs=True
│   ),
... 
```

## Connect to LLMs, MCP, RAG using DSPy

FIXME

## Web scrape developers.red.hat.com

Grab the list or URLs for all articles from developers.redhat.com

```bash
wget https://raw.githubusercontent.com/eformat/dev-rh-rag-loader/refs/heads/main/developers-redhat-com.sh
chmod 755 developers-redhat-com.sh
./developers-redhat-com.sh
```

This will create a file `/tmp/developers.redhat.com-2025-08-03-07-12-41.uri` or URIs

Run scrapy spider against this file or urls for all titles, paragraphs, code blocks. Adjust the spider to get the content you want to then index.

```bash
scrapy runspider spider-dev-red.py -o dev-red-rag.jsonl
```

Should generate a `dev-red-rag.jsonl` file. It took me this long ...

```bash
2025-08-04 08:14:35 [scrapy.core.engine] INFO: Spider closed (finished)
real	16m57.287s
user	4m31.672s
sys	0m2.857s
```

## Create a Colbertv2.0 index for RAG

You need a working NVIDIA GPU and CUDA here. I am using my laptop which has `cuda-toolkit-12.9.1-1.x86_64` and a `NVIDIA GeForce RTX 4070`.

We are going to use the [jsonl](https://jsonlines.org/) file to create the Colbertv2.0 index.

```bash
(venv) virt:~/git/colbertv2.0$ python index2.py 
/home/mike/git/colbertv2.0/index2.py:1: UserWarning: 
********************************************************************************
RAGatouille WARNING: Future Release Notice
--------------------------------------------
RAGatouille version 0.0.10 will be migrating to a PyLate backend 
instead of the current Stanford ColBERT backend.
PyLate is a fully mature, feature-equivalent backend, that greatly facilitates compatibility.
However, please pin version <0.0.10 if you require the Stanford ColBERT backend.
********************************************************************************
  from ragatouille import RAGPretrainedModel
/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/networkx/utils/backends.py:135: RuntimeWarning: networkx backend defined more than once: nx-loopback
  backends.update(_get_backends("networkx.backends"))
/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/colbert/utils/amp.py:12: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
  self.scaler = torch.cuda.amp.GradScaler()
[Aug 04, 08:38:18] #> Creating directory .ragatouille/colbert/indexes/dev-red-rag 
[Aug 04, 08:38:22] [0] 		 #> Encoding 129880 passages..
/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/colbert/utils/amp.py:15: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
  return torch.cuda.amp.autocast() if self.activated else NullContextManager()
[Aug 04, 08:45:38] [0] 		 avg_doclen_est = 20.08635711669922 	 len(local_sample) = 129,880
[Aug 04, 08:45:39] [0] 		 Creating 32,768 partitions.
[Aug 04, 08:45:39] [0] 		 *Estimated* 11,029,579 embeddings.
[Aug 04, 08:45:39] [0] 		 #> Saving the indexing plan to .ragatouille/colbert/indexes/dev-red-rag/plan.json ..
Clustering 2558816 points in 128D to 32768 clusters, redo 1 times, 4 iterations
  Preprocessing in 0.23 s
  Iteration 3 (37.17 s, search 34.92 s): objective=432944 imbalance=2.130 nsplit=4         
[Aug 04, 08:46:18] Loading decompress_residuals_cpp extension (set COLBERT_LOAD_TORCH_EXTENSION_VERBOSE=True for more info)...
[Aug 04, 08:46:19] Loading packbits_cpp extension (set COLBERT_LOAD_TORCH_EXTENSION_VERBOSE=True for more info)...
[0.026, 0.028, 0.026, 0.025, 0.024, 0.027, 0.027, 0.024, 0.025, 0.026, 0.026, 0.025, 0.026, 0.026, 0.026, 0.028, 0.024, 0.025, 0.025, 0.026, 0.026, 0.027, 0.026, 0.025, 0.025, 0.025, 0.027, 0.026, 0.027, 0.027, 0.026, 0.027, 0.027, 0.026, 0.025, 0.023, 0.027, 0.025, 0.025, 0.03, 0.026, 0.027, 0.027, 0.027, 0.027, 0.025, 0.024, 0.03, 0.027, 0.025, 0.025, 0.025, 0.027, 0.028, 0.024, 0.026, 0.028, 0.027, 0.03, 0.025, 0.026, 0.028, 0.026, 0.026, 0.028, 0.026, 0.027, 0.026, 0.025, 0.026, 0.028, 0.024, 0.025, 0.027, 0.025, 0.027, 0.026, 0.027, 0.026, 0.026, 0.028, 0.027, 0.026, 0.026, 0.026, 0.027, 0.026, 0.025, 0.025, 0.028, 0.025, 0.027, 0.025, 0.028, 0.026, 0.026, 0.029, 0.024, 0.027, 0.026, 0.027, 0.027, 0.026, 0.025, 0.027, 0.025, 0.026, 0.025, 0.026, 0.024, 0.027, 0.026, 0.026, 0.025, 0.026, 0.024, 0.026, 0.027, 0.026, 0.027, 0.025, 0.025, 0.026, 0.026, 0.026, 0.029, 0.028, 0.025]
0it [00:00, ?it/s][Aug 04, 08:46:20] [0] 		 #> Encoding 25000 passages..
/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/colbert/utils/amp.py:15: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
  return torch.cuda.amp.autocast() if self.activated else NullContextManager()
1it [01:22, 82.12s/it][Aug 04, 08:47:42] [0] 		 #> Encoding 25000 passages..
2it [02:35, 77.23s/it][Aug 04, 08:48:56] [0] 		 #> Encoding 25000 passages..
3it [03:25, 64.64s/it][Aug 04, 08:49:45] [0] 		 #> Encoding 25000 passages..
4it [04:23, 62.09s/it][Aug 04, 08:50:44] [0] 		 #> Encoding 25000 passages..
5it [05:30, 63.92s/it][Aug 04, 08:51:51] [0] 		 #> Encoding 25000 passages..
6it [06:40, 65.97s/it][Aug 04, 08:53:01] [0] 		 #> Encoding 25000 passages..
7it [08:05, 72.19s/it][Aug 04, 08:54:26] [0] 		 #> Encoding 25000 passages..

8it [09:37, 78.52s/it][Aug 04, 08:55:58] [0] 		 #> Encoding 25000 passages..
9it [11:07, 82.02s/it][Aug 04, 08:57:28] [0] 		 #> Encoding 25000 passages..
10it [12:41, 85.66s/it][Aug 04, 08:59:01] [0] 		 #> Encoding 25000 passages..
11it [14:14, 87.85s/it][Aug 04, 09:00:34] [0] 		 #> Encoding 25000 passages..
12it [15:48, 89.81s/it][Aug 04, 09:02:08] [0] 		 #> Encoding 25000 passages..
13it [17:24, 91.73s/it][Aug 04, 09:03:45] [0] 		 #> Encoding 25000 passages..
14it [18:57, 91.95s/it][Aug 04, 09:05:17] [0] 		 #> Encoding 25000 passages..
15it [20:32, 92.83s/it][Aug 04, 09:06:52] [0] 		 #> Encoding 25000 passages..
16it [22:03, 92.55s/it][Aug 04, 09:08:24] [0] 		 #> Encoding 25000 passages..
17it [23:40, 93.73s/it][Aug 04, 09:10:00] [0] 		 #> Encoding 25000 passages..
18it [25:11, 93.01s/it][Aug 04, 09:11:32] [0] 		 #> Encoding 25000 passages..
19it [26:46, 93.46s/it][Aug 04, 09:13:06] [0] 		 #> Encoding 25000 passages..
20it [28:18, 93.03s/it][Aug 04, 09:14:38] [0] 		 #> Encoding 25000 passages..
21it [29:55, 94.18s/it][Aug 04, 09:16:15] [0] 		 #> Encoding 24108 passages..
22it [31:24, 85.68s/it]
100%|████████████████████████████████████████████████████████| 22/22 [00:00<00:00, 210.42it/s]
[Aug 04, 09:17:46] #> Optimizing IVF to store map from centroids to list of pids..
[Aug 04, 09:17:46] #> Building the emb2pid mapping..
[Aug 04, 09:17:47] len(emb2pid) = 11019252
100%|████████████████████████████████████████████████| 32768/32768 [00:00<00:00, 53455.02it/s]
[Aug 04, 09:17:48] #> Saved optimized IVF to .ragatouille/colbert/indexes/dev-red-rag/ivf.pid.pt
Done indexing!
```

![images/colbert-index.png](images/colbert-index.png)

This will generate the index

```bash
(venv) virt:~/git/colbertv2.0$ tree .ragatouille/colbert/indexes/dev-red-rag/
.ragatouille/colbert/indexes/dev-red-rag/
├── 0.codes.pt
├── 0.metadata.json
├── 0.residuals.pt
├── 10.codes.pt
├── 10.metadata.json
├── 10.residuals.pt
├── 11.codes.pt
├── 11.metadata.json
├── 11.residuals.pt
├── 12.codes.pt
├── 12.metadata.json
├── 12.residuals.pt
├── 13.codes.pt
├── 13.metadata.json
├── 13.residuals.pt
├── 14.codes.pt
├── 14.metadata.json
├── 14.residuals.pt
├── 15.codes.pt
├── 15.metadata.json
├── 15.residuals.pt
├── 16.codes.pt
├── 16.metadata.json
├── 16.residuals.pt
├── 17.codes.pt
├── 17.metadata.json
├── 17.residuals.pt
├── 18.codes.pt
├── 18.metadata.json
├── 18.residuals.pt
├── 19.codes.pt
├── 19.metadata.json
├── 19.residuals.pt
├── 1.codes.pt
├── 1.metadata.json
├── 1.residuals.pt
├── 20.codes.pt
├── 20.metadata.json
├── 20.residuals.pt
├── 21.codes.pt
├── 21.metadata.json
├── 21.residuals.pt
├── 2.codes.pt
├── 2.metadata.json
├── 2.residuals.pt
├── 3.codes.pt
├── 3.metadata.json
├── 3.residuals.pt
├── 4.codes.pt
├── 4.metadata.json
├── 4.residuals.pt
├── 5.codes.pt
├── 5.metadata.json
├── 5.residuals.pt
├── 6.codes.pt
├── 6.metadata.json
├── 6.residuals.pt
├── 7.codes.pt
├── 7.metadata.json
├── 7.residuals.pt
├── 8.codes.pt
├── 8.metadata.json
├── 8.residuals.pt
├── 9.codes.pt
├── 9.metadata.json
├── 9.residuals.pt
├── avg_residual.pt
├── buckets.pt
├── centroids.pt
├── collection.json
├── docid_metadata_map.json
├── doclens.0.json
├── doclens.10.json
├── doclens.11.json
├── doclens.12.json
├── doclens.13.json
├── doclens.14.json
├── doclens.15.json
├── doclens.16.json
├── doclens.17.json
├── doclens.18.json
├── doclens.19.json
├── doclens.1.json
├── doclens.20.json
├── doclens.21.json
├── doclens.2.json
├── doclens.3.json
├── doclens.4.json
├── doclens.5.json
├── doclens.6.json
├── doclens.7.json
├── doclens.8.json
├── doclens.9.json
├── ivf.pid.pt
├── metadata.json
├── pid_docid_map.json
└── plan.json

1 directory, 97 files
```

Test a single Retrieve of documents.

```python
query = "tell me about small models and Neural Magic"
RAG = RAGPretrainedModel.from_index("/home/mike/git/colbertv2.0/.ragatouille/colbert/indexes/dev-red-rag")
```

Results:

```bash
(venv) virt:~/git/colbertv2.0$ python retrieve2.py 
/home/mike/git/colbertv2.0/retrieve2.py:1: UserWarning: 
********************************************************************************
RAGatouille WARNING: Future Release Notice
--------------------------------------------
RAGatouille version 0.0.10 will be migrating to a PyLate backend 
instead of the current Stanford ColBERT backend.
PyLate is a fully mature, feature-equivalent backend, that greatly facilitates compatibility.
However, please pin version <0.0.10 if you require the Stanford ColBERT backend.
********************************************************************************
  from ragatouille import RAGPretrainedModel
/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/networkx/utils/backends.py:135: RuntimeWarning: networkx backend defined more than once: nx-loopback
  backends.update(_get_backends("networkx.backends"))
/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/colbert/utils/amp.py:12: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
  self.scaler = torch.cuda.amp.GradScaler()
Loading searcher for index dev-red-rag for the first time... This may take a few seconds
[Aug 04, 09:23:25] #> Loading codec...
[Aug 04, 09:23:25] Loading decompress_residuals_cpp extension (set COLBERT_LOAD_TORCH_EXTENSION_VERBOSE=True for more info)...
[Aug 04, 09:23:25] Loading packbits_cpp extension (set COLBERT_LOAD_TORCH_EXTENSION_VERBOSE=True for more info)...
[Aug 04, 09:23:25] #> Loading IVF...
[Aug 04, 09:23:25] #> Loading doclens...
100%|███████████████████████████████████████████████████████| 22/22 [00:00<00:00, 2259.59it/s]
[Aug 04, 09:23:25] #> Loading codes and residuals...
100%|████████████████████████████████████████████████████████| 22/22 [00:00<00:00, 184.30it/s]
Searcher loaded!

#> QueryTokenizer.tensorize(batch_text[0], batch_background[0], bsize) ==
#> Input: tell me about small models and Neural Magic, 		 True, 		 None
#> Output IDs: torch.Size([32]), tensor([  101,     1,  2425,  2033,  2055,  2235,  4275,  1998, 15756,  3894,
          102,   103,   103,   103,   103,   103,   103,   103,   103,   103,
          103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
          103,   103], device='cuda:0')
#> Output Mask: torch.Size([32]), tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0], device='cuda:0')

/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/colbert/utils/amp.py:15: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
  return torch.cuda.amp.autocast() if self.activated else NullContextManager()
[
    {
        'content': 'Weight sparsity, which consists of pruning individual weights from a 
neural network by setting them to zero, can be combined with quantization to compress models 
even more. In the past, Neural Magic has pruned smaller models like BERT to >90% sparsity, but
it had not been confirmed whether these techniques can be applied to the scale of LLMs.',
        'score': 22.9375,
        'rank': 1,
        'document_id': 'eae02018-fb1f-4282-a771-0baf8bbfac9a',
        'passage_id': 516510,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2023/10/12/sparse-fine-tuning-accelerating-llms-with-d
eepsparse'
            },
            {
                'entity': 'title',
                'source': 'Sparse fine-tuning for accelerating large language models with 
DeepSparse | Red Hat Developer'
            }
        ]
    },
    {
        'content': 'Neural Magic is doubling down on this challenge with sparse LLMs—reducing 
the model size by removing unneeded connections while retaining accuracy. Sparse models, 
though underexplored in the LLM space due to the high compute demands of pretraining, offer an
increasingly promising dimension in model compression and efficiency.',
        'score': 21.328125,
        'rank': 2,
        'document_id': '1d333031-c469-4689-bfa7-8fd861803d62',
        'passage_id': 511643,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2025/02/28/24-sparse-llama-smaller-models-efficient-gp
u-inference'
            },
            {
                'entity': 'title',
                'source': '2:4 Sparse Llama: Smaller models for efficient GPU inference | Red 
Hat Developer'
            }
        ]
    },
    {
        'content': 'Neural Magic, now part of Red Hat, is a top commercial contributor to 
vLLM, working extensively on model and systems optimizations to improve vLLM performance at 
scale. The framework supports multimodal models, embeddings, and reward modeling, and is 
increasingly used in reinforcement learning with human feedback (RLHF) workflows. With 
features such as advanced scheduling, chunk prefill, Multi-LoRA batching, and structured 
outputs, vLLM is optimized for both inference acceleration and enterprise-scale deployment.',
        'score': 20.15625,
        'rank': 3,
        'document_id': 'd50d7758-ff1b-4347-8bda-83be23d71252',
        'passage_id': 521917,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2025/03/19/how-we-optimized-vllm-deepseek-r1'
            },
            {
                'entity': 'title',
                'source': 'How we optimized vLLM for DeepSeek-R1 | Red Hat Developer'
            }
        ]
    },
    {
        'content': 'Neural Magic DeepSparse is a CPU inference runtime that implements 
optimizations to take advantage of sparsity and quantization to accelerate inference 
performance. DeepSparse supports a large variety of model architectures including CNNs like 
YOLO and\xa0encoder-only transformers like BERT. Over the past several months we have adapted 
DeepSparse to support the decoder-only architecture used by popular models like Llama 2 and 
MPT with specialized infrastructure to handle KV-caching and new sparse math kernels targeted 
at the key operations underlying decoder models.',
        'score': 19.75,
        'rank': 4,
        'document_id': '0699f36c-4bc0-4148-9008-78d7d189464e',
        'passage_id': 516516,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2023/10/12/sparse-fine-tuning-accelerating-llms-with-d
eepsparse'
            },
            {
                'entity': 'title',
                'source': 'Sparse fine-tuning for accelerating large language models with 
DeepSparse | Red Hat Developer'
            }
        ]
    },
    {
        'content': "LLM Compressor, a unified library for creating compressed models for 
faster inference with vLLM, is now available. Neural Magic's research team has successfully 
utilized it to create our latest compressed models, including fully quantized and accurate 
versions of Llama 3.1, and with that, we are excited to open up the toolkit to the community 
with its first 0.1 release for general usage to compress your models!",
        'score': 19.546875,
        'rank': 5,
        'document_id': 'b7fae44c-ebf6-4b97-bccc-ae37881ba2cd',
        'passage_id': 511981,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2024/08/14/llm-compressor-here-faster-inference-vllm'
            },
            {
                'entity': 'title',
                'source': 'LLM Compressor is here: Faster inference with vLLM | Red Hat 
Developer'
            }
        ]
    },
    {
        'content': 'At Neural Magic, we believe the future of AI is open, and we are on a 
mission to bring the power of open source models and vLLM to every enterprise on the planet.',
        'score': 19.515625,
        'rank': 6,
        'document_id': '2338170b-a95a-4a1a-981a-52fdc34180a4',
        'passage_id': 512047,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2024/08/14/llm-compressor-here-faster-inference-vllm'
            },
            {
                'entity': 'title',
                'source': 'LLM Compressor is here: Faster inference with vLLM | Red Hat 
Developer'
            }
        ]
    },
    {
        'content': 'Neural Magic is proud to continue its commitment to the open-source 
community, empowering developers, researchers, and enterprises to adopt and build upon these 
innovations. Our open source FP8 models and high-performance kernels for vLLM are designed to 
simplify integration and experimentation for real-world use cases.',
        'score': 19.46875,
        'rank': 7,
        'document_id': '85e555da-5007-44b1-b181-dcc42921b577',
        'passage_id': 513078,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2024/12/18/24-sparse-llama-fp8-sota-performance-nvidia
-hopper-gpus'
            },
            {
                'entity': 'title',
                'source': '2:4 Sparse Llama FP8: SOTA performance for NVIDIA Hopper GPUs | Red
Hat Developer'
            }
        ]
    },
    {
        'content': 'Neural Magic and the Institute of Science and Technology Austria (ISTA) 
collaborated to explore how fine-tuning and sparsity can come together to address these 
issues, to enable accurate models that can be deployed on CPUs.',
        'score': 19.421875,
        'rank': 8,
        'document_id': '4998389b-4075-4b19-bf75-85e5f70e27a2',
        'passage_id': 516492,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2023/10/12/sparse-fine-tuning-accelerating-llms-with-d
eepsparse'
            },
            {
                'entity': 'title',
                'source': 'Sparse fine-tuning for accelerating large language models with 
DeepSparse | Red Hat Developer'
            }
        ]
    },
    {
        'content': 'Neural Magic’s integration into Red Hat marks an exciting new era for open
and efficient AI. The compressed Granite 3.1 models and vLLM support exemplify the benefits of
combining state-of-the-art model compression, advanced high-performance computing, and 
enterprise-grade generative AI capabilities.',
        'score': 19.390625,
        'rank': 9,
        'document_id': '1784f617-7ddd-484e-ad9d-ba2f88e6290f',
        'passage_id': 513216,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2025/01/30/compressed-granite-3-1-powerful-performance
-small-package'
            },
            {
                'entity': 'title',
                'source': 'Compressed Granite 3.1: Powerful performance in a small package | 
Red Hat Developer'
            }
        ]
    },
    {
        'content': 'Now part of Red Hat, Neural Magic remains the leading commercial 
contributor to vLLM, providing enterprise-ready optimized models and distributions that help 
businesses maximize GPU utilization for optimized deployments.\xa0Read on to learn more about 
vLLM and distributed inference. If you prefer, you can watch the full',
        'score': 19.046875,
        'rank': 10,
        'document_id': 'a4050198-d479-41ec-814e-fb2ff935ec52',
        'passage_id': 514788,
        'document_metadata': [
            {
                'entity': 'url',
                'source': 
'https://developers.redhat.com/articles/2025/02/06/distributed-inference-with-vllm'
            },
            {
                'entity': 'title',
                'source': 'Distributed inference with vLLM | Red Hat Developer'
            }
        ]
    }
]
```

## Host a Colbertv2.0 server

We are going to host a flask server with the index, then query it using MCP from DSPy

```bash
python server.py 
```

Server starts up.

```bash
Importing RAGPretrainedModel from ragatouille (this might take a while)...
/home/mike/git/colbertv2.0/server.py:12: UserWarning: 
********************************************************************************
RAGatouille WARNING: Future Release Notice
--------------------------------------------
RAGatouille version 0.0.10 will be migrating to a PyLate backend 
instead of the current Stanford ColBERT backend.
PyLate is a fully mature, feature-equivalent backend, that greatly facilitates compatibility.
However, please pin version <0.0.10 if you require the Stanford ColBERT backend.
********************************************************************************
  from ragatouille import RAGPretrainedModel
/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/networkx/utils/backends.py:135: RuntimeWarning: networkx backend defined more than once: nx-loopback
  backends.update(_get_backends("networkx.backends"))
RAGPretrainedModel imported successfully.
Initializing the engine...
/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/colbert/utils/amp.py:12: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
  self.scaler = torch.cuda.amp.GradScaler()
Engine initialized successfully.
 * Serving Flask app 'server'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8081
 * Running on http://10.0.0.3:8081
Press CTRL+C to quit
API request count: 1
Query=tell me about small models and Neural Magic
Loading searcher for index dev-red for the first time... This may take a few seconds
[Aug 04, 09:28:03] #> Loading codec...
[Aug 04, 09:28:03] Loading decompress_residuals_cpp extension (set COLBERT_LOAD_TORCH_EXTENSION_VERBOSE=True for more info)...
[Aug 04, 09:28:03] Loading packbits_cpp extension (set COLBERT_LOAD_TORCH_EXTENSION_VERBOSE=True for more info)...
[Aug 04, 09:28:03] #> Loading IVF...
[Aug 04, 09:28:03] #> Loading doclens...
100%|█████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 2935.13it/s]
[Aug 04, 09:28:03] #> Loading codes and residuals...
100%|██████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 224.31it/s]
Searcher loaded!

#> QueryTokenizer.tensorize(batch_text[0], batch_background[0], bsize) ==
#> Input: tell me about small models and Neural Magic, 		 True, 		 None
#> Output IDs: torch.Size([32]), tensor([  101,     1,  2425,  2033,  2055,  2235,  4275,  1998, 15756,  3894,
          102,   103,   103,   103,   103,   103,   103,   103,   103,   103,
          103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
          103,   103], device='cuda:0')
#> Output Mask: torch.Size([32]), tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0], device='cuda:0')

/home/mike/git/colbertv2.0/venv/lib64/python3.9/site-packages/colbert/utils/amp.py:15: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
  return torch.cuda.amp.autocast() if self.activated else NullContextManager()
127.0.0.1 - - [04/Aug/2025 09:28:04] "GET /api/search?query=tell%20me%20about%20small%20models%20and%20Neural%20Magic&k=3 HTTP/1.1" 200 -
API request count: 2
127.0.0.1 - - [04/Aug/2025 09:28:13] "GET /api/search?query=tell%20me%20about%20small%20models%20and%20Neural%20Magic&k=3 HTTP/1.1" 200 -
API request count: 3
127.0.0.1 - - [04/Aug/2025 10:04:53] "GET /api/search?query=tell%20me%20about%20small%20models%20and%20Neural%20Magic&k=3 HTTP/1.1" 200 -
```

Test Query

```json
prompt: "tell me about small models and Neural Magic"
k: 3
```

```bash
time curl -s 'http://localhost:8081/api/search?query=tell%20me%20about%20small%20models%20and%20Neural%20Magic&k=3' | jq .
[
  {
    "content": "Neural Magic is doubling down on this challenge with sparse LLMs—reducing the model size by removing unneeded connections while retaining accuracy. Sparse models, though underexplored in the LLM space due to the high compute demands of pretraining, offer an increasingly promising dimension in model compression and efficiency.",
    "document_id": "2391ac26-01f8-49ef-b654-c15e0f6e975a",
    "document_metadata": [
      {
        "entity": "url",
        "source": "https://developers.redhat.com/articles/2025/02/28/24-sparse-llama-smaller-models-efficient-gpu-inference"
      },
      {
        "entity": "title",
        "source": "2:4 Sparse Llama: Smaller models for efficient GPU inference | Red Hat Developer"
      }
    ],
    "passage_id": 501,
    "rank": 1,
    "score": 20.09375
  },
  {
    "content": "Neural networks are a class of machine learning models inspired by the human brain. They are made up of layers of interconnected units called neurons, or nodes, which process input data and learn patterns to make predictions or decisions. Neural networks are the foundation of many artificial intelligence applications, including image recognition, speech processing, and natural language understanding (Figure 6).",
    "document_id": "88c26d65-dcd8-44ac-a668-c9bd327b6b2c",
    "document_metadata": [
      {
        "entity": "url",
        "source": "https://developers.redhat.com/articles/2025/04/10/road-ai-guide-understanding-aiml-models"
      },
      {
        "entity": "title",
        "source": "The road to AI: A guide to understanding AI/ML models | Red Hat Developer"
      }
    ],
    "passage_id": 89,
    "rank": 2,
    "score": 16.0
  },
  {
    "content": "These considerations led us to explore techniques that enhance the small language model-powered agent's ability to orchestrate multiple tool calls and reason dynamically.",
    "document_id": "4e7af5df-deb1-4529-b0a9-f10df7633c01",
    "document_metadata": [
      {
        "entity": "url",
        "source": "https://developers.redhat.com/articles/2025/07/22/react-vs-naive-prompt-chaining-llama-stack"
      },
      {
        "entity": "title",
        "source": "ReAct vs. naive prompt chaining on Llama Stack | Red Hat Developer"
      }
    ],
    "passage_id": 1462,
    "rank": 3,
    "score": 15.453125
  }
]

real	0m0.008s
user	0m0.002s
sys	0m0.006s
```
