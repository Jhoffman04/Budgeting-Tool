from federal import calculate_federal_tax
from sample_budget import print_sample_budget
from state import calculate_state_tax


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
    owns_home_input = input("Do you own a home? (yes/no): ").strip().lower()
    owns_home = owns_home_input in {"yes", "y"}

    property_tax = 0
    if owns_home:
        home_value = float(input("How much is your home worth? $"))
        property_tax = home_value * 0.009

    federal_tax = calculate_federal_tax(income, marital_status)
    state_tax = calculate_state_tax(income, state)

    if state_tax is None:
        print("That state's full tax system is not added yet.")
        print("Federal tax owed: $", round(federal_tax, 2))
        return

    total_tax = federal_tax + state_tax + property_tax
    take_home = income - total_tax
    effective_rate = (total_tax / income) * 100 if income > 0 else 0

    print("Federal tax owed: $", round(federal_tax, 2))
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
