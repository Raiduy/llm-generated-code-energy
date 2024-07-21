

def count_distinct_characters_substrings(string: str, length: int) -> dict:
    if length > len(string):
        return {}
    result = {}
    for i in range(len(string) - length + 1):
        substring = string[i:i + length]
        distinct_chars = set(substring)
        result[substring] = len(distinct_chars)
    return result

if __name__ == '__main__':
    inputs = [eval(f"[{i}]") for i in ["'xyzXYZabc', 3", "'Jerry', 2", "'Jerry', 6", "'', 0", "'a', 1", "'aa', 1", "'aaa', 2", "'a'*100, 100", "'abc'*33+'a', 100", "'abcdefghijklmnopqrstuvwxyz', 25", "'abcdefghijklmnopqrstuvwxyz', 26", "'abcdefghijklmnopqrstuvwxyz', 27", "'a'*1000+'b'*1000, 2000", "'z'*1000+'y'*1000, 1", "'abcdefghijklmnopqrstuvwxyz', 5", "'abcdefghijklmnopqrstuvwxyZabcdefghijklmnopqrstuvwxyZ', 10", "'1234567890', 4", "'Hello World!', 4", "'AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ', 8", "'abcde'*100, 50", "'a'*100 + 'b'*100, 150", "'Python Python Python', 6", "'1234567890'*10, 1", "'The quick brown fox', 3", "'jumped over the lazy dog', 5", "'Python is a great language for data analysis', 10", "'I love Machine Learning and Artificial Intelligence', 15", "'Java, C++, Ruby, Rust, Go, Perl', 4", "'JavaScript is also a great language for web development', 7", "'', 3", "'a', 1", "'abcde', 5", "'aaaaa', 3", "'abcabcabc', 3", "'1234567890', 10", "'a'*100, 50", "'abc'*33+'a', 100", "'xyz'*34, 101", "'uniquecharactersonly', 20", "'with spaces and symbols $#@!', 5", "'UPPERCASE', 2", "'lowercase', 9", "'MiXedCaSe', 4", "'SpecialCharacters #$%&*', 5", "'nonasciicharactersĀāĒē', 6", "'with\\nnewlines', 4", "'aaabbbccc', 3", "'1234567890', 5", "'!@#$%^', 2", "'abcdefghijklmnopqrstuvwxyz', 26", "'abcdefghijklmnopqrstuvwxyz', 27", "'a'*10000 + 'b'*10000, 15000", "'This is a sentence with many distinct characters', 10", "'##@@!!%%^^&&', 4", "'ABCabc123', 1", "'AaBbCcDdEeFfGgHhIiJj', 2", "'abcdefghijklmnopqrstuvwxyz', 5", "'1234567890', 3", "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 4", "'!@#$%^&*()_+-=', 2", "'Lorem Ipsum Dolor Sit Amet', 6", "'The quick brown fox jumps over the lazy dog', 7", "'Pneumonoultramicroscopicsilicovolcanoconiosis', 8", "'Supercalifragilisticexpialidocious', 9", "'Two driven jocks help fax my big quiz', 10", "'Bright vixens jump; dozy fowl quack', 11", "'Jackdaws love my big sphinx of quartz', 12", "'Mr. Jock, TV quiz PhD, bags few lynx', 13", "'!@#$%^&*()_+-=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 14"]]
    i = 0

    while(True):
        count_distinct_characters_substrings(*inputs[i%len(inputs)])
        i += 1

