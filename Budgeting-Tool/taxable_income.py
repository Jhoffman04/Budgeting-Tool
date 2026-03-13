STANDARD_DEDUCTIONS = {
    1: 14600,  # Single
    2: 29200,  # Married filing jointly / qualifying surviving spouse
    3: 14600,  # Married filing separately
    4: 21900,  # Head of household
}


def get_standard_deduction(marital_status):
    return STANDARD_DEDUCTIONS.get(marital_status, 0)


def calculate_tithing_amount(income, include_tithing):
    if not include_tithing:
        return 0

    return income * 0.10


def calculate_taxable_income(
    income,
    marital_status,
    include_tithing=False,
    charitable_giving=0,
):
    standard_deduction = get_standard_deduction(marital_status)
    tithing_amount = calculate_tithing_amount(income, include_tithing)
    total_charitable_deductions = tithing_amount + charitable_giving
    deduction_used = max(standard_deduction, total_charitable_deductions)
    taxable_income = max(0, income - deduction_used)

    return {
        "gross_income": income,
        "standard_deduction": standard_deduction,
        "tithing_amount": tithing_amount,
        "charitable_giving": charitable_giving,
        "total_charitable_deductions": total_charitable_deductions,
        "deduction_used": deduction_used,
        "taxable_income": taxable_income,
    }
