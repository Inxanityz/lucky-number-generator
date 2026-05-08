from datetime import date

def addDigits(n):
    """Add the digits of an integer once. Raise ValueError on non-integers."""
    if not isinstance(n, int):
        raise ValueError("addDigits expects an integer")
    n = abs(n)
    return sum(int(d) for d in str(n))

def isMasterNumber(n):
    """Return True if n is 11, 22, or 33, else False."""
    return n in (11, 22, 33)

def reduceNumber(n):
    """Reduce a number by adding its digits until single digit or master number."""
    if not isinstance(n, int):
        raise ValueError("reduceNumber expects an integer")
    n = abs(n)
    while n > 9 and not isMasterNumber(n):
        n = addDigits(n)
    return n

def monthConverter(month_in):
    """
    Convert month name or number to 1..12.
    Accepts: 10, "10", "Oct", "October"
    Raises ValueError if month's invalid.
    """
    # If input is an integer
    if isinstance(month_in, int):
        if 1 <= month_in <= 12:
            return month_in
        else:
            raise ValueError("Month out of range")

    # Convert to string and turns all input to lowercase
    s = str(month_in).strip().lower()

    # If numeric string
    if s.isdigit():
        m = int(s)
        if 1 <= m <= 12:
            return m
        else:
            raise ValueError("Month out of range")

    # Dictionary for month names
    months = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "sept": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }

    if s in months:
        return months[s]

    raise ValueError(f"Unrecognized month: {month_in}")

def checkBirthday(day, month, year):
    """
    Check birthday:
    - Year must be between 1901 and 2024 (inclusive).
    - Month can be a number or a name ("10" or "October")
    - Day must be valid for that month and year (leap years considered).
    """

    if year < 1901 or year > 2024:
        return (False, "Year must be between 1901 and 2024")

    try:
        # Convert month into a number (1 to 12)
        m = monthConverter(month)

        # Convert day and year to integers
        d = int(day)
        y = int(year)

        # Use datetime.date to check if the date really exists
        date(y, m, d)

        return (True, "")

    except Exception as e:
        return (False, f"Invalid date: {e}")

def getLuckyNumber(day, month, year):
    """
    Calculate the Lucky Number from a birthday.
   
    Returns:
        Lucky Number as an integer.
    """
    # Check the birthday is valid
    ok, msg = checkBirthday(day, month, year)
    if not ok:
        raise ValueError(f"Invalid birthday: {msg}")

    # Convert month to number
    m = monthConverter(month)

    # digit-sum day, month, and year
    d_part = addDigits(int(day))
    m_part = addDigits(int(m))
    y_part = addDigits(int(year))

    # Add them together
    total = d_part + m_part + y_part

    # Reduce the result to a single digit or a master number (11, 22, 33)
    return reduceNumber(total)

def getLuckyAnimal(lucky_number):
    """
    Return the Lucky Animal for a given lucky number.
 
    Raises ValueError if no animal is mapped to the number.
    """
    animals = {
        1: "Parrot",
        2: "Rabbit",
        3: "Elephant",
        4: "Beetles",
        5: "Bears",
        6: "Deer",
        7: "Crane",
        8: "Horse",
        9: "Fish",
        11: "Dolphin",
        22: "Lion",
        33: "Turtle"
    }

    if lucky_number in animals:
        return animals[lucky_number]
    else:
        raise ValueError(f"No animal for Lucky Number {lucky_number}")

def getGeneration(year):
    """
    Returns the generation name for a given birth year.
    """
    if 1901 <= year <= 1945:
        return "Silent Generation"
    elif 1946 <= year <= 1964:
        return "Baby Boomers"
    elif 1965 <= year <= 1979:
        return "Generation X"
    elif 1980 <= year <= 1994:
        return "Millennials"
    elif 1995 <= year <= 2009:
        return "Generation Z"
    elif 2010 <= year <= 2024:
        return "Generation Alpha"
    else:
        raise ValueError("Year must be between 1901 and 2024")

def makeProfile(day, month, year):
    """
    Build a profile for one person

    Raises ValueError if the birthday is invalid.
    """
    ok, msg = checkBirthday(day, month, year)
    if not ok:
        raise ValueError(f"Invalid birthday: {msg}")

    m_num = monthConverter(month)
    ln = getLuckyNumber(day, m_num, year)

    return {
        "day": int(day),
        "month": int(m_num),
        "year": int(year),
        "lucky_number": ln,
        "is_master": isMasterNumber(ln),
        "animal": getLuckyAnimal(ln),
        "generation": getGeneration(int(year)),
    }

