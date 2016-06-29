import os

PUNCTUATION_MARKS = (',', ':', '"', "'", '(', ')', ';', '`', '—', '[', ']', '{', '}', "!", "...", ".")


def is_russian(word):
    for char in word.lower():
        if 'а' <= char <= 'я':
            continue
        return False
    return True


def get_sentences(text):
    result = []

    current = ''
    initial = False
    after_point = 0

    for i in range(len(text)):
        if text[i] == ' ':
            if after_point == 1:
                after_point += 1

            current += text[i]
            continue

        if text[i] == '!' or text[i] == '?':
            current += text[i]
            if current:
                result.append(current)
                current = ''
            continue

        if after_point != 0 and text[i].lower() == text[i]:
            after_point = 0

        if after_point == 2:
            current = current[:-1]
            if current:
                result.append(current)
                current = ''

        current += text[i]

        if text[i] == '.' and not initial:
            after_point = 1

        initial = False

        if text[i].lower() != text[i] and is_russian(text[i]):
            initial = True

    return result


def is_initial(word):
    return len(word) == 1 and word.lower() != word and is_russian(word)


def is_correct_name(word):
    return len(word) > 1 and word[:1].lower() != word[:1] and word[1:].lower() == word[1:] and is_russian(word)


def is_correct_family(word):
    if word.count("-") == 1:
        first, second = word.split("-")
        return is_correct_name(first) and is_correct_name(second)

    return is_correct_name(word)


def get_names(text):
    result = []
    for mark in PUNCTUATION_MARKS:
        text = text.replace(mark, "")

    words = list(text.split(" "))
    flag = 0

    for i in range(len(words) - 1):
        if flag > 0:
            flag -= 1
            continue

        if is_correct_name(words[i]) and is_correct_family(words[i + 1]):
            result.append((words[i], words[i + 1]))
            flag = 1
            continue

        if not is_initial(words[i]):
            continue

        if is_initial(words[i + 1]) and i + 2 < len(words) and is_correct_family(words[i + 2]):
            result.append((words[i] + ". " + words[i + 1] + ".", words[i + 2]))
            flag = 2
        elif is_correct_family(words[i + 1]):
            result.append((words[i] + ".", words[i + 1]))
            flag = 1

    return result


def remove_path(path):
    for file in os.listdir(path):
        if os.path.isfile(path + "/" + file):
            os.remove(path + "/" + file)
        else:
            remove_path(path + "/" + file)
            os.rmdir(path + "/" + file)


def main():
    input_file = open("input.txt", "r", encoding="utf-8")
    text = input_file.read()
    input_file.close()
    text = text.replace("\n", " ")

    try:
        os.mkdir("output")
    except OSError:
        remove_path("output")

    for sentence in get_sentences(text):
        names = get_names(sentence)

        for name in names:
            if not os.path.exists("output/" + name[1]):
                os.mkdir("output/" + name[1])

            if name[0][-1] != ".":
                address = "output/" + name[1] + "/" + name[0] + ".txt"
            else:
                address = "output/" + name[1] + "/" + name[0] + "txt"
            if os.path.exists(address):
                file = open(address, "a", encoding="utf-8")
                file.write("\n")
            else:
                file = open(address, "w", encoding="utf-8")

            file.write(sentence)
            file.close()


if __name__ == "__main__":
    main()
