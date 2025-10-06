import sys


class Emulator:
    def __init__(self, vfs_path=None, script_path=None):
        self.vfs_name = "vfs"
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.running = True

        print(f"Параметры запуска:")
        print(f"  VFS путь: {vfs_path or 'не указан'}")
        print(f"  Скрипт: {script_path or 'не указан'}")
        print("-" * 40)

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
                return False
            self.running = False
            return True

        elif cmd_name == "ls":
            print(f"ls: {' '.join(args)}")

        elif cmd_name == "cd":
            print(f"cd: {' '.join(args)}")

        elif cmd_name == "echo":
            print(f"{' '.join(args)}")

        else:
            print(f"{cmd_name}: команда не найдена")

    def execute_script(self, script_path):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    if not line or line.startswith('#'):
                        continue

                    print(f"{self.vfs_name}$ {line}")

                    parts = self.parse_args(line)
                    if not parts:
                        continue

                    cmd_name = parts[0]
                    args = parts[1:]

                    self.execute_command(cmd_name, args)

        except FileNotFoundError:
            print(f"Ошибка: скрипт '{script_path}' не найден")
            return False
        except Exception as e:
            print(f"Ошибка выполнения скрипта (строка {line_num}): {e}")
            return False

        return True

    def run(self):
        if self.script_path:
            if not self.execute_script(self.script_path):
                return

        while self.running:
            try:
                command_line = input(f"{self.vfs_name}$ ").strip()

                if not command_line:
                    continue

                parts = self.parse_args(command_line)
                cmd_name = parts[0]
                args = parts[1:]

                self.execute_command(cmd_name, args)

            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                continue


def main():
    vfs_path = None
    script_path = None

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--vfs" and i + 1 < len(sys.argv):
            vfs_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--script" and i + 1 < len(sys.argv):
            script_path = sys.argv[i + 1]
            i += 2
        else:
            print(f"Неизвестный параметр: {sys.argv[i]}")
            i += 1

    emulator = Emulator(vfs_path, script_path)
    emulator.run()


if __name__ == "__main__":
    main()