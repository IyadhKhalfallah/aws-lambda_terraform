def is_anagram(string_1, string_2):
    return sorted(string_1.lower()) == sorted(string_2.lower())
