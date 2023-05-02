

def is_contain_word(data: object, word: str) -> bool:
    if word.lower() in data['text'].lower():
        return True
    return False

def is_contain_words(data: object, word_list: list)->bool:
    for word in word_list:
        if is_contain_word(data, word):
            return True
    return False

def get_word_frequency(data: object, word: str)->int:
    count = 0
    word_list = data['text'].split(' ')
    for d_word in word_list:
        if d_word.lower() == word.lower():
            count += 1
    return count

def get_words_frequency(data: object, word_list: list)->int:
    count = 0
    d_word_list = data['text'].split(' ')
    for d_word in d_word_list:
        if d_word.lower() in word_list:
            count += 1
    return count



def get_word_position(data: object, word: str) -> int:
    word_list = data['text'].split()
    pos = 0
    for wd in word_list:
        if wd.lower() == word.lower():
            return pos
        pos += 1
    return -1




