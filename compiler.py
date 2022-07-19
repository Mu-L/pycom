import tokenise
import re

invopmap = {v: k for k, v in tokenise.tokmap.items()}

implemented = [
    ('KW', 'def'),
    ('KW', 'for'),
    ('KW', 'if'),
    ('KW', 'elif'),
    ('KW', 'else'),
    ('KW', 'while'),
    ('KW', 'match'),
    ('KW', 'case'),
    ('KW', 'return'),
    ('KW', 'continue'),
    ('KW', 'import'),


    ('SIG', 'NEWLINE'),
    ('SIG', 'BLOCK_START'),
    ('SIG', 'BLOCK_END'),
    ('SIG', 'TYPEPOINTER'),
    ('SIG', 'FUNCTYPEPOINTER'),
    ('SIG', 'COMMA')
]

implementedtypes = [
    "STRING",
    "FSTRING"
]

implementedmodules = [
    "math"
]

pythonbuiltins = [
    ('NAME', 'print'),
    ('NAME', 'range'),

    ('METHOD', 'factorial'),
    ('METHOD', 'sqrt')
]

cfuncs = [
    'void print(std::string str){std::cout << str << std::endl;}',
    'void print(int istr){std::cout << istr << std::endl;}',
    'void print(float fstr){std::cout << fstr << std::endl;}',
    'void print(long long int llistr){std::cout << llistr << std::endl;}',
    'void print(long double ldstr){std::cout << ldstr << std::endl;}',
    'int len(std::string str){return str.length();}',
    'std::string input(std::string prompt){std::cout << prompt; std::string x; std::cin >> x; return x;}',
]

types = ["str", "int", "float", "None"]

includes = ["iostream", "string", "headers/range.hpp", "sstream"]
using = ["util::lang::range"]

pytypetoctype = {
    "str": "std::string",
    "int": "long long int",
    "float": "long double",
    "None": "void",
    "list": "std::vector<std::string>"
}

def fstringtocppformat(stringtok: str):

    stringtok = stringtok[1:]

    formatargs = []

    for i in range(len(stringtok)):
        if stringtok[i] == '{':
            wi = i + 1
            expr = ""
            while stringtok[wi] != "}":
                expr += stringtok[wi]
                wi += 1
            
            formatargs.append(expr)
    
    strformatargs = ", "
    for arg in formatargs:
        strformatargs += arg + ", "

    return re.sub("\{.*?\}", "{}", stringtok) + strformatargs
            

def findlastkw(tokens, currentind):
    for i in range(currentind, -1, -1):
        if tokens[i][0] == "KW":
            return tokens[i]

def findnextfunctypeptr(tokens: list, currentind):
    try:
        return tokens.index(("SIG", "FUNCTYPEPOINTER"), currentind)

    except ValueError:
        return None

def parsetabamount(tabtok):
    return int(str(tabtok[1]).removesuffix(" TAB"))

def removenewlinedups(x):
    return [x[i] for i in range(len(x)) if (i==0) or (x[i] !=x[i-1]) or (x[i] != ("SIG", "NEWLINE"))]

