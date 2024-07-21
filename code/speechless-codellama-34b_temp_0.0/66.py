

def advancedDigitSum(s, t):
    sum_s = 0
    sum_t = 0
    for char in s:
        if char.isupper():
            sum_s += ord(char)
    for char in t:
        if char.islower():
            sum_t += ord(char)
    return (sum_s, sum_t)

if __name__ == '__main__':
    inputs = [eval(f"[{i}]") for i in ['"", "abc"', '"abAB", "abc"', '"abcCd", ""', '"helloE", "abc"', '"woArBld", "xyz"', '"ZABCD", "zabcd"', '"HELLO", "hello"', '"WORLD", "world"', '"Python", "python"', '"Java", "java"', '"JavaScript", "javascript"', '"Csharp", "csharp"', '"GOlang", "golang"', '"Kotlin", "kotlin"', '"RUBY", "ruby"', '"Scala", "scala"', '"LuA", "lua"', '"Tcl", "tcl"', '"SwifT", "swift"', '"VbNet", "vbnet"', '"Perl", "perl"', '"PHP", "php"', '"Rust", "rust"', '"TypeScript", "typescript"', '"Groovy", "groovy"', '"!@#$$%^&*()", "abc123"', '"ABCDEFG", "1234567"', '"?!@#$%^&*", "abcdefghijklmnopqrstuvwxyz"', '"NOupperCaseHere", "alllowercasehere"', '"MIXEDcaseINPUT", "mixedCASEinput"', '"~`!@#$%^&*()-_=+[]{}\\|;:\'\\",<.>/?", "qwertyuiopasdfghjklzxcvbnm"', '"a"*10000 + "A"*10000, "z"*10000 + "Z"*10000', '"aaaaaAAAAA", "bbbbbBBBBB"', '"1234567890", "!@#$%^&*()"', '"", ""', '"1234567890", "1234567890"', '"AAAAAAA", "aaaaaaa"', '"A"*100000, "a"*100000', '"!@#$%^&*()", "!@#$%^&*()"', '"ABCDEFGHIJKLM", "nopqrstuvwxyz"', '"AbCdEfG", "HjKlMnO"', '"Z", "z"', '"Hello World", "HELLO WORLD"', '" ", " "', '"\\t\\n\\r", "\\t\\n\\r"', '"aA", "Aa"', '"ABCD", "abcd"', '"", ""', '" ", " "', '"12345", "67890"', '"AbCdEfG", "hIjKlMn"', '"!@#$%^&*()", "_+=-"', '"mixedCaseString", "MIXEDCASESTRING"', '"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"', '"aaaaa", "BBBBB"', '"", ""', '"ABCD", "abcd"', '"123", "456"', '"abcd", "ABCD"', '"!@#$%^&", "*&^%$#@"', '"     ", "     "', '"AaBbCc", "DdEeFf"', '"XYZ", "xyz"', '"HelloWorld", "helloworld"', '"MixedCase123", "mixedcase123"', '"NONALPHANUMERIC", "nonalphanumeric"', '"UpperCaseOnly", "lowercaseonly"', '"NoUpperCaseHere", "NOLOWERCASEHERE"', '"SingleChar", "a"', '"U", "l"', '"VeryLongStringWithOnlyUpperCaseCharacters"*100, "VeryLongStringWithOnlyLowerCaseCharacters"*100']]
    i = 0

    while(True):
        advancedDigitSum(*inputs[i%len(inputs)])
        i += 1

