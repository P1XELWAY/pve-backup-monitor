import sys
import requests
import json
import re
import urllib3
import dateutil.parser as parser
from dateutil.parser import parse
from datetime import datetime

urllib3.disable_warnings()


class PVEBackup:
    """
    Class to monitor PVE Backup from Zabbix Monitoring
    """
    REGEX=r'[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9]'
    MAX_DAYS = 2
    HOST = 'https://set_proxmox_host_here:8006'
    USERNAME = 'set username here !!!!'
    PASSWORD = 'set password here !!!!'

    csrf_prevention_token = None
    ticket = None

    def load_ticket(self):
        """
        Load ticket and csrf from proxmox rest API
        """
        api = '/api2/json/access/ticket'
        resp = requests.post(
            '{}{}?username={}&password={}'.format(self.HOST, api, self.USERNAME, self.PASSWORD), 
            verify=False,
        )
        if resp.status_code != 200:
            raise Exception('POST {} {}'.format(api, resp.status_code))
        if resp.content:
            content = json.loads(resp.content)
            data = content.get('data')
            self.csrf_prevention_token = data.get('CSRFPreventionToken')
            self.ticket = data.get('ticket')

    def get_backup_list(self, node):
        """
        Return list proxmox backup in selected node 
        """
        api = '/api2/json/nodes/proxmox/storage/{}/content'.format(node)    
        cookies = {
            'PVEAuthCookie': self.ticket
        } 
        headers = {
            'CSRFPreventionToken': self.csrf_prevention_token
        }
        resp = requests.get('{}{}'.format(self.HOST, api), verify=False, cookies=cookies, headers=headers)
        content = json.loads(resp.content)
        return content.get('data')

    def run(self, node):
        self.load_ticket()
        list=self.get_backup_list(node)
        delta=None
        success=False
        size=0
        if list:
            last_backup = list[-1]
            volid=last_backup.get('volid')
            size=last_backup.get('size')
            if re.search(self.REGEX, volid):
                found=re.findall(self.REGEX, volid)[0].replace('_', '.')
                parserinfo=parser.parserinfo(dayfirst=False, yearfirst=True)
                backup_date=parse(found, parserinfo)
                now=datetime.now()
                delta=now-backup_date
                days=delta.days
                success=delta.days<=self.MAX_DAYS
        return {
            "node": node,
            "delta": days,
            "success": success,
            "size": size,
            "mb": round(size / 1024000, 2) if size > 0 else size,
            "gb": round(size / 1024000000, 2) if size > 0 else size
        }

node='local' if len(sys.argv)==1 else sys.argv[1]
pveb=PVEBackup()
print(json.dumps(pveb.run(node)))