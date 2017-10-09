''' Sample OPC Items for testing purposes '''

import datetime
from PyOPC.OPCContainers import *

# Initial timestamp for all ItemValues
def_ts = datetime.datetime(2006, 2, 15, 12, 15, 18)

TestOPCItems = ((ItemContainer(ItemName='water_flow',
                               Value=100,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
		(OPCProperty(Name='accessRights',
                              Value='readWriteable'),
		OPCProperty(Name='description',
                              Value='Integer Item'))),
		(ItemContainer(ItemName='vat',
                               Value=0,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                (OPCProperty(Name='accessRights',
                              Value='readWriteable'),)),
		(ItemContainer(ItemName='steam',
				Value=0,
				Timestamp=def_ts,
				QualityField='good',
				LimitField='none',
				VendorField=0),
		(OPCProperty(Name='accessRights',
				Value='readWriteable'),)),
		(ItemContainer(ItemName="valve1",
				Value=0,
				Timestamp=def_ts),
		(OPCProperty(Name='accessRights',
				Value='readWritable'),)),
		(ItemContainer(ItemName="switch",
				Value=1,
				Timestamp=def_ts,
				QualityField='good',
				LimitField='none',
				VendorField=0),
		(OPCProperty(Name='accessRights',
				Value='readWritable'),)))