def compareProfiles(a, b):
    """
    Compare two people by Lucky Number and Lucky Animal.
    Args: a or b can be tuple OR profile dict
    """
    #Normalize profile a into dict
    if isinstance(a, dict):
        pa = a
    else:
        pa = makeProfile(a[0], a[1], a[2])
    #Normalize profile b into dict
    if isinstance(b, dict):
        pb = b
    else:
        pb = makeProfile(b[0], b[1], b[2])

    return {
        "same_number": pa["lucky_number"] == pb["lucky_number"],
        "same_animal": pa["animal"] == pb["animal"],
    }

def getBirthdayInput():
    """
    Ask user to input a birthday using keyboard and return (day, month, year).
    Validates input with checkBirthday. Month is normalized to 1..12.
    """
    day = int(input("Day (1-31): "))
    month_raw = input("Month (number or name): ")
    year = int(input("Year (1901-2024): "))

    ok, msg = checkBirthday(day, month_raw, year)
    if not ok:
        raise ValueError(f"Invalid birthday: {msg}")

    return (day, monthConverter(month_raw), year)

def readBirthdaysFile(path):
    """
    Read birthdays from a text/CSV file.
    Accepts rows like: 13,Nov,1987
    Normalizes month to 1..12.
    """
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                continue
            d_s, m_s, y_s = parts
            try:
                d = int(d_s)
                y = int(y_s)
            except ValueError:
                continue

            ok, msg = checkBirthday(d, m_s, y)
            if not ok:
                print(f"Excluding invalid date: {line} ({msg})")
                continue

            results.append((d, monthConverter(m_s), y))
    return results

def showProfile(profile):
    """
    Print a single profile; raise ValueError on missing keys.
    """
    required = {"day","month","year","lucky_number","is_master","animal","generation"}
    missing = required - set(profile.keys())
    if missing:
        raise ValueError(f"Missing keys: {sorted(missing)}")

    print(f"Birthday     : {profile['day']}-{profile['month']}-{profile['year']}")
    print(f"Lucky Number : {profile['lucky_number']} ({'Master' if profile['is_master'] else 'Normal'})")
    print(f"Lucky Animal : {profile['animal']}")
    print(f"Generation   : {profile['generation']}")


def saveProfile(profile, path):
    """
    Validate and append a profile to a file; raise ValueError on missing keys.
    """
    required = {"day","month","year","lucky_number","is_master","animal","generation"}
    missing = required - set(profile.keys())
    if missing:
        raise ValueError(f"Missing keys: {sorted(missing)}")

    line = (
        f"{profile['day']}-{profile['month']}-{profile['year']},"
        f"{profile['lucky_number']},"
        f"{'Master' if profile['is_master'] else 'Normal'},"
        f"{profile['animal']},"
        f"{profile['generation']}\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)


def mainProgram():
    """
    An interactive menu that wraps all function within the code
    """
    print("1 = Keyboard")
    print("2 = File")
    print("3 = Compare two birthdays")
    print("4 = Show a profile (keyboard)")
    print("5 = Save a profile (keyboard -> file)")
    choice = input("Choose: ").strip()

    if choice == "1":
	#option 1: Enter one birthday, build profile, show on screen
        try:
            d, m, y = getBirthdayInput()
            p = makeProfile(d, m, y)
            showProfile(p)
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "2":
	#option 2: Read birthdays from file, show each profile
        path = input("File path: ").strip()
        try:
            rows = readBirthdaysFile(path)
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        for d, m, y in rows:
            try:
                p = makeProfile(d, m, y)
                showProfile(p)
            except Exception as e:
                print(f"Skipping row ({d},{m},{y}): {e}")

    elif choice == "3":
	#option 3: Compare two birthdays
        try:
            print("Enter first birthday:")
            d1, m1, y1 = getBirthdayInput()
            print("Enter second birthday:")
            d2, m2, y2 = getBirthdayInput()

            result = compareProfiles((d1, m1, y1), (d2, m2, y2))
            print(f"Same Lucky Number : {result['same_number']}")
            print(f"Same Lucky Animal : {result['same_animal']}")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "4":
        try:
            d, m, y = getBirthdayInput()
            p = makeProfile(d, m, y)
            showProfile(p)
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "5":
        try:
            d, m, y = getBirthdayInput()
            p = makeProfile(d, m, y)
            showProfile(p)  # show before saving
            out_path = input("Enter output file path (ex: profiles.txt): ").strip()
            saveProfile(p, out_path)
            print(f"Profile saved to {out_path}")
        except Exception as e:
            print(f"Error: {e}")

    else:
        print("Invalid choice")

if __name__ == "__main__":
    mainProgram()
