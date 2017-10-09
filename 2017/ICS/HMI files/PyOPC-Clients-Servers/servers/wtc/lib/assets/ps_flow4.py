#Test Tags to see if this is actually working
#Syntax (name, failValue, cmp_op, [previous_nodes], [next_nodes], startValue)
tags = [('PS2_DEST_NET', '0', '==', None, ['PS4_PUMP_0', 'PS4_PUMP_1'], '1'),
		('PS4_PUMP_0', '0', '==', ['PS2_DEST_NET'], ['PS4_VALVE_0'], '1'),
		('PS4_PUMP_1', '0', '==', ['PS2_DEST_NET'], ['PS4_VALVE_1'], '1'),	
		('PS4_VALVE_0', '0', '==', ['PS4_PUMP_0'], ['PS4_DEST_NET'], '1'), 
		('PS4_VALVE_1', '0', '==', ['PS4_PUMP_1'], ['PS4_DEST_NET'], '1'),
		('PS4_DEST_NET', '0', '==', ['PS4_VALVE_1', 'PS4_VALVE_0'], None, '1')]
