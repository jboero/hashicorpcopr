# Hashicorp COPR Repo
RPM specs for COPR repos. This uses COPR build automation to provide a secure yum repo to RPM-based Linux distributions.  Supported versions and builds can be found here: https://copr.fedorainfracloud.org/coprs/boeroboy/hashicorp/

Current builds are only open source.  Enterprise editions may be added later.

To enable these repos for easy install and automatic updates, do the following (yum/dnf):

```
yum copr enable boeroboy/hashicorp
yum install vault
```
Note that as Hashicorp uses arch "amd64" instead of EL standard "x86_64" we can't use the standard ${\_arch} reference to build all architectures automatically.  Only x86_64 is supported currently.

Detailed build state can be found here: https://copr.fedorainfracloud.org/coprs/boeroboy/hashicorp/monitor/detailed
