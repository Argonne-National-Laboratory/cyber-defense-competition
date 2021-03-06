import datetime
import random
from PyOPC.OPCContainers import *

# Initial timestamp for all ItemValues
def_ts = datetime.datetime(2006, 2, 15, 12, 15, 18)

WTCOPCItems = ((ItemContainer(ItemName='PS5_PUMP_0',
                               Value=1,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                 (OPCProperty(Name='accessRights',
                              Value='readWritable'),
                  OPCProperty(Name='description',
                              Value='Pumping Station 6 Pump 1'))),
            (ItemContainer(ItemName='PS5_PUMP_1',
                               Value=1,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                 (OPCProperty(Name='accessRights',
                              Value='readWritable'),
                  OPCProperty(Name='description',
                              Value='Pumping Station 6 Backup Pump'))),
            (ItemContainer(ItemName='PS5_VALVE_0',
                               Value=1,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                 (OPCProperty(Name='accessRights',
                              Value='readWritable'),
                  OPCProperty(Name='description',
                              Value='Pumping Station 6 Valve 1'))),
                 (ItemContainer(ItemName='PS5_VALVE_1',
                               Value=1,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                 (OPCProperty(Name='accessRights',
                              Value='readWritable'),
                  OPCProperty(Name='description',
                              Value='Pumping Station 6 Valve 2'))),
				(ItemContainer(ItemName='PS5_CHLOR',
                               Value=1,
                               Timestamp=def_ts,
                               QualityField='good',
                               LimitField='none',
                               VendorField=0),
                 (OPCProperty(Name='accessRights',
                              Value='readWritable'),
				  OPCProperty(Name='description',
                              Value='Pumping Station 6 Chlorine Tank'))))
