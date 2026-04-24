---
name: cisco-config-lookup
description: Search cisco.com configuration guides and command references for Cisco IOS-XR platforms. Use when you need to verify feature support, find CLI syntax, get configuration examples, or cite official Cisco documentation for any IOS-XR platform (Cisco 8000, ASR 9000, NCS 5500, NCS 540, NCS 560, XRd, etc.).
---

# Cisco IOS-XR Configuration Guide Lookup

## When to Use This Skill

This is the **first and primary lookup method** for every RFP requirement. Use it before checking local Boiler Plate, Feature Matrix, Scale Sheet, or Airtable data.

Use this skill to:
- Verify whether a feature is supported on a specific Cisco IOS-XR platform
- Find CLI command syntax or configuration examples
- Cite official cisco.com documentation in RFP Supplier Comments
- Confirm compliance codes with authoritative documentation

---

## Search Tools

Use either tool depending on what you need:

| Need | Tool |
|------|------|
| Quick citation + summary | `websearch_cited` |
| Read a full documentation page | `WebFetch` |

---

## Search Query Patterns

### Feature support on a platform
```
site:cisco.com/c/en/us/td/docs/iosxr "<feature>" "<platform>" supported
```
Examples:
```
site:cisco.com/c/en/us/td/docs/iosxr "MoFRR" "8000" supported
site:cisco.com/c/en/us/td/docs/iosxr "Flex-Algo" "8000" configuration
site:cisco.com/c/en/us/td/docs/iosxr "TWAMP" "8000" configuration guide
```

### CLI command syntax
```
site:cisco.com/c/en/us/td/docs/iosxr "<command keyword>" "cisco 8000" command reference
```
Examples:
```
site:cisco.com/c/en/us/td/docs/iosxr "snmp-server trap-source" cisco 8000
site:cisco.com/c/en/us/td/docs/iosxr "ipv4 redirects disable" cisco 8000
site:cisco.com/c/en/us/td/docs/iosxr "bgp allowas-in" cisco 8000
```

### RFC compliance
```
site:cisco.com/c/en/us/td/docs/iosxr RFC <number> "cisco 8000"
```

### Release-specific availability
```
site:cisco.com/c/en/us/td/docs/iosxr "<feature>" "26.2" "8000" release notes
```

---

## Cisco IOS-XR Documentation Hubs (WebFetch starting points)

| Platform | Documentation Hub URL |
|----------|-----------------------|
| Cisco 8000 Series | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000.html` |
| ASR 9000 | `https://www.cisco.com/c/en/us/td/docs/iosxr/asr9000.html` |
| NCS 5500 / 5700 | `https://www.cisco.com/c/en/us/td/docs/iosxr/ncs5500.html` |
| NCS 540 | `https://www.cisco.com/c/en/us/td/docs/iosxr/ncs540.html` |
| NCS 560 | `https://www.cisco.com/c/en/us/td/docs/iosxr/ncs560.html` |
| XRd | `https://www.cisco.com/c/en/us/td/docs/iosxr/xrd.html` |

---

## Cisco 8000 Direct Guide URLs (IOS-XR 26.x)

Use these with WebFetch when you know which guide applies:

