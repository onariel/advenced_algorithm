def message_scan(s):
    caps = 0
    marks = 0
    letter_combo = 0
    last_letter = ""
    for c in s:
        if 65 <= ord(c) <= 90:
            caps += 1
        elif c == "!" or c == "?":
            marks += 1
        if c == last_letter:
            letter_combo += 1
            if letter_combo == 4:
                return "spam"
        else:
            letter_combo = 0
        last_letter = c
    ratio = caps / len(s)
    if marks < 3 and ratio < 0.3:
        return "CALM"
    elif marks > 4 or ratio > 0.6:
        return "AGGRESSIVE"
    return "URGENT"


print(message_scan("heyyyyy"))
print(message_scan("Hey, want to connect?"))
print(message_scan("PLEASE ACCEPT MY REQUEST!!!"))
print(message_scan("Are you free? I need to talk!!!"))