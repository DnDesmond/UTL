letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
characters = [' ',
              '!',
              '"',
              '#',
              '$',
              '%',
              '&',
              "'",
              '(',
              ')',
              '*',
              '+',
              ',',
              '-',
              '.',
              '/',
              '0',
              '1',
              '2',
              '3',
              '4',
              '5',
              '6',
              '7',
              '8',
              '9',
              ':',
              ';',
              '<',
              '=',
              '>',
              '?',
              '@',
              'A',
              'B',
              'C',
              'D',
              'E',
              'F',
              'G',
              'H',
              'I',
              'J',
              'K',
              'L',
              'M',
              'N',
              'O',
              'P',
              'Q',
              'R',
              'S',
              'T',
              'U',
              'V',
              'W',
              'X',
              'Y',
              'Z',
              '[',
              '\\',
              ']',
              '^',
              '_',
              '`',
              'a',
              'b',
              'c',
              'd',
              'e',
              'f',
              'g',
              'h',
              'i',
              'j',
              'k',
              'l',
              'm',
              'n',
              'o',
              'p',
              'q',
              'r',
              's',
              't',
              'u',
              'v',
              'w',
              'x',
              'y',
              'z',
              '{',
              '|',
              '}',
              '~'
              ]
numbered = {}

for count, letter in enumerate(characters, 32):
    numbered[letter] = count

def binarises(number):
    current = 0
    finished = [0,0,0,0,0]
    valued = [16,8,4,2,1]
    regards = ""
    for cat in range(0, len(valued)):
        if number-current >= valued[cat]:
            finished[cat] = 1
            current += valued[cat]
    for num in finished:
        regards += str(num)
    return regards

def octalises(number):
    current = 0
    finished = []
    bases = []
    for cat in range(7,-1, -1):
        bases.append(8**cat)
    values = list(num*7 for num in bases)
    values.append(0)
    bases.append(0)
    for cat in range(0,8):
        sevenses = 0
        while (number-current)-bases[cat+1] >= values[cat+1]:
            if number-current != 0:
                current += bases[cat]
                sevenses += 1
            else:
                break
        finished.append(sevenses)
    for num in finished.copy():
        if num == 0:
            finished.remove(num)
        else:
            break

def duodecimalises(number):
    values = wide_base(number, 12)
    excess = {10: "A", 11: "B"}
    cat = 0
    for num in values:
        if num > 9:
            values[cat] = excess[num]
        cat += 1

def hexadecimalises(number):
    values = wide_base(number, 16)
    excess = {10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}
    cat = 0
    for num in values:
        if num > 9:
            values[cat] = excess[num]
        cat += 1

def wide_base(decimal: int, base: int):
    current = 0
    finished = []
    bases = []
    cat = 0
    while decimal >= (base**cat)*(base-1):
        bases.append(base**cat)
        cat += 1
    while cat < base:
        bases.append(base**cat)
        cat += 1
    bases.append(base**cat)
    bases.reverse()
    values = list(num*(base-1) for num in bases)
    values.append(0)
    bases.append(0)
    for cat in range(0,len(bases)-1):
        count = 0
        while (decimal-current)-bases[cat+1] >= values[cat+1]:
            if decimal-current != 0:
                current += bases[cat]
                count += 1
            else:
                break
        finished.append(count)
    for num in finished.copy():
        if num == 0:
            finished.remove(num)
        else:
            break
    excess = {}
    for count,char in enumerate(letters, 10):
        excess[count] = char.upper()
        excess[count+26] = char.lower()
    cat = 0
    # print(finished)
    for num in finished:
        if num > 9 and base > 10:
            finished[cat] = excess[num]
        cat += 1
    return finished

def narrow_acid(number: str, base: int):
    excess: dict[int: str] = {}
    for count,char in enumerate(letters, 10):
        excess[count] = char.upper()
        excess[count+26] = char.lower()
    values: list[int] = list(base**x for x in range(0,len(number)))
    values.reverse()
    current = 0
    cat = 0
    for character in number:
        try:    
            current += int(character)*values[cat]
        except ValueError:
            for key, value in excess.items():
                if value == character:
                    current += key*values[cat]
        cat += 1
    return current

def from_a_stone(finished: list):
    regards = ""
    for num in finished:
        regards += str(num)
    return regards

def destringer(string: str, file: str):
    to_write = open(f"{file}.txt", 'w')
    for character in string:
        if character != " ":
            if character.isupper():
                to_write.write(f"010{binarises(numbered[character.lower()])} ")
            else:
                to_write.write(f"011{binarises(numbered[character])} ")

def decoder(strings: list, base: int):
    results = []
    for string in strings:
        for key, value in numbered.items():
            if value == narrow_acid(string, base):
                results.append(key)
    return results

def coder(string: str, base:int):
    results = []
    for character in string:
        basic = wide_base(numbered[character], base)
        if base == 2:
            if len(basic) < 8:
                basic.reverse()
                while len(basic) < 8:
                    basic.append(0)
                basic.reverse()
        results.append(from_a_stone(basic))
    return results

def translator(number: str, current: int, desired: int):
    interim: int = narrow_acid(number, current)
    return from_a_stone(wide_base(interim, desired))

# coded = coder("In wilds beyond they speak your name with reverence and regret, for none could tame out savage souls yet you the challenge met, under palest watch, you taught, we changed, base instincts were redeemed, a world you gave to bug and beast as they had never dreamed.", 62)
# decoded = print(from_a_stone(decoder(coded, 62)))
# coded = coder("Hello World!", 12)
# print(coded)
# decoded = decoder(coded, 12)

# print(from_a_stone(wide_base(25,2)))
# print(wide_base(56800473913, 10))
# Oct 31 is Dec 25
# 56800473913