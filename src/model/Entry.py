# Entry.py is a file that will build the needed entry objects to be sent to
# Our C++ gui

class Entry:
    
    def __init__(self, data):
        self.data = data

    

    def toCSV(self):
        print("To CSV Used")
        if isinstance(self.data,list):
            with open("test.csv","w") as f:
                f.write(','.join(self.data[0].keys()))
                f.write('\n')
                for row in self.data:
                    f.write(','.join(str(x) for x in row.values()))
                    f.write('\n')

                f.close()


    def __str__(self):
        return str(self.data) 

class WikiWrapper (Entry):
    def __init__(self, data):
        self.data = data
        super().__init__(self.data)
        
class WorldBankWrapper(Entry):
    def __init__(self,data):
        self.data = data
        super().__init__(self.data)


class AppleMusicWrapper(Entry):
	def __init__(self,data):
		self.data=data
		super().__init__(self.data)

class Wrapper(Entry):
    def __init__(self,data):
        self.data=data
        super().__init__(self.data)
#data = [{"title": "Mike","Description":"Mike is a man"}]
#e = Entry(data)
#e.toCSV()
#print(e)



