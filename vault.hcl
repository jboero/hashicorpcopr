# Example Vault config
# jboero@hashicorp.com - for Vault v1.2.4

ui = true
#mlock = true
#disable_mlock = true

backend "file" {
  path = "/var/lib/vault/"
#  path = "/var/lib/vault2/"
}

# https://www.vaultproject.io/docs/configuration/storage/raft
#storage "raft" {
#  path="/var/lib/vault"
#}

#storage "consul" {
#  address = "127.0.0.1:8500"
#  path    = "vault"
#}

# HTTP listener
listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = 1
}

# HTTPS listener
#listener "tcp" {
#  address = "127.0.0.1:8200"
#  tls_cert_file = "/etc/pki/self.crt"
#  tls_key_file = "/etc/pki/self.key"
#}

# Example AWS KMS auto unseal
#seal "awskms" {
#  region = "us-east-1"
#  kms_key_id = "d7c1ffd9-8cce-45e7-be4a-bb38dd205966"
#}

# Example HSM auto unseal
#seal "pkcs11" {
#  lib            = "/usr/vault/lib/libCryptoki2_64.so"
#  slot           = "0"
#  pin            = "AAAA-BBBB-CCCC-DDDD"
#  key_label      = "vault-hsm-key"
#  hmac_key_label = "vault-hsm-hmac-key"
#}
