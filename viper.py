from non import translator
def venom(first, second):
    firsten:int = int(translator(first, 2, 10))
    seconten:int = int(translator(second, 2, 10))
    finalten:str = str(firsten+seconten)
    winner:str = translator(finalten, 10, 2)
    return winner
if __name__ == "__main__":
    first:str = input("Please enter the first binary number: ")
    second:str = input("Please enter the second binary number: ")
    winner:str = venom(first, second)
    print(f"The additive result is: {winner}")