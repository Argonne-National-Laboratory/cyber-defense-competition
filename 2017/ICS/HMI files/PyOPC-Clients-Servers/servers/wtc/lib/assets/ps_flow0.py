#Test Tags to see if this is actually working
#Syntax (name, failValue, cmp_op, [previous_nodes], [next_nodes], startValue)
tags = [('RESEVOIR', '0', '==', None, ['PS0_PUMP_0', 'PS0_PUMP_1'], '1'),
		('PS0_PUMP_0', '0', '==', ['RESEVOIR'], ['PS0_VALVE_0'], '1'),
		('PS0_PUMP_1', '0', '==', ['RESEVOIR'], ['PS0_VALVE_1'], '1'),	
		('PS0_VALVE_0', '0', '==', ['PS0_PUMP_0'], ['PS0_DEST_NET'], '1'), 
		('PS0_VALVE_1', '0', '==', ['PS0_PUMP_1'], ['PS0_DEST_NET'], '1'),
		('PS0_DEST_NET', '0', '==', ['PS0_VALVE_1', 'PS0_VALVE_0'], None, '1')]
