class Emulator:
    def __init__(self):
        self.vfs_name = "vfs"
        self.running = True
    
    def parse_args(self, command_line):
        args = []
        current_arg = ""
        in_quotes = False
        quote_char = None
        
        for char in command_line:
            if char in ['"', "'"]:
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
                else:
                    current_arg += char
            elif char == ' ' and not in_quotes:
                if current_arg:
                    args.append(current_arg)
                    current_arg = ""
            else:
                current_arg += char
        
        if current_arg:
            args.append(current_arg)
        
        return args
    
    def execute_command(self, cmd_name, args):
        if cmd_name == "exit":
            if args:
                print("exit: слишком много аргументов")
            self.running = False
        
        elif cmd_name == "ls":
            print(f"ls: {' '.join(args)}")
        
        elif cmd_name == "cd":
            print(f"cd: {' '.join(args)}")
        
        else:
            print(f"{cmd_name}: команда не найдена")
    
    def run(self):
        while self.running:
            try:
                command_line = input(f"{self.vfs_name}$ ").strip()
                
                if not command_line: continue

                parts = self.parse_args(command_line)
                cmd_name = parts[0]
                args = parts[1:]

                self.execute_command(cmd_name, args)
                
            except EOFError: break
            except KeyboardInterrupt:
                print()
                continue

if __name__ == "__main__":
    emulator = Emulator()
    emulator.run()