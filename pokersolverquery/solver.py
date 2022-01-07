import subprocess
import os
import pathlib


class SolverException(Exception):
    pass


class OutputReadError(Exception):
    pass


class Solver:
    def __init__(self, solver_path=r'C:\PioSOLVER\PioSOLVER-edge.exe'):
        """
        Create a new solver instance.
        :arg solver_path: path to the solver executable to use
        """
        workingdirectory = pathlib.Path(solver_path).parent
        os.chdir(workingdirectory)

        self.process = subprocess.Popen([solver_path],
                                        bufsize=0,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
        self.write_line("set_end_string END")
        self.read_until_end()
        self._hand_order = None

    def exit(self):
        self.process.kill()
        self.process.wait(1)
        self.process.__exit__(None, None, None)

    def commands(self, lines, print_out=False):
        for line in lines:
            result = self.command(line)
            if print_out:
                for res in result:
                    print(res)

    def command(self, line):
        try:
            self.write_line(line)
            return self.read_until_end()
        except SolverException:
            self.read_until_end()
            raise

    def write_line(self, line):
        self.write_lines([line])

    def write_lines(self, lines):
        self.process.stdin.write("\n".join(lines))
        self.process.stdin.write("\n")

    def read_until_end(self):
        """Reads until the keyword 'END'"""
        return self.read_until('END')

    def read_until(self, target):
        """Reads until given keyword"""
        lines = []
        while True:
            line = self.read_line()

            # Error finding
            if line.find("problems with your license") == 0:
                raise SolverException(line)
            if line.find("ERROR") == 0 or line.find("Piosolver directory") > 0:
                raise SolverException(line)

            # Performing task
            if line.strip() == target.strip():  # Checks for target
                return lines
            else:  # Appends output here
                lines.append(line.strip())

    def read_line(self):
        """Reads the next line and returns it"""
        line = self.process.stdout.readline()
        if not line:
            raise OutputReadError(f"Unexpected end of output.")
        return line
