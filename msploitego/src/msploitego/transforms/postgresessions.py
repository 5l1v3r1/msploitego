from pprint import pprint

from datetime import datetime

from common.MaltegoTransform import *
from common.postgresdb import MsploitPostgres
import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    db = mt.getValue()
    user = mt.getVar("user")
    password = mt.getVar("password").replace("\\", "")
    mpost = MsploitPostgres(user, password, db)
    for session in mpost.getForAllHosts("sessions"):
        sessionentity = mt.addEntity("msploitego.MeterpreterSession", str(session.get("id")))
        sessionentity.setValue(str(session.get("id")))
        for k,v in session.items():
            if isinstance(v,datetime):
                sessionentity.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                sessionentity.addAdditionalFields(k, k.capitalize(), False, str(v))
        sessionentity.addAdditionalFields("user", "User", False, user)
        sessionentity.addAdditionalFields("password", "Password", False, password)
        sessionentity.addAdditionalFields("db", "db", False, db)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['postgreshosts.py', 'msf', 'properties.postgresdatabase=msf']
# dotransform(args)