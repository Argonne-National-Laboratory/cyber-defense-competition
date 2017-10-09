class OPCItem:
     def __init__(self, name, value):
         self._observers = []
         self.name = name
         self.value = value

     def bind_to(self, callback):
         self._observers.append(callback)

     def getValue(self):
         return self.value

     def setValue(self, value):
         self.value = value
         print 'in setValue'
         for callback in self._observers:
             callback(self.value)

class OPCHolder:
     def __init__(self, inIClist):
         self.OPC = {}
         for skip, item in enumerate(inIClist):
             self.OPC[item.ItemName] = OPCItem(item.ItemName, item.Value)

     def PollUpdate(self, inIClist):
         for skip, item in enumerate(inIClist):
             self.OPC[item.ItemName].setValue(item.Value)