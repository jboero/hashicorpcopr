data_dir = "/var/lib/nomad/"

server {
  enabled          = true
  bootstrap_expect = 1
}

client {
  enabled          = true
  servers = ["127.0.0.1:4647"]
}
