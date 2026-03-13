from federal import calculate_bracket_tax


def normalize_state(state_input):
    state_input = state_input.strip().upper()

    aliases = {
        "ALABAMA": "AL",
        "ALASKA": "AK",
        "ARIZONA": "AZ",
        "ARKANSAS": "AR",
        "CALIFORNIA": "CA",
        "COLORADO": "CO",
        "CONNECTICUT": "CT",
        "DELAWARE": "DE",
        "FLORIDA": "FL",
        "GEORGIA": "GA",
        "HAWAII": "HI",
        "IDAHO": "ID",
        "ILLINOIS": "IL",
        "INDIANA": "IN",
        "IOWA": "IA",
        "KANSAS": "KS",
        "KENTUCKY": "KY",
        "LOUISIANA": "LA",
        "MAINE": "ME",
        "MARYLAND": "MD",
        "MASSACHUSETTS": "MA",
        "MICHIGAN": "MI",
        "MINNESOTA": "MN",
        "MISSISSIPPI": "MS",
        "MISSOURI": "MO",
        "MONTANA": "MT",
        "NEBRASKA": "NE",
        "NEVADA": "NV",
        "NEW HAMPSHIRE": "NH",
        "NEW JERSEY": "NJ",
        "NEW MEXICO": "NM",
        "NEW YORK": "NY",
        "NORTH CAROLINA": "NC",
        "NORTH DAKOTA": "ND",
        "OHIO": "OH",
        "OKLAHOMA": "OK",
        "OREGON": "OR",
        "PENNSYLVANIA": "PA",
        "RHODE ISLAND": "RI",
        "SOUTH CAROLINA": "SC",
        "SOUTH DAKOTA": "SD",
        "TENNESSEE": "TN",
        "TEXAS": "TX",
        "UTAH": "UT",
        "VERMONT": "VT",
        "VIRGINIA": "VA",
        "WASHINGTON": "WA",
        "WEST VIRGINIA": "WV",
        "WISCONSIN": "WI",
        "WYOMING": "WY",
    }

    return aliases.get(state_input, state_input)


NO_INCOME_TAX_STATES = {
    "AK",
    "FL",
    "NV",
    "NH",
    "SD",
    "TN",
    "TX",
    "WA",
    "WY",
}

FLAT_TAX_RATES = {
    "AZ": 0.0250,
    "CO": 0.0425,
    "GA": 0.0519,
    "ID": 0.05695,
    "IL": 0.0495,
    "IN": 0.0300,
    "IA": 0.0380,
    "KY": 0.0400,
    "LA": 0.0300,
    "MI": 0.0425,
    "NC": 0.0399,
    "PA": 0.0307,
    "UT": 0.0455,
}