class Compile:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.type = 0
        self.value = 1

        self.oktokens = self.checktokens()

    def iteratetokens(self):
        code = ""
        for include in includes: code += f'#include "{include}"\n'
        for use in using: code += f"using {use};\n"
        for func in cfuncs: code += func + " "
        code += "struct list {int i; std::string str; float f;};\n"
        
        for i in range(len(self.oktokens)):
            if self.oktokens[i][self.type] == "KW":
                gobackby = 1

                if self.oktokens[i-1] == ("SIG", "NEWLINE"):
                    gobackby = 2

                if self.oktokens[i-gobackby][self.type] != "SIG" and not str(self.oktokens[i-gobackby][self.value]).endswith(" TAB"):
                    if self.oktokens[i+1] != ("FUNC", "main") and self.oktokens[i] != ("KW", "continue") and self.oktokens[i] != ("KW", "return"):
                        code += "}"

            if self.oktokens[i][self.type] == "NAME" or self.oktokens[i][self.type] == "FUNCREF" or self.oktokens[i][self.type] == "VARREF":
                code += self.oktokens[i][self.value]
            
            elif self.oktokens[i][self.type] == "OP":
                if self.oktokens[i][self.value] == "LPAREN":
                    code += "("

                elif self.oktokens[i][self.value] == "RPAREN":
                    code += ")"

                elif self.oktokens[i][self.value] == "in":
                    code += ": "

                else:
                    mapped = invopmap[self.oktokens[i][self.value]] 
                    if mapped != ";":
                        code += mapped

            elif self.oktokens[i][self.type] == "STRING" or self.oktokens[i][self.type] == "INT":
                code += self.oktokens[i][self.value]
            elif self.oktokens[i][self.type] == "SIG":
                if self.oktokens[i][self.value] == "NEWLINE":
                    if self.oktokens[i-1] != ("SIG", "NEWLINE"): 
                        if self.oktokens[i-1][self.type] != "SIG" and not str(self.oktokens[i-1][self.value]).endswith(" TAB") and self.oktokens[i+1] != ("KW", "def"):
                            code += ";"

                if self.oktokens[i] == ("SIG", "COMMA"):
                    code += ","

                if self.oktokens[i] == ("SIG", "DOT"):
                    code += "."

                elif self.oktokens[i] == ("SIG", "BLOCK_START"): code += "{"
                elif self.oktokens[i] == ("SIG", "BLOCK_END"): code += "}"
                
            elif self.oktokens[i][self.type] == "KW":
                if self.oktokens[i][self.value] == "def":
                    if self.oktokens[i+1] == ('FUNC', 'main'):
                        code += "int "

                    else:
                        indoftypedec = findnextfunctypeptr(self.oktokens, i)
                        if indoftypedec is not None:
                            if self.oktokens[indoftypedec + 1][self.value] in types:
                                code += pytypetoctype[self.oktokens[indoftypedec + 1][self.value]] + " " 
                            else:
                                print(f"error: token #{i}: invalid type specified for function '{self.oktokens[i+1][self.value]}'")

                elif self.oktokens[i][self.value] == "for":
                    itervarname = self.oktokens[i+1][self.value]
                    code += f"for(auto {itervarname}"

                elif self.oktokens[i][self.value] == "if":
                    code += "if("

                elif self.oktokens[i][self.value] == "elif":
                    code += "else if("

                elif self.oktokens[i][self.value] == "else":
                    code += "else"

                elif self.oktokens[i][self.value] == "while":
                    code += "while("

                elif self.oktokens[i][self.value] == "continue":
                    code += "continue"

                elif self.oktokens[i][self.value] == "return":
                    code += "return "

                elif self.oktokens[i][self.value] == "import":
                    code = f'#include "headers/py{self.oktokens[i+1][self.value]}.hpp"\n{str(self.oktokens[i+1][self.value]).capitalize()} {self.oktokens[i+1][self.value]};\n' + code

                else:
                    print(f"error: token #{i}: keyword '{self.oktokens[i][self.value]}' is not yet implemented, sorry")
                    exit(1)

            elif self.oktokens[i][self.type] == "FUNC":
                code += self.oktokens[i][self.value]

            elif self.oktokens[i][self.type] == "PARAM":
                if self.oktokens[i+1] == ("SIG", "TYPEPOINTER"):
                    if self.oktokens[i+2][1] in types:
                        typeofparam = self.oktokens[i+2][1] 
                    else: 
                        print(f"error: token #{i}: invalid type specified for param '{self.oktokens[i][self.value]}'")
                        exit(1)
                    ctypeofparam = pytypetoctype[typeofparam]
                    paramname = self.oktokens[i][self.value]
                    code += f"{ctypeofparam} {paramname}"


                else:
                    print(f"error: token #{i}: no type specified for param")
                    exit(1)

            elif self.oktokens[i][self.type] == "IMPORTREF":
                code += self.oktokens[i][self.value]

            elif self.oktokens[i][self.type] == "METHOD":
                code += self.oktokens[i][self.value]

            if i + 1 != len(self.oktokens): 
                if self.oktokens[i+1] == ("SIG", "BLOCK_END") and self.oktokens[i] != ("SIG", "NEWLINE"): code += ";"
                if self.oktokens[i+1] == ("SIG", "BLOCK_START"):
                    blockkw = findlastkw(self.oktokens, i)
                    if blockkw not in [('KW', 'def'), ('KW', 'else')]:
                        code += ")"

            

        return code, self.oktokens

            
    def checktokens(self):
        oktokens = []
        
        for token in self.tokens:
            if token[self.type] == "IMPORT_MODULE" and token[self.value] not in implementedmodules:
                continue


            if token[self.type] == "SIG" and str(token[self.value]).endswith(" TAB"):
                oktokens.append(token)
                continue

            if token in pythonbuiltins:
                oktokens.append(token)
                continue

            if token not in implemented:
                if token[self.type] not in ["STRING", "FSTRING", "NAME", "FUNC", "VAR", "SIG", "PARAM", "TYPE", "INT", "OP", "VARREF", "FUNCREF", "IMPORTREF", "IMPORT_MODULE"]: continue

                if token[self.type] == "OP": pass
 
            oktokens.append(token)


        temp = []

        for i in range(len(oktokens)):
            if oktokens[i] == ("KW", "import") and oktokens[i+1][self.type] != "IMPORT_MODULE":
                continue

            temp.append(oktokens[i])

        oktokens = temp

        oktokens = removenewlinedups(oktokens)

        return oktokens
