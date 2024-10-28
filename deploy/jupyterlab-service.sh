#!/bin/bash
# This script installs and enables/starts a systemd service
export NAME=Jupyter
WorkingDirectory=/home/thomas/workspace
User=thomas
Group=thomas

# Create service file
cat >/etc/systemd/system/${NAME}.service <<EOF
[Unit]
Description=${NAME}

[Service]
Type=simple
ExecStart=/usr/bin/env jupyter lab --ip=0.0.0.0 --no-browser --port 8888 --allow-root  --LabApp.token=''

WorkingDirectory=${WorkingDirectory}
User=${User}
Group=${Group}

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
source .venv/bin/activate
systemctl enable --now ${NAME}
systemctl start ${NAME}