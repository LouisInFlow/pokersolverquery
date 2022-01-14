import subprocess
import os
import pathlib
from typing import Union
from texasholdem import Flop
import pokersolverquery.building_blocks


class SolverException(Exception):
    pass


class OutputReadError(Exception):
    pass


class BaseSolver:
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

    def command(self, line):
        try:
            self.write_line(line)
            return self.read_until_end()
        except SolverException:
            self.read_until_end()
            raise

    def commands(self, lines, print_out=False):
        for line in lines:
            result = self.command(line)
            if print_out:
                for res in result:
                    print(res)

    def write_line(self, line):
        self.process.stdin.write(line + '\n')

    def write_lines(self, lines):
        for line in lines:
            self.write_lines(line)

    def read_line(self):
        """Reads the next line and returns it"""
        line = self.process.stdout.readline()
        if not line:
            raise OutputReadError(f"Unexpected end of output.")
        return line

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
                lines.append(line.strip())
                return lines
            else:  # Appends output here
                lines.append(line.strip())

    def read_until_end(self):
        """Reads until the keyword 'END'"""
        return self.read_until('END')


class UPISolver(BaseSolver):
    def __init__(self, solver_path=r'C:\PioSOLVER\PioSOLVER-edge.exe'):
        """
        Create a new UPI solver instance.
        :arg solver_path: path to the solver executable to use
        """
        super().__init__(solver_path=solver_path)

    @property
    def tree_exists(self):
        return 'true' in self.command('is_tree_present')[0]

    def load_tree(self, tree_path):
        self.command(f'load_tree "{tree_path}"')


class LoadedTree:
    def __init__(self, path: str, solver: UPISolver):
        self.file_path = path
        self.solver = solver
        self.solver.load_tree(path)

    @property
    def flop(self):
        r_node = self.solver.command(f'show_node r')
        return Flop.from_string(r_node[2])

    @property
    def ip_range(self):
        return pokersolverquery.building_blocks.TexasRange(self.solver.command('show_range IP')[0])

    @property
    def opp_range(self):
        return pokersolverquery.building_blocks.TexasRange(self.solver.command('show_range OOP')[0])

    @property
    def all_lines(self):
        return self.solver.command('show_all_lines')[:-1]

    def next_actions(self, line):
        res = self.solver.command(f'show_children {line}')
        line_codes = res[1::7]
        return [pokersolverquery.building_blocks.Line(code).line[-1] for code in line_codes]


class FlopSolver:
    """
    A convenient wrapper for the BaseSolver class, introducing methods specific to flop solving
    """
    def __init__(self):
        self.flops = []
        self.Tree = None  # Add tree object type

    def add_flops(self, flops: Union[list, Flop]):
        pass


def main():
    solve = UPISolver(solver_path=r'C:\PioSOLVER\jesolver_pro_1080\jesolver_pro_avx2_1080.exe')
    tree = LoadedTree(r'D:\Pio Saves 2\Stacked\FLOP FULL EP vs IP call\The rest (range check)\Ts9s2d.cfr', solve)
    print(tree.flop)
    print(tree.ip_range)
    print([str(el) for el in tree.next_actions('r:0:c')])
    # for line in tree.all_lines:
    #     parsed = building_blocks.parse_line(line)[0]
    #     print(line, tuple(act.action + ' ' + str(act.betsize) for act in parsed))


if __name__ == '__main__':
    main()

