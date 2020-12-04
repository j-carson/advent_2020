import string


def check_passport_keys(passport):
    """Check that input passport dictionary has all vaild keys, or all valid keys except 'cid'
    """
    all_fields = set(("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid",))
    ok_to_skip = set(("cid",))
    fields_present = set(passport.keys())
    return fields_present == all_fields or (all_fields - fields_present) == ok_to_skip


def number_between_or_die(num, low, high):
    assert low <= int(num) <= high


def validate_passport(passport):
    """Checks both the keys and the values of the input passport dictionary"""

    def key_between(key, low, high):
        number_between_or_die(passport[key], low, high)

    try:
        assert check_passport_keys(passport)

        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        key_between("byr", 1920, 2002)

        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        key_between("iyr", 2010, 2020)

        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        key_between("eyr", 2020, 2030)

        # hgt (Height) - a number followed by either cm or in:
        hgt = passport["hgt"]
        # If cm, the number must be at least 150 and at most 193.
        if hgt.endswith("cm"):
            number_between_or_die(hgt[:-2], 150, 193)
        # If in, the number must be at least 59 and at most 76.
        elif hgt.endswith("in"):
            number_between_or_die(hgt[:-2], 59, 76)
        else:
            return False

        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        hcl = passport["hcl"]
        assert hcl.startswith("#")
        assert sum((c in string.hexdigits for c in hcl[1:])) == 6

        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        assert passport["ecl"] in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")

        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        pid = passport["pid"]
        assert sum((c.isdigit() for c in pid)) == 9

    except (AssertionError, KeyError):
        return False

    return True


def parse_passport(pass_string):
    """Convert passport string to a dictionary"""
    return {s[0]: s[1] for s in (w.split(":") for w in pass_string.split())}


if __name__ == "__main__":
    with open("passports.txt") as fp:
        text = fp.read()
    passports = [parse_passport(passtring) for passtring in text.split("\n\n")]

    n_check = sum(check_passport_keys(p) for p in passports)
    print(n_check)

    n_validate = sum(validate_passport(p) for p in passports)
    print(n_validate)
