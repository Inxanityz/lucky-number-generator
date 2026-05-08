# test_lucky.py
# Minimal imports; relies on pytest fixtures (monkeypatch, tmp_path, capsys)
import pytest
import lucky as mod  # your module under test


# ---------------------------
# 1) monthConverter  (EP/BVA + white-box paths)
# ---------------------------
def test_monthConverter_valid_paths():
    # name / abbrev / case-insensitive
    assert mod.monthConverter("October") == 10
    assert mod.monthConverter("Oct") == 10
    assert mod.monthConverter("oCtObEr") == 10
    # alt abbrev path
    assert mod.monthConverter("sept") == 9
    # numeric string path
    assert mod.monthConverter("5") == 5
    # int-in-range path
    assert mod.monthConverter(5) == 5
    # bounds
    assert mod.monthConverter(1) == 1
    assert mod.monthConverter(12) == 12

def test_monthConverter_invalid_paths():
    # out of range numeric
    with pytest.raises(ValueError):
        mod.monthConverter(13)
    # unknown token
    with pytest.raises(ValueError):
        mod.monthConverter("Smarch")


# ---------------------------
# 2) checkBirthday  (EP/BVA)
# ---------------------------
@pytest.mark.parametrize(
    "d,m,y,ok",
    [
        (15, 10, 2000, True),
        (28, 2, 2001, True),
        (29, 2, 2000, True),   # leap valid
        (29, 2, 2001, False),  # leap invalid
        (31, 4, 2000, False),  # invalid day-in-month
        (1, 1, 1901, True),    # lower bound
        (31, 12, 2024, True),  # upper bound
        (1, 1, 1766, False),   # year too low
        (15, 13, 2000, False), # month invalid
    ],
)
def test_checkBirthday(d, m, y, ok):
    result, _ = mod.checkBirthday(d, m, y)
    assert result is ok


# ---------------------------
# 3) addDigits  (EP/BVA; white-box negative/invalid input)
# ---------------------------
def test_addDigits():
    assert mod.addDigits(7) == 7
    assert mod.addDigits(987) == 24
    assert mod.addDigits(0) == 0
    assert mod.addDigits(10) == 1  # 9->10 transition
    with pytest.raises(ValueError):
        mod.addDigits("123")


# ---------------------------
# 4) reduceNumber  (white-box loop/early-stop)
# ---------------------------
def test_reduceNumber_whitebox():
    # single digit: loop not entered
    assert mod.reduceNumber(7) == 7
    # master: early stop
    assert mod.reduceNumber(11) == 11
    # reduce → master
    assert mod.reduceNumber(29) == 11
    # multi-iteration
    assert mod.reduceNumber(99) == 9
    # near master
    assert mod.reduceNumber(12) == 3


# ---------------------------
# 5) getLuckyNumber  (composition + exception path)
# ---------------------------
def test_getLuckyNumber():
    assert mod.getLuckyNumber(15, 10, 2000) == 9
    # white-box master example aligned with current algorithm
    assert mod.getLuckyNumber(29, 7, 1901) == 11
    with pytest.raises(ValueError):
        mod.getLuckyNumber(31, 4, 2000)


# ---------------------------
# 6) isMasterNumber
# ---------------------------
@pytest.mark.parametrize(
    "n,ans",
    [(11, True), (22, True), (33, True), (10, False), (34, False)],
)
def test_isMasterNumber(n, ans):
    assert mod.isMasterNumber(n) is ans


# ---------------------------
# 7) getLuckyAnimal
# ---------------------------
def test_getLuckyAnimal():
    assert mod.getLuckyAnimal(1) == "Parrot"
    assert mod.getLuckyAnimal(9) == "Fish"
    assert mod.getLuckyAnimal(11) == "Dolphin"
    with pytest.raises(ValueError):
        mod.getLuckyAnimal(0)


# ---------------------------
# 8) getGeneration  (EP/BVA)
# ---------------------------
def test_getGeneration():
    assert mod.getGeneration(1996) == "Generation Z"
    assert mod.getGeneration(1901) == "Silent Generation"
    assert mod.getGeneration(2024) == "Generation Alpha"
    with pytest.raises(ValueError):
        mod.getGeneration(1766)
    with pytest.raises(ValueError):
        mod.getGeneration(2025)


# ---------------------------
# 9) makeProfile  (composition)
# ---------------------------
def test_makeProfile():
    p = mod.makeProfile(15, 10, 2000)
    assert p["lucky_number"] == 9
    assert p["animal"] == "Fish"
    assert p["generation"] == "Generation Z"

    p2 = mod.makeProfile(7, "January", 2024)
    assert p2["month"] == 1
    assert p2["generation"] == "Generation Alpha"

    with pytest.raises(ValueError):
        mod.makeProfile(31, 4, 2000)


