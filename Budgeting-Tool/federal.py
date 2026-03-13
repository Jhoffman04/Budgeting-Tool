def calculate_bracket_tax(income, brackets):
    tax = 0
    previous_limit = 0

    for limit, rate in brackets:
        if income > limit:
            tax += (limit - previous_limit) * rate
            previous_limit = limit
        else:
            tax += (income - previous_limit) * rate
            break

    return tax


def get_federal_brackets(marital_status):
    if marital_status == 1:
        return [
            (11925, 0.10),
            (48475, 0.12),
            (103350, 0.22),
            (197300, 0.24),
            (250525, 0.32),
            (626350, 0.35),
            (float("inf"), 0.37),
        ]
    if marital_status == 2:
        return [
            (23850, 0.10),
            (96950, 0.12),
            (206700, 0.22),
            (394600, 0.24),
            (501050, 0.32),
            (751600, 0.35),
            (float("inf"), 0.37),
        ]
    if marital_status == 3:
        return [
            (11925, 0.10),
            (48475, 0.12),
            (103350, 0.22),
            (197300, 0.24),
            (250525, 0.32),
            (375800, 0.35),
            (float("inf"), 0.37),
        ]
    if marital_status == 4:
        return [
            (17000, 0.10),
            (64850, 0.12),
            (103350, 0.22),
            (197300, 0.24),
            (250500, 0.32),
            (626350, 0.35),
            (float("inf"), 0.37),
        ]
    return []


def calculate_federal_tax(income, marital_status):
    brackets = get_federal_brackets(marital_status)
    return calculate_bracket_tax(income, brackets)
