from app import evaluateGuess


def test_eval():
    assert evaluateGuess("rebua", "bauer") == [1, 1, 1, 1, 1]


def test_eval2():
    assert evaluateGuess("barue", "bauer") == [2, 2, 1, 1, 1]


def test_eval3():
    assert evaluateGuess("xyzxy", "bauer") == [0, 0, 0, 0, 0]


def test_eval4():
    assert evaluateGuess("maler", "maler") == [2, 2, 2, 2, 2]


def test_eval5():
    assert evaluateGuess("rofo", "refa") == [2, 0, 2, 0]


def test_eval6():
    assert evaluateGuess("axcd", "abdf") == [2, 0, 0, 1]


def test_eval7():
    assert evaluateGuess("wata", "xazz") == [0, 2, 0, 0]


def test_eval8():
    assert evaluateGuess("wataaa", "watzzz") == [2, 2, 2, 0, 0, 0]


def test_eval9():
    assert evaluateGuess("wassers", "ssaaaaa") == [0, 1, 1, 1, 0, 0, 0]


def test_eval10():
    assert evaluateGuess("jannik", "jannik") == [2, 2, 2, 2, 2, 2]


def test_eval11():
    assert evaluateGuess("jannnik", "jannoik") == [2, 2, 2, 2, 0, 2, 2]


def test_eval12():
    assert evaluateGuess("wasssers", "ssaaaaas") == [0, 1, 1, 1, 1, 0, 0, 0]
