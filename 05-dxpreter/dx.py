import os
import re
import sys
import enum


class DataTypes(enum.Enum):
    """DataTypes are the supported types of data which we can do work on."""
    Int = "int"
    Str = "str"


class Interpreter:
    variables: dict[str, tuple[DataTypes, str]]

    def __init__(self) -> None:
        self.variables = {
            # Standard variable: pwd
            # includes the current working directory path.
            "pwd": (DataTypes.Str, os.getcwd()),
        }

    def parse_and_execute(self, line: str):
        line = line.strip()

        if line == "":
            # Ignore empty lines
            return
        elif line.startswith("//"):
            # Ignore comment lines
            return

        # If the line is a variable, we parse it and save it
        # into the instance's variables.
        res = self.__match_variable(line)
        if res is not None:
            dtype, name, value = res.groups()

            data_type = DataTypes(dtype)

            if data_type == DataTypes.Int:
                self.variables[name] = (data_type, value)
            elif data_type == DataTypes.Str:
                value = value.strip('"').strip("'")
                self.variables[name] = (data_type, value)
            else:
                raise Exception("unsupported data type")

            return

        # If the line is a "log" function, we just print it out.
        res = self.__match_std_log(line)
        if res is not None:
            print(res.group(1))
            return

        # If the line is a "log formatter" function, we need to
        # update the message and the print it out.
        res = self.__match_std_log_formatter(line)
        if res is not None:
            raw_var_names, message = res.groups()

            var_names = list(map(lambda txt: txt.strip(), raw_var_names.split(",")))

            for var_name in var_names:
                var = self.variables.get(var_name)
                if var is None:
                    raise Exception(f"Variable {var_name} is not defined")

                # Update the message with the variable names.
                data_type, value = var
                if data_type == DataTypes.Int:
                    message = message.replace("%int%", value, 1)
                elif data_type == DataTypes.Str:
                    message = message.replace("%str%", value, 1)
                else:
                    raise Exception(f"variable {var_name} has an unsupported data type {data_type}")

            print(message)
            return

        raise Exception("Invalid or unsupported syntax")

    @staticmethod
    def __match_variable(line: str) -> re.Match[str] | None:
        """Matches for `[data_type] [variable_name] = [value]`"""
        pattern = r'^(int|str)\s([a-zA-Z][a-zA-Z0-9_]+)\s=\s(.+)$'

        return re.match(pattern, line)

    @staticmethod
    def __match_std_log(line: str) -> re.Match[str] | None:
        """Matches for `log("Hello World")`"""
        pattern = r'^log\("(.*?)"\)$'

        return re.match(pattern, line)

    @staticmethod
    def __match_std_log_formatter(line: str) -> re.Match[str] | None:
        """Matches for `log[var_name1, var_name2, ...]("Hello %str%")`"""
        pattern = r'^log\[([a-zA-Z][a-zA-Z0-9_]+(?:\s*,\s*[a-zA-Z][a-zA-Z0-9_]+)*)\]\("(.*?)"\)$'

        return re.match(pattern, line)


class Runtime:
    file_path: str
    interpreter: Interpreter

    def __init__(self) -> None:
        self.interpreter = Interpreter()

        if len(sys.argv) >= 2:
            self.file_path = sys.argv[1]

    def start(self):
        if self.file_path:
            self.__run_file()
        else:
            self.__run_shell()

    def __run_shell(self):
        print("DXPreter started.")
        print("Start writing your code! (type 'exit' to exit)")

        while True:
            try:
                line = input(">> ")
                if line == 'exit':
                    break

                try:
                    self.interpreter.parse_and_execute(line)
                except Exception as error:
                    print(f"Syntax Error: {error}")
            except KeyboardInterrupt:
                break
            finally:
                print("\nExiting...")

    def __run_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line_index, line in enumerate(file.readlines()):
                    try:
                        self.interpreter.parse_and_execute(line)
                    except Exception as error:
                        print(f"Syntax Error on line {line_index+1}: {error}")
        except FileNotFoundError:
            print("There's no such a file to run!")
        except Exception as error:
            print(f"An error occurred! {error}")


if __name__ == "__main__":
    runtime = Runtime()
    runtime.start()
