
def validate_password(
    password,
    letter,
    min_count,
    max_count
):
    """Check to see if letter appears in password between
    min_count and max_count times """
    count = password.count(letter)
    return count >= min_count and count <= max_count

def validate_password2(
    password,
    letter,
    first_pos,
    second_pos
):
    """Check to see if letter appears in password at
    first_pos OR second_pos (exactly once), where
    positions are ONE-INDEXED """
    count = password.count(letter)
    first_match = (password[first_pos - 1] == letter)
    second_match = (password[second_pos - 1] == letter)
    return (first_match + second_match) == 1

if __name__ == "__main__":
    
    valid_count = 0
    valid_count2 = 0

    with open('day2_input.txt') as fp:
        text = fp.read()
    
    # line format 
    # number-number letter: password
    # example:
    # 16-18 b: qbbbbbfbbbbbbbbnbd
    for line in text.split('\n'):
        numberstr, letter, password = line.split()
        n1, n2 = [int(i) for i in numberstr.split('-')]
        letter = letter[0]
        if validate_password(password, letter, n1, n2):
            valid_count += 1
        if validate_password2(password, letter, n1, n2):
            valid_count2 += 1
            
    print("Part A", valid_count)
    print("Part B", valid_count2)