import random

reaction_emojis = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]
reaction_emojis_human = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

captchas = {
    "What is the decimal representation of the largest single digit number in base-9?": 8,
    "In this capture you will be asked to compute a prime number decomposition. Since this may not be possible using a single emoji, please read the following hints first: In case the decomposition consists of multiple prime numbers, give them by reacting with the corresponding different numbers in exactly 2s +/ 10ms time intervals. In case a prime number has to be given twice, be sure to un-react the corresponding emoji within the 2s-time-window such that you can retain the desired input frequency. Also make sure to give the prime numbers in ascending order. Please compute the prime number decomposition of seven now.": 7,
    "Consider a tricycle with a square wheel. How many sides does the wheel have?": 4,
    "Assume you are playing gregtech: new horizons. you want to build an IV fluid extractor, which requires two IV circuits, two 1x Platinum Wires, 1 IV electric pump, 1 IV electric piston, 1 IV machine hull and 2 borosilicate glass blocks. for the circuits, you need different alloys and circuit boards, and you need to do this with different recipes, with IV power. what you do not need is cobblestone. so tell me, what is the maximum stack size of cobblestone in vanilla minecraft divided by 8?": 8,
    "In this question you will be asked to compare apples with pears. Which is more, 3 apples or 4 pears?": 4,
    "On a scale from 0-9, how cool is this bot?": 9,
    "Imagine a mouse observing a pacman collecting bottles of beer. The mouse reacts to this message with twice the amount of beer bottles that the pacman drank. What emoji would it react with, if the pacman drank 3 bottles?": 6,
    "How many trimesters can one study 'Viticulture and Enology' at the Washington State University (WSU) per year?": 3,
    "Assume there are nine moons orbiting the earth. Assume that every moon is connected to exactly two different other moons by wormholes in such a way that it is possible to reach every moon by travelling through the wormholes after starting on an arbitrary moon. Consider a moon-nazi jumping from their nazi-base on moon A into a wormhole. Which is the minimum amount of wormholes that the moon-nazi has to traverse in order to get back to moon A if he cannot use a wormhole that he previously traversed? The wormwhole that he has already jumped through initially shall be included.": 9,
    "To get anywhere in life you must be able to code. This captcha will ask of you to return the result of the C compiler, when high level code is passed to it. It is important to consider preprocessing directives, lexical analysis and intermediate representation of high-level code before conversion to basic assembly instructions. Additionally, macros, absence of concrete typing and library calls play an important factor in this. Please now answer what the C compiler would return, given the following high level python code: eval('print(15/3)')": 5,
    "I have 4 siblings. How many children does my dad have? (Hint: Assume that my dad is in his first and only marriage, and that he did not have any children before. Also, neglect any potential step siblings that my mom may have brought into the marriage.)": 5,
    "What is the maximal number of times that an Indonesian blue-tongued skink can die before it is dead?": 1,
    "How many times can an Indonesian blue-tongued skink die before it is dead?": 1,
    "What is the value of the integral from the euler-mascheroni-constant to pi over the 42-Jonquière polylogarithm multiplied by zero?": 0,
    "Which is the 6th natural number? (Hint: Only fools call 0 a natural number.)": 6
  }

def get_captcha_result(captcha_message: str) -> int:
    return captchas[captcha_message]
