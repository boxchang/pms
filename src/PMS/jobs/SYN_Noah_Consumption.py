import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from PMS.database import database
from jobs.func import get_ip

class SYN_Noah_Consumption(object):
    db = None
    PROD = False
    DC_SCHEMA = None
    WMS_SCHEMA = None
    IP = None

    def __init__(self, PROD):
        self.IP = get_ip()
        self.PROD = PROD
        if PROD:
            self.DC_SCHEMA = "DC.dbo"
            self.WMS_SCHEMA = "WMS2.dbo"
        else:
            self.DC_SCHEMA = "DC_Dev.dbo"
            self.WMS_SCHEMA = "WMS2_Dev.dbo"
        self.db = database()