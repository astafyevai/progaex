PUNCTUATION_MARKS = (',', ':', '"', "'", '(', ')', ';', '`', '—', '[', ']', '{', '}', "!", "...", ".")


def is_russian(word):
    for char in word.lower():
        if 'а' <= char <= 'я':
            continue
        return False
    return True


def is_initial(word):
    return len(word) == 1 and word.lower() != word and is_russian(word)


def is_correct_name(word):
    return len(word) > 1 and word[:1].lower() != word[:1] and word[1:].lower() == word[1:] and is_russian(word)


def is_correct_family(word):
    if word.count("-") == 1:
        first, second = word.split("-")
        return is_correct_name(first) and is_correct_name(second)

    return is_correct_name(word)


def main():
    input_file = open("input.txt", "r", encoding="utf-8")
    text = input_file.read()
    input_file.close()
    text = text.replace("\n", " ")

    for mark in PUNCTUATION_MARKS:
        text = text.replace(mark, "")

    words = list(text.split(" "))
    flag = 0

    for i in range(len(words) - 1):
        if flag > 0:
            flag -= 1
            continue

        if is_correct_name(words[i]) and is_correct_family(words[i + 1]):
            print(words[i], words[i + 1])
            flag = 1
            continue

        if not is_initial(words[i]):
            continue

        if is_initial(words[i + 1]) and i + 2 < len(words) and is_correct_family(words[i + 2]):
            print(words[i] + ". " + words[i + 1] + ". " + words[i + 2])
            flag = 2
        elif is_correct_family(words[i + 1]):
            print(words[i] + ". " + words[i + 1])
            flag = 1


if __name__ == "__main__":
    main()
