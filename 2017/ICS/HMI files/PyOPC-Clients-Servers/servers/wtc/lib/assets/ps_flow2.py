#Test Tags to see if this is actually working
#Syntax (name, failValue, cmp_op, [previous_nodes], [next_nodes], startValue)
tags = [('PS1_DEST_NET', '0', '==', None, ['PS2_PUMP_0', 'PS2_PUMP_1'], '1'),
		('PS2_PUMP_0', '0', '==', ['PS1_DEST_NET'], ['PS2_VALVE_0'], '1'),
		('PS2_PUMP_1', '0', '==', ['PS1_DEST_NET'], ['PS2_VALVE_1'], '1'),	
		('PS2_VALVE_0', '0', '==', ['PS2_PUMP_0'], ['PS2_DEST_NET'], '1'), 
		('PS2_VALVE_1', '0', '==', ['PS2_PUMP_1'], ['PS2_DEST_NET'], '1'),
		('PS2_DEST_NET', '0', '==', ['PS2_VALVE_1', 'PS2_VALVE_0'], None, '1')]
