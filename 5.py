
PUNCTUATION_MARKS = (',', ':', '"', "'", '(', ')', ';', '`', '—', '[', ']', '{', '}', "!", "...", ".")


def is_initial(word):
    return len(word) == 1 and word.lower() != word and 'А' <= word <= 'Я'


def is_correct_name(word):
    if word.count("-") == 1:
        first, second = word.split("-")
        return is_correct_name(first) and is_correct_name(second)

    return len(word) > 1 and word[:1].lower() != word[:1] and word[1:].lower() == word[1:]


def main():
    input_file = open("input.txt", "r", encoding = "utf-8")
    text = input_file.read()
    input_file.close()

    for mark in PUNCTUATION_MARKS:
        text = text.replace(mark, "")

    words = list(text.split(" "))
    flag = False

    for i in range(len(words) - 1):
        if flag:
            flag = False
            continue

        if not is_initial(words[i]):
            continue

        if is_initial(words[i + 1]) and i + 2 < len(words) and is_correct_name(words[i + 2]):
            print(words[i] + ". " + words[i + 1] + ". " + words[i + 2])
            flag = True
        elif is_correct_name(words[i + 1]):
            print(words[i] + ". " + words[i + 1])


if __name__ == "__main__":
    main()
