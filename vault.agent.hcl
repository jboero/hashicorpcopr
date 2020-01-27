pid_file = "./pidfile"

vault {
        address = "https://127.0.0.1:8200"
}

auto_auth {
        method "aws" {
                mount_path = "auth/aws-subaccount"
                config = {
                        type = "iam"
                        role = "foobar"
                }
        }

        sink "file" {
                config = {
                        path = "/tmp/file-foo"
                }
        }

        sink "file" {
                wrap_ttl = "5m"
                aad_env_var = "TEST_AAD_ENV"
                dh_type = "curve25519"
                dh_path = "/tmp/file-foo-dhpath2"
                config = {
                        path = "/tmp/file-bar"
                }
        }
}

cache {
        use_auto_auth_token = true
}

listener "unix" {
         address = "/var/run/vaultagent.sock"
         tls_disable = true
}

listener "tcp" {
         address = "127.0.0.1:8100"
         tls_disable = true
}

#template {
#  source      = "/etc/vault/server.key.ctmpl"
#  destination = "/etc/vault/server.key"
#}

#template {
#  source      = "/etc/vault/server.crt.ctmpl"
#  destination = "/etc/vault/server.crt"
#}