# ---------------------------
# 10) compareProfiles  (dicts, tuples, mixed — white-box normalization)
# ---------------------------
def test_compareProfiles_dicts():
    r = mod.compareProfiles(
        {"lucky_number": 9, "animal": "Fish"},
        {"lucky_number": 9, "animal": "Fish"},
    )
    assert r == {"same_number": True, "same_animal": True}

def test_compareProfiles_mixed_and_tuples():
    # mixed dict & tuple
    r = mod.compareProfiles(
        {"lucky_number": 9, "animal": "Fish"},
        (15, 10, 2000),
    )
    assert r["same_number"] in (True, False)  # just ensure it runs
    assert r["same_animal"] in (True, False)

    # both tuples (forces normalization)
    r2 = mod.compareProfiles((15, 10, 2000), (7, "January", 2024))
    assert set(r2.keys()) == {"same_number", "same_animal"}


# ---------------------------
# 11) getBirthdayInput  (white-box: valid numeric, valid name, invalid)
# ---------------------------
def _fake_input(monkeypatch, answers):
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _: next(it))

def test_getBirthdayInput_numeric(monkeypatch):
    _fake_input(monkeypatch, ["15", "10", "2000"])
    assert mod.getBirthdayInput() == (15, 10, 2000)

def test_getBirthdayInput_name(monkeypatch):
    _fake_input(monkeypatch, ["7", "January", "2024"])
    assert mod.getBirthdayInput() == (7, 1, 2024)

def test_getBirthdayInput_invalid(monkeypatch):
    _fake_input(monkeypatch, ["31", "4", "2000"])
    with pytest.raises(ValueError):
        mod.getBirthdayInput()


# ---------------------------
# 12) readBirthdaysFile  (white-box: 0/1/N lines + invalid + missing)
# ---------------------------
def test_readBirthdaysFile_empty(tmp_path):
    p = tmp_path / "empty.txt"
    p.write_text("", encoding="utf-8")
    assert mod.readBirthdaysFile(str(p)) == []

def test_readBirthdaysFile_one_valid(tmp_path):
    p = tmp_path / "one.txt"
    p.write_text("15,10,2000\n", encoding="utf-8")
    assert mod.readBirthdaysFile(str(p)) == [(15, 10, 2000)]

def test_readBirthdaysFile_mixed_and_exclusion(tmp_path, capsys):
    p = tmp_path / "mix.txt"
    p.write_text("15,10,2000\n7,January,2024\n31,4,2000\n# note\n", encoding="utf-8")
    rows = mod.readBirthdaysFile(str(p))
    assert rows[:2] == [(15, 10, 2000), (7, 1, 2024)]
    out = capsys.readouterr().out
    assert "Excluding invalid date" in out

def test_readBirthdaysFile_missing():
    with pytest.raises(FileNotFoundError):
        mod.readBirthdaysFile("__no_such_file__")


# ---------------------------
# 13) showProfile  (ok + missing keys)
# ---------------------------
def test_showProfile_prints(capsys):
    p = mod.makeProfile(15, 10, 2000)
    mod.showProfile(p)
    out = capsys.readouterr().out
    assert "Lucky Number" in out
    assert "Lucky Animal" in out

def test_showProfile_missing_keys():
    with pytest.raises(ValueError):
        mod.showProfile({"number": 9})


# ---------------------------
# 14) saveProfile  (ok + bad path + invalid profile)
# ---------------------------
def test_saveProfile_ok_and_bad_path(tmp_path):
    p = mod.makeProfile(15, 10, 2000)
    out = tmp_path / "profiles.txt"
    mod.saveProfile(p, str(out))
    text = out.read_text(encoding="utf-8").strip()
    assert "Fish" in text
    assert len(text.splitlines()) == 1

    bad = tmp_path / "subdir" / "profiles.txt"  # subdir doesn't exist
    with pytest.raises(FileNotFoundError):
        mod.saveProfile(p, str(bad))

def test_saveProfile_invalid_profile(tmp_path):
    with pytest.raises(ValueError):
        mod.saveProfile({"day": 1}, str(tmp_path / "x.txt"))


# ---------------------------
# 15) mainProgram  (menu render + invalid choice)
# ---------------------------
def test_mainProgram_menu(monkeypatch, capsys):
    # feed 'x' so menu prints and invalid path is exercised
    it = iter(["x"])
    monkeypatch.setattr("builtins.input", lambda _: next(it))
    mod.mainProgram()
    out = capsys.readouterr().out.lower()
    assert "1 = keyboard" in out
    assert "2 = file" in out
    assert "3 = compare two birthdays" in out
    assert "4 = show a profile (keyboard)" in out
    assert "5 = save a profile (keyboard -> file)" in out
    assert "invalid choice" in out

