### Creating a new Daemon service on the Pi

`cd /etc/systemd/system/`

`sudo nano myScriptName.service`

Paste the following into nano, providing the file paths * *:
----------------------------------------------------------------
<div>
[Unit]<br>
Description=My Script Service<br>
After=network-online.target<br>
Wants=network-online.target<br>
<br>
[Service]<br>
Type=simple<br>
ExecStart=/usr/bin/python "Location of script here" > /home/pi/Documents/Code/ 2>&1<br>
WorkingDirectory= "Directory to run code here"<br>
User=pi<br>
Restart=always<br>
RestartSec=120<br>
<br>
[Install]<br>
WantedBy=multi-user.target<br>
<div/>
----------------------------------------------------------------

Give service permission: 

`sudo chmod 644 /etc/systemd/system/myScriptName.service`

Configure system:

`sudo systemctl daemon-reload`\
`sudo systemctl enable myScriptName.service`

Check Status:

`sudo systemctl status myScriptName.service`
