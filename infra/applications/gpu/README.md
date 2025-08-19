## gpu config

Time Slicing Enable.

1. Label the node

    ```bash
    oc label --overwrite node \
        --selector=nvidia.com/gpu.product=NVIDIA-L40S \
        nvidia.com/device-plugin.config=NVIDIA-L40S
    ```

2. Apply the config

    ```bash
    oc apply -k .
    ```

3. Check

    ```bash
    oc get $(oc get node -o name -l beta.kubernetes.io/instance-type=g6e.2xlarge) -o=jsonpath={.status.allocatable} | python -m json.tool
    ```
