import sys
import os
from io import StringIO
import contextlib


def eval_attempt(code, test_cases):
    @contextlib.contextmanager
    def stdout_io(stdout=None):
        old_stdout = sys.stdout
        old_stdin = sys.stdin
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        sys.stdin = open(test_cases, "r")
        yield stdout
        sys.stdout = old_stdout
        sys.stdin = old_stdin

    with stdout_io() as s:
        try:
            exec(code)
        except Exception as err:
            print(f"{type(err).__name__} was raised: {err}")

    return s.getvalue()


def one_answers(test_case):
    if test_case == 0:
        return "Hello, David\n"
    return "Hello, David\n"


def one(filename, code):
    for test_case in range(1, 2):
        test_case = f"case/input/one/{test_case}.txt"
        data = eval_attempt(code, test_case)
        print(repr(data))
        if data != one_answers(test_case):
            with open(filename[:-3] + "_resp.txt", "a+") as ff:
                ff.write(data)
            os.remove(filename)
            return filename[:-3] + "_resp.txt"
    with open(filename[:-3] + "_resp.txt", "a+") as ff:
        ff.write("Congrats! Next clue: ...")
    return filename[:-3] + "_resp.txt"


def control(question, filename, code):
    print(repr(question))
    return one(os.path.join(app.config['UPLOAD_FOLDER'], filename), code)