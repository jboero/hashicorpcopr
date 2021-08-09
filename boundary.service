[Unit]
Description=Hashicorp Boundary service
After=syslog.target network.target local-fs.target remote-fs.target nss-lookup.target

[Service]
Type=simple
User=nomad
Group=nomad
ExecStart=/usr/bin/boundary server -config=/etc/boundary.d/boundary.hcl
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
