# Basic Nomad configuration for single server+agent locally.
# John Boero - jboero@hashicorp.com
# https://www.nomadproject.io/docs/configuration/index.html

datacenter = "dc1"
data_dir   = "/var/lib/nomad/"

bind_addr  = "127.0.0.1"

advertise {
        http    = "127.0.0.1"
        rpc     = "127.0.0.1"
        serf    = "127.0.0.1"
}

server {
        enabled = true
}

client {
        enabled = true
}

consul {
        address = "127.0.0.1:8500"
}
