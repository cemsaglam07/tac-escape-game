import check50

@check50.check()
def hello_world():
    """multiline hello world"""
    check50.run("python3 multi_hello.py").stdout("Hello\nWorld!", regex=False).exit(0)
