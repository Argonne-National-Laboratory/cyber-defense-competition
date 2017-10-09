''' Sample OPC Items for testing purposes '''

import datetime
from PyOPC.OPCContainers import *

# Initial timestamp for all ItemValues
def_ts = datetime.datetime(2006, 2, 15, 12, 15, 18)


OPCItems = (

		(ItemContainer(ItemName='relay2_load',
                               Value=100,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                (OPCProperty(Name='accessRights',
                              Value='readWriteable'),)),

		(ItemContainer(ItemName='relay2_breaker',
                               Value=1,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                (OPCProperty(Name='accessRights',
                              Value='readWriteable'),)),

		(ItemContainer(ItemName='relay2_flow',
                               Value=100,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                (OPCProperty(Name='accessRights',
                              Value='readWriteable'),)))

