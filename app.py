from flask import Flask, redirect, render_template, request, session
import random as rand

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

words = []

# TODO wenn buchstabe mehrfach vorkommt, nur den richtigen mit 2 markieren (wenn an richtiger stelle)
# ansonsten, nur so viele mit 1 markieren, wie auch in dem wort vorkommen

# TODO wenn spiel zu ende -> neu starten button
# TODO beim seiten refresh aktuellen session spielstand anzeigen, so dass der nutzer später weiterspielen kann

with open("words.txt", "r") as file:
    dict = {}
    for line in file:
        placeholder = len(line)
        words.append(line.removesuffix("\n"))
        if not placeholder in dict:
            dict[placeholder] = 0
        dict[placeholder] += 1
    print(dict)


def istrichtig(zeile, spalte):
    return 0


@app.route("/reset-session")
def resetSession():
    session.clear()
    return redirect("/")


@app.route("/")
def hello():
    # TODO oder wenn session finish ist true
    if 'spielstand' not in session or session["finish"]:
        spielstand = {"aktuelleZeile": 0, "spalten": rand.randint(
            5, 12), "zeilen": rand.randint(5, 7)}
        session['spielstand'] = spielstand
        session["gamefield"] = [[0 for x in range(spielstand.get(
            "spalten"))] for y in range(spielstand.get("zeilen"))]
        session["loesungsWort"] = rand.choice(
            [x for x in words if len(x) == spielstand["spalten"]])
        session["finish"] = False
        session.update()
    return render_template('hello.html', spielstand=session['spielstand'], istrichtig=istrichtig, gamefield=session["gamefield"])


# @app.route("/new-game", methods=['POST'])
# def newGame():
    # finish = True
    # return "ok"
 #   pass

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


@app.route("/raten", methods=['POST'])
def correctWord():
    guess = request.form["guess"]

    # ERSTMAL WEGLASSEN: if guess not in words
    #    throw , abort(400)

    correctWordList = evaluateGuess(guess, session["loesungsWort"])

    session["spielstand"]["aktuelleZeile"] += 1
    result = {"result": correctWordList}

    if session["spielstand"]["aktuelleZeile"] >= session["spielstand"]["zeilen"] or guess == session["loesungsWort"]:
        result["solution"] = session["loesungsWort"]
        session["finish"] = True

    session.update()

    return result
