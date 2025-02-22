class notVim:
    def __init__(self, file_system):
        self.file_system = file_system
        self.current_file = None

    def open(self,filename):
        if filename in self.file_system.current_directory.file:
            self.current_file = self.file_system.current_directory.file[filename]
            print(self.current_file.data)
        else:
            print("Making new file.")
            self.file_system.create_file(filename,"")
            self.current_file = self.file_system.current_directory.file[filename]
    def write(self,content):

        if self.current_file is None:
            return
        self.current_file.data += content
        print(self.current_file.data)
    def save_and_close(self):
        if self.current_file is None:
            return
        self.file_system.save_file_system()
        print("File saved")
        self.current_file = None
    def run(self):
        print("<noVim> Type open <filename> to open file")
        while True:
            command = input("vim> ").strip()
            if command.startswith("open "):
                filename = "".join(command.split(" ")[1:])
                self.open(filename)
            elif command.startswith("write "):
                content = command.split(" ",1)[1]
                self.write(content)
            elif command.startswith("wq"):
                self.save_and_close()
                break
