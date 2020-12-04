def check_passport(passport):
    all_fields = set(("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid",))
    ok_to_skip = set(("cid",))
    fields = set([word.split(":")[0] for word in passport.split()])
    return fields == all_fields or (all_fields - fields) == ok_to_skip


def validate_passport(passport):
    try:
        assert check_passport(passport)
        fields = {word.split(":")[0]: word.split(":")[1] for word in passport.split()}

        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        byr = int(fields["byr"])
        assert byr >= 1920
        assert byr <= 2002

        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        iyr = int(fields["iyr"])
        assert iyr >= 2010
        assert iyr <= 2020

        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        eyr = int(fields["eyr"])
        assert eyr >= 2020
        assert eyr <= 2030

        # hgt (Height) - a number followed by either cm or in:
        hgt = fields["hgt"]
        # If cm, the number must be at least 150 and at most 193.
        if hgt.endswith("cm"):
            h = int(hgt.replace("cm", ""))
            assert h >= 150
            assert h <= 193
        # If in, the number must be at least 59 and at most 76.
        elif hgt.endswith("in"):
            h = int(hgt.replace("in", ""))
            assert h >= 59
            assert h <= 76
        else:
            return False

        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        hcl = fields["hcl"]
        assert hcl.startswith("#")
        assert sum((c.isdigit() or c in "abcdef" for c in hcl[1:])) == 6

        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        ecl = fields["ecl"]
        assert ecl in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")

        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        pid = fields["pid"]
        assert sum((c.isdigit() for c in pid)) == 9
    except Exception:
        return False

    return True


if __name__ == "__main__":
    with open("passports.txt") as fp:
        text = fp.read()
    passports = text.split("\n\n")

    n_check = sum(check_passport(p) for p in passports)
    print(n_check)

    n_validate = sum(validate_passport(p) for p in passports)
    print(n_validate)
