# Kubernetes MCP Server

Manage Kubernetes clusters from OpenCode -- list pods, view logs, exec into containers, create/delete resources, and monitor resource usage.

**Package:** [`kubernetes-mcp-server`](https://www.npmjs.com/package/kubernetes-mcp-server)

## Prerequisites

- [Node.js](https://nodejs.org/) (v18+)
- A valid `~/.kube/config` with at least one cluster context configured
- `kubectl` access to the target cluster

## Configuration

Add the following to your `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "kubernetes": {
      "type": "local",
      "command": [
        "npx",
        "kubernetes-mcp-server@latest"
      ],
      "enabled": true
    }
  }
}
```

No additional environment variables needed -- it uses your existing kubeconfig.

## Cluster Context

The server uses the current context from your kubeconfig. You can switch contexts before launching OpenCode:

```bash
kubectl config use-context my-cluster
opencode
```

Or specify a context in your prompts:

```
List pods in the production namespace using the prod-cluster context
```

## Available Tools

### Cluster & Config
- `configuration_contexts_list` -- List all kubeconfig contexts
- `configuration_view` -- View current kubeconfig

### Pods
- `pods_list` / `pods_list_in_namespace` -- List pods with label/field selectors
- `pods_get` -- Get pod details
- `pods_log` -- View pod logs (with tail and container selection)
- `pods_exec` -- Execute commands inside containers
- `pods_run` -- Launch a new pod from an image
- `pods_delete` -- Delete a pod
- `pods_top` -- View pod CPU/memory usage

### Nodes
- `nodes_top` -- Node resource consumption
- `nodes_log` -- Node-level logs (kubelet, etc.)
- `nodes_stats_summary` -- Detailed node stats via kubelet Summary API

### Resources (Generic)
- `resources_list` -- List any resource type (Deployments, Services, Ingresses, etc.)
- `resources_get` -- Get a specific resource
- `resources_create_or_update` -- Apply YAML/JSON resource definitions
- `resources_delete` -- Delete any resource
- `resources_scale` -- Scale Deployments/StatefulSets

### Events & Namespaces
- `events_list` -- Cluster events for debugging
- `namespaces_list` -- List all namespaces

## Verification

After restarting OpenCode:

```
List all pods across all namespaces
```

```
Show me the logs for the nginx pod in the default namespace
```
