''' Sample OPC Items for testing purposes '''

import datetime
from PyOPC.OPCContainers import *

# Initial timestamp for all ItemValues
def_ts = datetime.datetime(2006, 2, 15, 12, 15, 18)

TestOPCItems = ((ItemContainer(ItemName='generation',
                               Value=100.0,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                (OPCProperty(Name='accessRights',
                              Value='readWriteable'),)),

		(ItemContainer(ItemName='load',
                               Value=100.0,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                (OPCProperty(Name='accessRights',
                              Value='readWriteable'),)),

		(ItemContainer(ItemName='breaker',
                               Value=1,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                (OPCProperty(Name='accessRights',
                              Value='readWriteable'),)),

		(ItemContainer(ItemName='flow',
                               Value=100.0,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                (OPCProperty(Name='accessRights',
                              Value='readWriteable'),)))


