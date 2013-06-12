# imports?


class ScriptGenerator():

    # script is an instance of pnlScript
    def __init__(self, script):
        self._script = script

    def filter_value(self, value, operator):
        line = "# filter_value -- "
        if operator == '<':
            line = line + "less than %s\n" % (value)
        if operator == '>':
            line = line + "greater than %s\n" % (value)
        self._script.write(line)