BRACKET_STATES = {
    "AL": [(500, 0.02), (3000, 0.04), (float("inf"), 0.05)],
    "AR": [(4500, 0.02), (float("inf"), 0.039)],
    "CA": [
        (10756, 0.01),
        (25499, 0.02),
        (40245, 0.04),
        (55866, 0.06),
        (70606, 0.08),
        (360659, 0.093),
        (432787, 0.103),
        (721314, 0.113),
        (1000000, 0.123),
        (float("inf"), 0.133),
    ],
    "CT": [
        (10000, 0.02),
        (50000, 0.045),
        (100000, 0.055),
        (200000, 0.06),
        (250000, 0.065),
        (500000, 0.069),
        (float("inf"), 0.0699),
    ],
    "DE": [
        (5000, 0.022),
        (10000, 0.039),
        (20000, 0.048),
        (25000, 0.052),
        (60000, 0.0555),
        (float("inf"), 0.066),
    ],
    "HI": [
        (9600, 0.014),
        (14400, 0.032),
        (19200, 0.055),
        (24000, 0.064),
        (36000, 0.068),
        (48000, 0.072),
        (125000, 0.076),
        (175000, 0.079),
        (225000, 0.0825),
        (275000, 0.09),
        (325000, 0.10),
        (float("inf"), 0.11),
    ],
    "KS": [(23000, 0.052), (float("inf"), 0.0558)],
    "ME": [(26800, 0.058), (63450, 0.0675), (float("inf"), 0.0715)],
    "MD": [
        (1000, 0.02),
        (2000, 0.03),
        (3000, 0.04),
        (100000, 0.0475),
        (125000, 0.05),
        (150000, 0.0525),
        (250000, 0.055),
        (float("inf"), 0.0575),
    ],
    "MA": [(1083150, 0.05), (float("inf"), 0.09)],
    "MN": [
        (32570, 0.0535),
        (106990, 0.068),
        (198630, 0.0785),
        (float("inf"), 0.0985),
    ],
    "MO": [
        (2626, 0.02),
        (3939, 0.025),
        (5252, 0.03),
        (6565, 0.035),
        (7878, 0.04),
        (9191, 0.045),
        (float("inf"), 0.047),
    ],
    "MT": [(21100, 0.047), (float("inf"), 0.059)],
    "NE": [
        (4030, 0.0246),
        (24120, 0.0351),
        (38870, 0.0501),
        (float("inf"), 0.052),
    ],
    "NJ": [
        (20000, 0.014),
        (35000, 0.0175),
        (40000, 0.035),
        (75000, 0.05525),
        (500000, 0.0637),
        (1000000, 0.0897),
        (float("inf"), 0.1075),
    ],
    "NM": [
        (5500, 0.015),
        (16500, 0.032),
        (33500, 0.043),
        (66500, 0.047),
        (210000, 0.049),
        (float("inf"), 0.059),
    ],
    "NY": [
        (8500, 0.04),
        (11700, 0.045),
        (13900, 0.0525),
        (80650, 0.055),
        (215400, 0.06),
        (1077550, 0.0685),
        (5000000, 0.0965),
        (25000000, 0.103),
        (float("inf"), 0.109),
    ],
    "ND": [(244825, 0.0195), (float("inf"), 0.025)],
    "OK": [
        (1000, 0.0025),
        (2500, 0.0075),
        (3750, 0.0175),
        (4900, 0.0275),
        (7200, 0.0375),
        (float("inf"), 0.0475),
    ],
    "OR": [
        (4400, 0.0475),
        (11050, 0.0675),
        (125000, 0.0875),
        (float("inf"), 0.099),
    ],
    "RI": [(79900, 0.0375), (181650, 0.0475), (float("inf"), 0.0599)],
    "SC": [(3560, 0.0), (17830, 0.03), (float("inf"), 0.062)],
    "VT": [
        (47900, 0.0335),
        (116000, 0.066),
        (242000, 0.076),
        (float("inf"), 0.0875),
    ],
    "VA": [(3000, 0.02), (5000, 0.03), (17000, 0.05), (float("inf"), 0.0575)],
    "WV": [
        (10000, 0.0222),
        (25000, 0.0296),
        (40000, 0.0333),
        (60000, 0.0444),
        (float("inf"), 0.0482),
    ],
    "WI": [
        (14680, 0.035),
        (29370, 0.044),
        (323290, 0.053),
        (float("inf"), 0.0765),
    ],
}


def calculate_special_flat_state_tax(income, state):
    if state == "MS":
        return max(0, income - 10000) * 0.044

    if state == "OH":
        return max(0, income - 26050) * 0.0275

    return None


def calculate_state_tax(income, state_input):
    state = normalize_state(state_input)

    if state in NO_INCOME_TAX_STATES:
        return 0

    if state in FLAT_TAX_RATES:
        return income * FLAT_TAX_RATES[state]

    special_tax = calculate_special_flat_state_tax(income, state)
    if special_tax is not None:
        return special_tax

    if state in BRACKET_STATES:
        return calculate_bracket_tax(income, BRACKET_STATES[state])

    return None
