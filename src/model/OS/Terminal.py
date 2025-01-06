# The terminal version
import tkinter as tk

class Terminal:
    def __init__(self,initialInput,frame,dbEngine):
        self.root = frame
        self.command = initialInput
        self.scrollbar = None
        self.t = None
        self.t2 = None
        self.db = dbEngine

    def buildApp(self):
        #print("HI")
        try:
            self.t = tk.Text(self.root)
            self.scrollbar = tk.Scrollbar(self.root,command=self.t.yview)
            self.scrollbar.pack(side='right',fill='y',expand=True)
            self.t.configure(yscrollcommand=self.scrollbar.set)
            #self.scrollbar.configure(yscrollcommand=self.)
            #b = tk.Label(self.scrollbar,text=self.command)
            
            #b.pack(side='bottom',fill='x',expand=False,anchor='w')
            b = tk.Label(self.t,text=self.command)
            b.pack()
            self.t.window_create("end",window=b)
            self.t.insert("end","\n")
            self.t.pack(expand=True,fill=tk.BOTH)#,anchor='center')

            
            self.t2 = tk.Text(self.root,bg='black')#,fill='x',expand=False)
            self.t2.pack(side='bottom',fill='x',expand=False)
            
            self.t2.bind('<Return>',lambda e2: self.addCommand())

        
            
        except Exception as e:
            print("ERROR!!!",e)
    
    def addCommand(self):
        string = self.t2.get("1.0","end-1c").strip()
        
        b = tk.Label(self.t,text=string)
        b.pack()
        self.t.window_create("end",window=b)
        self.t.insert("end","\n")

        if string == 'clear':
            self.t.delete("1.0","end-1c")
        try:
            self.db.scan(string)
            self.db.parse()
            print("The final amount: ",self.db.getFlist())
            fList = self.db.getFlist()
            
            for line in fList:
                b1 = tk.Label(self.t,text=line.strip())
                b1.pack()
                self.t.window_create("end",window=b1)
                self.t.insert("end","\n")

        except Exception as e:
            print("Error compiling code: ",e)
            b1 = tk.Label(self.t,text=e,fg="red")
            b1.pack()
            self.t.window_create("end",window=b1)
            self.t.insert("end","\n")

        #self.t.window_create("end",window=b)
        #self.t.insert("end","\n")
        self.t2.delete("1.0","end-1c")
