Run `helm template` with the current chart and set the output directory to the tenant.
In a real project you would likely have a dedicated repo for the tenant workload and the tenant subdirectory would refer out to that repo.

Below is a specific example of using this command to create a new set of manifests:

```sh
helm template demo-pipeline . --values values.yaml --output-dir ../../../infra/tenants/tenant-name/base/sno
```