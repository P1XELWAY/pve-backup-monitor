# pve-backup-monitor
Proxmox Backup Monitoring script for Zabbix

## Installation of the script.

Open ssh on target server and type :

<pre>
    sudo -i
    chmod a+rw /opt
    cd /opt
    git clone ...
    mv pve-backup-monitor pve
    cd pve
    pip install -r requirements.txt
    chmod +x run.sh
</pre>

Upgrade main.py values :

<pre>
HOST = 'https://set_proxmox_host_here:8006'
USERNAME = 'set username here !!!!'
PASSWORD = 'set password here !!!!'
</pre>

## Zabbix agent configuration

Add EnableRemoteCommands=1 option

## Zabbix configuration

1. Create new template
2. Create new application
3. Add new item, for example:
<br>
<br>
    Name : CI-APP-BACKUP<br>
    Type : Zabbix Agent<br>
    Key : system.run[/opt/pve/run.sh CI-APP-BACKUP]<br>
    Applications: select created application<br>

4. Add new trigger to call the item

<hr>

Monitoring:
<img src="img/monitoring.png" />

<hr>

Items:
<img src="img/items.png" />

Item edit:
<img src="img/item_edit.png" />

Item edit preprocessing:
<img src="img/item_edit_preprocessing.png" />

<hr>

Triggers:
<img src="img/triggers.png" />

Trigger edit:
<img src="img/trigger_edit.png" />