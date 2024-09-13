

#class Scope:
#    declarations: list[Declaration]
#    instructions: list
#
#
#class Instruction:
#    dupa: int
#
#
#class Func:
#    scope: Scope
#    references: list[Invocation]
#
#
#class Assignment:
#    name: str
#    value: str
#
#
#class Declaration:
#    ctype: str
#    name: str
#
#
#class Variable:
#    ctype: str
#    name: str
#    value: str
#
#
#class Invocation:
#    func: Func
#    args: list[Variable]
#

c_keywords = [
    "if",
    "while"
    "do",
    "goto"
    "return",
    "else",
    "for"
]

# probably escape \t to \\t
declaration_regex = "[^(),=\t]+ +[(),=\t]+;"
assignement_regex = "[^(),=\t]+ *= *[(),=\t]+;"

# What if I only divide it like that
# - assignment                      ".=.;"
#   something = something;
# - function call                   ".();"
#   something();
# - assignment and function call    ".=.();"
#   something = something();
# - declaration                     ". .;"
#   something;
# - declaration and assignment      ". .=.;"
#   something = something;
# - function declaration            ". .();"
#   something something();
# - function definition             ". .()"
#   something something()
# - scope start                     "{"
#   {
# - scope end
#   }                               "}"
# - everything else

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[93m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'
CEND    = '\033[0m'

def color_print(msg: str, end: str, color: str = ""):
    print(f"{color}{msg}{CEND}", end=end)

def parse(filename: str):
    f = open("dupa.c", "r")
    scope = 0
    is_multiline_comment = False
    is_multiline_define = False
    # open the file
    while True: # read it line by line
        line = f.readline()
        # for later: what if there are several semicolons in a line?

        # if there is no semicolon, read lines till we have one
        # also, check if the semicolon is not in a string
        # essentialy check if the line ends with it?


        # TODO: function definition and declarations can only appear in global scope

        # comments
        if "/*" in line and "*/" not in line:
            color_print(f"({scope})multiline comment:            |{line}", end="", color=CBLACK)
            is_multiline_comment = True
            continue
        if is_multiline_comment:
            color_print(f"({scope})multiline comment:            |{line}", end="", color=CBLACK)
            if "*/" in line:
                is_multiline_comment = False
            continue

        # defines
        if "#" in line or is_multiline_define:
            color_print(f"({scope})macro:                        |{line}", end="", color=CRED)
            if line.endswith("\\\n"):
                is_multiline_define = True
            else:
                is_multiline_define = False
            continue

        # proper scope detection
        if "{" in line:
            scope = scope + 1
        if "}" in line:
            scope = scope - 1

        if "//" in line or "/*" in line and "*/" in line:
            color_print(f"({scope})comment:                      |{line}", end="", color=CBLACK)
        elif any(key in line for key in c_keywords):
            color_print(f"({scope})c keyword:                    |{line}", end="", color=CYELLOW)
        elif "{" in line:
            color_print(f"({scope})scope start:                  |{line}", end="", color=CBEIGE)
        elif "}" in line:
            color_print(f"({scope})scope end:                    |{line}", end="", color=CBEIGE)
        elif "(" in line and ")" in line and ";" not in line and scope == 0:
            color_print(f"({scope})function definition:          |{line}", end="", color=CRED)
        elif "(" in line and ")" in line and "=" in line:
            color_print(f"({scope})assignment and function call: |{line}", end="", color=CGREEN)
        elif "(" in line and ")" in line and scope != 0:
            color_print(f"({scope})function call:                |{line}", end="", color=CVIOLET)
        elif "=" in line:
            color_print(f"({scope})assignement:                  |{line}", end="", color=CBLUE)
        elif "return" in line:
            color_print(f"({scope})return:                       |{line}", end="")
        elif "}" in line:
            color_print(f"{line}")
        elif "}" in line:
            color_print(f"{line}")
        else:
            color_print(f"({scope})other:                        |{line}", end="", color=CWHITE)

        if line == "":
            break

parse("")
