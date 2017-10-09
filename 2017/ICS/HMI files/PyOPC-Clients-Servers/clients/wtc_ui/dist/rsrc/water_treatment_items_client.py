from PyOPC.OPCContainers import *

WTCOPCItems = [ItemContainer(ItemName='TC0_PUMP_0'),
               ItemContainer(ItemName='TC0_PUMP_1'),
               ItemContainer(ItemName='TC0_VALVE_0'),
               ItemContainer(ItemName='TC0_VALVE_1'),
               ItemContainer(ItemName='TC0_VALVE_2'),
               ItemContainer(ItemName='TC0_VALVE_3'),
               ItemContainer(ItemName='TC0_VALVE_4'),
               ItemContainer(ItemName='TC0_PUMP_2'),
               ItemContainer(ItemName='TC0_VALVE_5'),
               ItemContainer(ItemName='TC0_VALVE_6'),
               ItemContainer(ItemName='TC0_SULF_ACID'),
               ItemContainer(ItemName='TC0_FERR_CH'),
               ItemContainer(ItemName='TC0_SOD_BI'),
               ItemContainer(ItemName='TC0_OZONE'),
               ItemContainer(ItemName='TC0_CHLORINE'),
               ItemContainer(ItemName='TC0_SOD_HYDRO'),
               ItemContainer(ItemName='TC0_UV0'),
               ItemContainer(ItemName='TC0_UV1'),
               ItemContainer(ItemName='TC0_UV2'),
               ItemContainer(ItemName='TC0_FLOUR'),
               ItemContainer(ItemName='TC0_ORTHO_PHOS'),
               ItemContainer(ItemName='H20_QUALITY')]

tc_master_tags = ['TC0_SULF_ACID', 'TC0_FERR_CH',
				  'TC0_PUMP_0', 'TC0_SOD_BI', 'TC0_OZONE',
				  'TC0_PUMP_1', 'TC0_VALVE_0', 'TC0_VALVE_1', 
				  'TC0_VALVE_2', 'TC0_VALVE_3', 'TC0_CHLORINE',
				  'TC0_SOD_HYDRO','TC0_PUMP_2', 'TC0_VALVE_4', 
				  'TC0_VALVE_5', 'TC0_VALVE_6', 'TC0_UV0', 
				  'TC0_UV1', 'TC0_UV2', 'TC0_FLOUR', 'TC0_ORTHO_PHOS']
              
PS0OPCItems = [ItemContainer(ItemName='PS0_PUMP_0'),
               ItemContainer(ItemName='PS0_PUMP_1'),
               ItemContainer(ItemName='PS0_VALVE_0'),
               ItemContainer(ItemName='PS0_VALVE_1'),
               ItemContainer(ItemName='PS0_CHLOR')]
               
PS1OPCItems = [ItemContainer(ItemName='PS1_PUMP_0'),
               ItemContainer(ItemName='PS1_PUMP_1'),
               ItemContainer(ItemName='PS1_VALVE_0'),
               ItemContainer(ItemName='PS1_VALVE_1'),
               ItemContainer(ItemName='PS1_CHLOR')]
               
PS2OPCItems = [ItemContainer(ItemName='PS2_PUMP_0'),
               ItemContainer(ItemName='PS2_PUMP_1'),
               ItemContainer(ItemName='PS2_VALVE_0'),
               ItemContainer(ItemName='PS2_VALVE_1'),
               ItemContainer(ItemName='PS2_CHLOR')]
               
PS3OPCItems = [ItemContainer(ItemName='PS3_PUMP_0'),
               ItemContainer(ItemName='PS3_PUMP_1'),
               ItemContainer(ItemName='PS3_VALVE_0'),
               ItemContainer(ItemName='PS3_VALVE_1'),
               ItemContainer(ItemName='PS3_CHLOR')]
               
PS4OPCItems = [ItemContainer(ItemName='PS4_PUMP_0'),
               ItemContainer(ItemName='PS4_PUMP_1'),
               ItemContainer(ItemName='PS4_VALVE_0'),
               ItemContainer(ItemName='PS4_VALVE_1'),
               ItemContainer(ItemName='PS4_CHLOR')]
               
PS5OPCItems = [ItemContainer(ItemName='PS5_PUMP_0'),
               ItemContainer(ItemName='PS5_PUMP_1'),
               ItemContainer(ItemName='PS5_VALVE_0'),
               ItemContainer(ItemName='PS5_VALVE_1'),
               ItemContainer(ItemName='PS5_CHLOR')]

ps0_master_tags = ['PS0_PUMP_0', 'PS0_PUMP_1', 'PS0_VALVE_0', 'PS0_VALVE_1', 'PS0_CHLOR']
ps1_master_tags = ['PS1_PUMP_0', 'PS1_PUMP_1', 'PS1_VALVE_0', 'PS1_VALVE_1', 'PS1_CHLOR']
ps2_master_tags = ['PS2_PUMP_0', 'PS2_PUMP_1', 'PS2_VALVE_0', 'PS2_VALVE_1', 'PS2_CHLOR']
ps3_master_tags = ['PS3_PUMP_0', 'PS3_PUMP_1', 'PS3_VALVE_0', 'PS3_VALVE_1', 'PS3_CHLOR']
ps4_master_tags = ['PS4_PUMP_0', 'PS4_PUMP_1', 'PS4_VALVE_0', 'PS4_VALVE_1', 'PS4_CHLOR']
ps5_master_tags = ['PS5_PUMP_0', 'PS5_PUMP_1', 'PS5_VALVE_0', 'PS5_VALVE_1', 'PS5_CHLOR']
