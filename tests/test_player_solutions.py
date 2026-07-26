import game.player_solutions as ps


def test_add():
    assert ps.add(2, 3) == 5
    assert ps.add(-1, 1) == 0


def test_is_even():
    assert ps.is_even(4) is True
    assert ps.is_even(5) is False
    assert ps.is_even(0) is True


def test_reverse_string():
    assert ps.reverse_string("Python") == "nohtyP"
    assert ps.reverse_string("") == ""


def test_count_vowels():
    assert ps.count_vowels("hello") == 2
    assert ps.count_vowels("Sky") == 0
    assert ps.count_vowels("AEIOU") == 5


def test_fizzbuzz():
    assert ps.fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    assert ps.fizzbuzz(1) == ["1"]


def test_word_count():
    assert ps.word_count("Red red blue") == {"red": 2, "blue": 1}
    assert ps.word_count("One") == {"one": 1}
