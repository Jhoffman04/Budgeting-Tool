from federal import calculate_federal_tax, calculate_fica_tax
from sample_budget import print_sample_budget
from state import calculate_state_tax
from taxable_income import calculate_taxable_income


def main():
    income = float(input("Enter yearly income (before taxes): $"))

    print("Input your marital status:")
    print("1. Single")
    print("2. Married Filing Jointly / Qualifying Surviving Spouse")
    print("3. Married Filing Separately")
    print("4. Head of Household")
    marital_status = int(input("Type the number corresponding to your marital status: "))

    state = input("Enter your state (example: GA or Georgia): ")
    tithing_input = input("Are you tithing? (yes/no): ").strip().lower()
    include_tithing = tithing_input in {"yes", "y"}
    charitable_giving = float(
        input("Enter yearly charitable giving outside of tithing: $")
    )
    owns_home_input = input("Do you own a home? (yes/no): ").strip().lower()
    owns_home = owns_home_input in {"yes", "y"}

    property_tax = 0
    if owns_home:
        home_value = float(input("How much is your home worth? $"))
        property_tax = home_value * 0.009

    taxable_income_details = calculate_taxable_income(
        income,
        marital_status,
        include_tithing=include_tithing,
        charitable_giving=charitable_giving,
    )
    taxable_income = taxable_income_details["taxable_income"]

    federal_tax = calculate_federal_tax(taxable_income, marital_status)
    fica_tax = calculate_fica_tax(income)
    state_tax = calculate_state_tax(taxable_income, state)

    if state_tax is None:
        print("That state's full tax system is not added yet.")
        print("Federal tax owed: $", round(federal_tax, 2))
        return

    total_tax = federal_tax + fica_tax + state_tax + property_tax
    take_home = income - total_tax
    effective_rate = (total_tax / income) * 100 if income > 0 else 0

    print("Gross income: $", round(income, 2))
    print("Standard deduction: $", round(taxable_income_details["standard_deduction"], 2))
    print(
        "Tithing deduction: $",
        round(taxable_income_details["tithing_amount"], 2),
    )
    print(
        "Other charitable giving deduction: $",
        round(taxable_income_details["charitable_giving"], 2),
    )
    print("Deduction used: $", round(taxable_income_details["deduction_used"], 2))
    print("Taxable income: $", round(taxable_income, 2))
    print("Federal tax owed: $", round(federal_tax, 2))
    print("FICA tax owed: $", round(fica_tax, 2))
    print("State tax owed: $", round(state_tax, 2))
    if owns_home:
        print("Estimated property tax owed: $", round(property_tax, 2))
    print("Total tax owed: $", round(total_tax, 2))
    print("Take-home pay: $", round(take_home, 2))
    print("Effective tax rate:", round(effective_rate, 2), "%")
    print("")
    monthly_income = round(take_home / 12, 2)
    print("Monthly Budget Amount: $", monthly_income)
    print_sample_budget(
        monthly_income,
        include_tithing=include_tithing,
        property_tax_monthly=property_tax / 12,
    )


if __name__ == "__main__":
    main()
