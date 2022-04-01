from cgitb import text
import json
from flask import Flask, jsonify, redirect, render_template, request, session
import random as rand

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

words = []

words_medium = []
words_hard = []
words_nightmare = []
words_impossible = []

with open("words.txt", "r") as file:
    length = 0
    for line in file:
        placeholder = len(line)
        if placeholder < 7:
            words_medium.append(line.rstrip("\n").lower())
        elif placeholder < 9:
            words_hard.append(line.rstrip("\n").lower())
        elif placeholder < 11:
            words_nightmare.append(line.rstrip("\n").lower())
        else:
            words_impossible.append(line.rstrip("\n").lower())


def istrichtig(zeile, spalte):
    return 0


@app.route("/reset-session")
def resetSession():
    session["schwierigkeitsgrad"] = request.args.get(
        "difficulty", default="medium")
    session["new_game"] = True
    return redirect("/")


words = {
    "medium": words_medium,
    "hard": words_hard,
    "nightmare": words_nightmare,
    "impossible": words_impossible
}

diff = {
    "medium": [5, 5],
    "hard": [7, 7],
    "nightmare": [9, 9],
    "impossible": [11, 11]  # TODO
}


def maxSpalten(difficulty):
    [a, b] = diff[difficulty]
    return rand.randint(a, b)


@app.route("/")
def hello():
    schwierigkeitsgrad = session.get("schwierigkeitsgrad", "medium")

    if 'spielstand' not in session or session["finish"] or session.get("new_game", False):
        session["new_game"] = False
        s = maxSpalten(schwierigkeitsgrad)
        session["loesungsWort"] = rand.choice(
            [x for x in words[schwierigkeitsgrad] if len(x) == s])
        spalten = len(session["loesungsWort"])
        spielstand = {"aktuelleZeile": 0,
                      "spalten": spalten, "zeilen": spalten}
        session['spielstand'] = spielstand
        session["gamefield"] = [[0 for x in range(spielstand.get(
            "spalten"))] for y in range(spielstand.get("zeilen"))]
        session["finish"] = False
        session.update()
    return render_template('hello.html', schwierigkeitsgrad=schwierigkeitsgrad, spielstand=session['spielstand'],
                           istrichtig=istrichtig,
                           gamefield=session["gamefield"])


def evaluateGuess(guess, solution):
    correctWordList = []
    wordsGuess = []
    wordsSolution = []
    wordsRightPosition = []

    for letter in guess:
        if letter not in words:
            wordsGuess.append(letter)
    for letter in solution:
        if letter not in wordsSolution:
            wordsSolution.append(letter)

    letterIndex = 0
    for letter in guess:
        vorkommenAnz = 0
        for i in wordsGuess:
            if i == letter:
                vorkommenAnz += 1

        if letter in solution:
            if letter == solution[letterIndex]:
                correctWordList.append(2)
                wordsRightPosition.append(letter)
            elif vorkommenAnz >= 1 and letter not in wordsRightPosition:
                correctWordList.append(1)
            else:
                correctWordList.append(0)
        else:
            correctWordList.append(0)
        letterIndex += 1
    print("guess: " + str(guess))
    print("solution: " + str(solution))
    print("Words guess: " + str(wordsGuess))
    print("Words solution: " + str(wordsSolution))
    return correctWordList


@ app.route("/raten", methods=['POST'])
def correctWord():
    guess = request.form["guess"]
    print("IGoieomgvefvm" + guess)

    correctWordList = evaluateGuess(guess, session["loesungsWort"])

    session["gamefield"][session["spielstand"]["aktuelleZeile"]] = [
        {"buchstabe": x, "wert": y} for (x, y) in zip(list(guess), correctWordList)]

    print(session["gamefield"][session["spielstand"]["aktuelleZeile"]])

    session["spielstand"]["aktuelleZeile"] += 1
    result = {
        "result": correctWordList
    }

    print(session)

    if session["spielstand"]["aktuelleZeile"] >= session["spielstand"]["zeilen"] or guess == session["loesungsWort"]:
        result["solution"] = session["loesungsWort"]
        result["richtigGeraten"] = guess == session["loesungsWort"]

        session["finish"] = True

    session.update()

    return result
