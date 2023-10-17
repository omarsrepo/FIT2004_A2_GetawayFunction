import random


def make_dictionary(n: int):
    file = open("test_dict.txt", "w")
    for _ in range(n):
        length = random.randint(4, 8)
        word = ""
        frequency = random.randint(0, 5000)
        definition = ""
        for _ in range(length):
            word += random.choice(alphabet)
            for _ in range(random.randint(2,4)):
                definition += random.choice(alphabet)
        file.writelines(f"word: {word}\nfrequency: {frequency}\ndefinition: {definition}\n\n")
    file.close()


if __name__ == '__main__':
    alphabet = [chr(i) for i in range(97, 123)]
    make_dictionary(10**6)