| Topic | URL |
|-------|-----|
| BGP | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/bgp/26xx/configuration/guide/b-bgp-cg-cisco8000-26xx.html` |
| Routing (IS-IS, OSPF) | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/routing/26xx/configuration/guide/b-routing-cg-cisco8000-26xx.html` |
| MPLS | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/mpls/26xx/configuration/guide/b-mpls-cg-cisco8000-26xx.html` |
| Segment Routing | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/26xx/configuration/guide/b-segment-routing-cg-cisco8000-26xx.html` |
| SRv6 | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/26xx/configuration/guide/b-srv6-configuration-guide-cisco8000-26xx.html` |
| EVPN | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/evpn/26xx/configuration/guide/b-evpn-config-cisco8000-26xx.html` |
| L2VPN | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/l2vpn/26xx/configuration/guide/b-l2vpn-cg-cisco8000-26xx.html` |
| L3VPN | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/vpn/26xx/configuration/guide/b-l3vpn-cg-cisco8000-26xx.html` |
| QoS | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/qos/26xx/configuration/guide/b-modular-qos-config-cisco8000-26xx.html` |
| Multicast | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/multicast/26xx/configuration/guide/b-multicast-cg-cisco8k-r26xx.html` |
| Interfaces & BFD | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/interfaces/26xx/configuration/guide/b-interfaces-config-guide-cisco8k-r26xx.html` |
| IP Addresses & ACL | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/ip-addresses/26xx/configuration/guide/b-ip-addresses-cg-8k-26xx.html` |
| Security (AAA, SSH, LPTS) | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/security/26xx/configuration/guide/b-system-security-cg-cisco8000-26xx.html` |
| MACsec | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/security/26xx/configuration/guide/b-macsec-encryption-config-cisco8000-26xx.html` |
| System Management (SNMP, NTP) | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/system-management/26xx/configuration/guide/b-system-management-cg-8k-26xx.html` |
| System Monitoring (Syslog, EEM) | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/system-monitoring/26xx/configuration/guide/b-system-monitoring-cg-cisco8k-26xx.html` |
| Traffic Mirroring / SPAN | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/traffic-monitoring/26xx/configuration/guide/b-traffic-mirroring-configuration-guide-cisco8k-26xx.html` |
| NetFlow / IPFIX | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/netflow/26xx/configuration/guide/b-netflow-configuration-ios-xr-8000-26xx.html` |
| Telemetry (gNMI, gRPC) | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/telemetry/26xx/configuration/guide/b-telemetry-cg-8000-26xx.html` |
| Programmability (NETCONF, YANG) | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/programmability/26xx/configuration/guide/b-programmability-configuration-guide-cisco8000-26xx.html` |
| Timing & Sync (PTP, SyncE) | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/timing/26xx/configuration/guide/b-timing-sync-config-guide-cisco8000-26xx.html` |
| Software Install / ISSU | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/setup-upgrade/26xx/configuration/guide/b-setup-and-upgrade-cisco8k-26xx.html` |

---

## Topic-to-Guide Mapping

| Requirement topic | Guide to fetch |
|-------------------|---------------|
| BGP, AS-path, communities, route reflector | BGP |
| IS-IS, OSPF, static routes, redistribution | Routing |
| MPLS, LDP, RSVP-TE | MPLS |
| SR-MPLS, TI-LFA, SR-TE, PCE, Flex-Algo | Segment Routing |
| SRv6, uSID | SRv6 |
| EVPN, MAC/IP route types | EVPN |
| VPWS, VPLS, pseudowire | L2VPN |
| VRF, MP-BGP VPNv4/v6 | L3VPN |
| DSCP, WRED, H-QoS, shaping, policing | QoS |
| PIM, IGMP, MSDP, Multicast VPN | Multicast |
| Ethernet, LAG, LACP, BFD, OAM | Interfaces & BFD |
| ACL, prefix-list, LPTS, DHCP | IP Addresses & ACL |
| AAA, TACACS+, RADIUS, LDAP, SSH, password policy | Security |
| MACsec, 802.1AE | MACsec |
| SNMP, NTP, NTP auth, system users | System Management |
| Syslog, EEM, SPAN, RMON | System Monitoring |
| ERSPAN, local SPAN, traffic mirroring | Traffic Mirroring |
| NetFlow v9, IPFIX, sFlow | NetFlow / IPFIX |
| gNMI, gRPC, streaming telemetry | Telemetry |
| NETCONF, RESTCONF, YANG, NACM | Programmability |
| PTP (IEEE 1588v2), SyncE, NTP | Timing & Sync |
| ISSU, SMU, install rollback | Software Install |

---

## Additional Cisco Resources

| Resource | URL |
|----------|-----|
| Cisco Feature Navigator (cross-platform) | `https://cfnng.cisco.com/` |
| IOS-XR 8000 Release Notes 26.x | `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/release-notes/26xx/b-release-notes-cisco8000-r26xx.html` |
| Cisco 8608 Data Sheet | `https://www.cisco.com/c/en/us/products/collateral/routers/8000-series-routers/datasheet-c78-744356.html` |
| Cisco Security Advisories (PSIRT) | `https://sec.cloudapps.cisco.com/security/center/publicationListing.x` |

---

## Citing Sources in Responses

When using cisco.com content, format citations as:

```
[Source: Cisco IOS-XR <Guide Name>, Release <version>, cisco.com]
```

Examples:
- `[Source: Cisco IOS-XR BGP Configuration Guide for Cisco 8000, Release 26.x, cisco.com]`
- `[Source: Cisco IOS-XR System Security Configuration Guide for Cisco 8000, Release 26.x, cisco.com]`
- `[Source: Cisco Feature Navigator, cisco.com]`

Include the direct URL when available:
```
[Source: Cisco IOS-XR Segment Routing Configuration Guide, https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/26xx/configuration/guide/b-segment-routing-cg-cisco8000-26xx.html]
```

---

## If a URL Returns 404

1. Fetch the platform documentation hub (e.g. `https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000.html`) to find the current URL structure.
2. Fall back to `websearch_cited` with `site:cisco.com` to locate the correct page.
