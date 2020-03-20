# Basic Nomad configuration for single server+agent locally.
# John Boero - jboero@hashicorp.com
# https://www.nomadproject.io/docs/configuration/index.html

datacenter = "dc1"
data_dir   = "/var/lib/nomad/"

bind_addr  = "0.0.0.0"

server {
        enabled = false
}

client {
        enabled = true
        servers = [""]
}

consul {
        address = "127.0.0.1:8500"
}
