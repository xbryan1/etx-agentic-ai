## building custom llama-stack distribution

Build a custom llama-stack distro image for providers - vllm::remote, inline::rag-runtime, remote::model-context-protocol, remote::tavily-search

See:

- https://github.com/llamastack/llama-stack/blob/main/docs/source/distributions/building_distro.md

```bash
git clone git@github.com:meta-llama/llama-stack.git llama-stack-clean

cd ~/git/llama-stack-clean

-- build llama-stack
export USE_COPY_NOT_MOUNT="true"
export LLAMA_STACK_DIR="."
export CONTAINER_BINARY=podman

uv run llama stack build --config build.yaml
podman tag localhost/ubi9-test:dev quay.io/eformat/distribution-remote-vllm:latest
podman tag localhost/ubi9-test:dev quay.io/eformat/distribution-remote-vllm:0.2.15
podman push quay.io/eformat/distribution-remote-vllm:latest
podman push quay.io/eformat/distribution-remote-vllm:0.2.15
```
