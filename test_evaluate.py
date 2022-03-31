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
    eval = evaluateGuess("wasserfass", "wasserfall")
    assert eval.count(0) == 2
    assert eval.count(1) == 0
    assert eval.count(2) == 8


def test_eval10():
    assert evaluateGuess("jannik", "jannik") == [2, 2, 2, 2, 2, 2]


def test_eval11():
    assert evaluateGuess("jannnik", "jannoik") == [2, 2, 2, 2, 0, 2, 2]


def test_eval12():
    eval = evaluateGuess("wasssers", "ssaaaaas")
    assert eval.count(2) == 1


def test_eval13():
    eval = evaluateGuess("ei", "ei")
    assert eval == [2, 2]
