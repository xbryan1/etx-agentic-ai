# https://docs.scrapy.org/en/latest/intro/overview.html

# scrapy runspider spider-dev-red.py -o dev-red-rag.jsonl

from bs4 import BeautifulSoup
import scrapy
import json

class DeveloperRedHatSpider(scrapy.Spider):
    name = "dev-red-rag"

    start_urls = []

    with open('/tmp/developers.redhat.com-2025-08-03-07-12-41.uri', 'r') as file:
        start_urls = [line.strip() for line in file]

    # start_urls = [
    #     "https://developers.redhat.com/blog/2023/02/08/sno-spot",
    #     "https://developers.redhat.com/articles/2025/04/10/how-building-workbenches-accelerates-aiml-development",
    #     "https://developers.redhat.com/articles/2025/04/10/road-ai-guide-understanding-aiml-models",
    #     "https://developers.redhat.com/articles/2025/05/12/how-use-pipelines-aiml-automation-edge",
    #     "https://developers.redhat.com/articles/2025/02/28/24-sparse-llama-smaller-models-efficient-gpu-inference",
    #     "https://developers.redhat.com/articles/2025/04/02/practical-guide-llama-stack-nodejs-developers",
    #     "https://developers.redhat.com/articles/2025/04/05/llama-4-herd-here-day-zero-inference-support-vllm",
    #     "https://developers.redhat.com/articles/2025/04/30/retrieval-augmented-generation-llama-stack-and-nodejs",
    #     "https://developers.redhat.com/articles/2025/06/09/integrate-vllm-inference-macos-ios-llama-stack-apis",
    #     "https://developers.redhat.com/articles/2025/05/28/implement-ai-safeguards-nodejs-and-llama-stack",
    #     "https://developers.redhat.com/articles/2025/06/12/how-implement-observability-nodejs-and-llama-stack",
    #     "https://developers.redhat.com/articles/2025/07/22/react-vs-naive-prompt-chaining-llama-stack",
    #     "https://developers.redhat.com/articles/2025/07/08/ollama-or-vllm-how-choose-right-llm-serving-tool-your-use-case",
    #     "https://developers.redhat.com/articles/2025/07/15/exploring-llama-stack-python-tool-calling-and-agents",
    # ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml") # html.parser

        # for span_tag in soup.find_all('p'):
        #     new_tag = soup.new_tag("p")
        #     new_tag.string = span_tag.encode()
        #     span_tag.replace_with(new_tag)

        paragraphs = response.css('p::text').getall()
        for p_text in paragraphs:
             yield {
                "url": response.url, "title": soup.title.string,
                'paragraph': p_text
            }

        code = response.css('code::text').getall()
        for c_text in code:
             yield {
                "url": response.url, "title": soup.title.string,
                'code': c_text
            }
