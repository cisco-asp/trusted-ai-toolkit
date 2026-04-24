# NetBox MCP Server

Query [NetBox](https://netbox.dev/) infrastructure data (devices, sites, IPs, VLANs, circuits, and more) directly from OpenCode.

**Package:** [`netbox-mcp-server`](https://github.com/netbox-community/netbox-mcp-server) (Python, installed via `uv`)

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- A running NetBox instance
- A NetBox API token

## Generating a NetBox API Token

1. Log in to your NetBox instance
2. Navigate to your user profile (top right) > **API Tokens**
3. Click **Add a token**, configure permissions, and copy the token value

## Installation

Clone the NetBox MCP server:

```bash
git clone https://github.com/netbox-community/netbox-mcp-server.git ~/sw_projects/netbox_mcp
cd ~/sw_projects/netbox_mcp
uv sync
```

## Configuration

Add the following to your `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "netbox": {
      "type": "local",
      "command": [
        "uv",
        "--directory",
        "/path/to/netbox_mcp",
        "run",
        "netbox-mcp-server"
      ],
      "environment": {
        "NETBOX_URL": "https://your-netbox-instance.example.com/",
        "NETBOX_TOKEN": "YOUR_NETBOX_API_TOKEN",
        "VERIFY_SSL": "false"
      },
      "enabled": true
    }
  }
}
```

Replace:
- `/path/to/netbox_mcp` with the absolute path to your cloned repo
- `NETBOX_URL` with your NetBox instance URL
- `NETBOX_TOKEN` with your API token
- Set `VERIFY_SSL` to `"true"` if your NetBox instance has a valid TLS certificate

## Available Tools

- `netbox_get_objects` -- Query any NetBox object type with filtering, sorting, pagination
- `netbox_get_object_by_id` -- Get detailed info on a specific object
- `netbox_search_objects` -- Global search across devices, sites, IPs, interfaces, etc.
- `netbox_get_changelogs` -- View change history for objects

### Supported Object Types

Devices, sites, racks, interfaces, IP addresses, prefixes, VLANs, VRFs, circuits, virtual machines, cables, and many more. The full list covers DCIM, IPAM, circuits, virtualization, VPN, and wireless resources.

## Verification

After restarting OpenCode:

```
List all devices in NetBox
```

```
Search NetBox for any device named "router"
```
