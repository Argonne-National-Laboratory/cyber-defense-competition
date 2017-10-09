import datetime
import random
from PyOPC.OPCContainers import *

# Initial timestamp for all ItemValues
def_ts = datetime.datetime(2006, 2, 15, 12, 15, 18)

WTCOPCItems = ((ItemContainer(ItemName='PUMP',
                               Value=1,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                 (OPCProperty(Name='accessRights',
                              Value='readWritable'),
                  OPCProperty(Name='description',
                              Value='Pump'))),)
