PORT?=8321
NS_LLAMA?=llama-stack
NS_AGENT?=ai-agent
GITHUB_USER?=

.PHONY: port-forward
port-forward:
	@echo "Port-forwarding Llama Stack service on $(PORT)"
	oc -n $(NS_LLAMA) port-forward svc/llamastack-with-config-service $(PORT):$(PORT)

.PHONY: trigger-bad-run
trigger-bad-run:
	@if [ -z "$(GITHUB_USER)" ]; then echo "Set GITHUB_USER=<your-username>"; exit 1; fi
	oc -n $(NS_AGENT) create -f - <<'EOF'
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  generateName: agent-service-build-run-bad-
  namespace: $(NS_AGENT)
spec:
  taskRunTemplate:
    serviceAccountName: pipeline
  pipelineRef:
    name: agent-service-build
  params:
    - name: APP_NAME
      value: "ai-agent"
    - name: IMAGE_NAME
      value: "image-registry.openshift-image-registry.svc:5000/ai-agent/ai-agent"
    - name: GIT_REPO
      value: "https://github.com/$(GITHUB_USER)/etx-agentic-ai.git"
    - name: GIT_REVISION
      value: "bad"
    - name: PATH_CONTEXT
      value: "code"
  workspaces:
    - name: workspace
      volumeClaimTemplate:
        spec:
          accessModes: [ "ReadWriteOnce" ]
          resources:
            requests:
              storage: 3Gi
EOF




