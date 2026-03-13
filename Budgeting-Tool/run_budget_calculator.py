import sys

from budget_engine import MARITAL_STATUSES, calculate_budget_summary, export_budget_summary
from budget_gui import launch_gui
from sample_budget import print_sample_budget


def prompt_bool(prompt):
    return input(prompt).strip().lower() in {"yes", "y"}


def run_cli():
    income = float(input("Enter yearly income (before taxes): $"))

    print("Input your marital status:")
    for code, label in MARITAL_STATUSES.items():
        print(f"{code}. {label}")
    marital_status = int(input("Type the number corresponding to your marital status: "))

    state = input("Enter your state (example: GA or Georgia): ")
    include_tithing = prompt_bool("Are you tithing? (yes/no): ")
    charitable_giving = float(
        input("Enter yearly charitable giving outside of tithing: $")
    )
    owns_home = prompt_bool("Do you own a home? (yes/no): ")
    home_value = float(input("How much is your home worth? $")) if owns_home else 0

    summary = calculate_budget_summary(
        income=income,
        marital_status=marital_status,
        state=state,
        include_tithing=include_tithing,
        charitable_giving=charitable_giving,
        owns_home=owns_home,
        home_value=home_value,
    )

    if not summary["supported"]:
        print("That state's full tax system is not added yet.")
        print("Federal tax owed: $", round(summary["federal_tax"], 2))
        return

    details = summary["taxable_income_details"]
    print("Gross income: $", round(details["gross_income"], 2))
    print("Standard deduction: $", round(details["standard_deduction"], 2))
    print("Tithing deduction: $", round(details["tithing_amount"], 2))
    print(
        "Other charitable giving deduction: $",
        round(details["charitable_giving"], 2),
    )
    print("Deduction used: $", round(details["deduction_used"], 2))
    print("Taxable income: $", round(details["taxable_income"], 2))
    print("Federal tax owed: $", round(summary["federal_tax"], 2))
    print("FICA tax owed: $", round(summary["fica_tax"], 2))
    print("State tax owed: $", round(summary["state_tax"], 2))
    if owns_home:
        print("Estimated property tax owed: $", round(summary["property_tax"], 2))
    print("Total tax owed: $", round(summary["total_tax"], 2))
    print("Take-home pay: $", round(summary["take_home"], 2))
    print("Effective tax rate:", round(summary["effective_rate"], 2), "%")
    print("")
    monthly_income = round(summary["monthly_income"], 2)
    print("Monthly Budget Amount: $", monthly_income)
    print_sample_budget(
        monthly_income,
        include_tithing=include_tithing,
        property_tax_monthly=summary["property_tax"] / 12,
    )

    if prompt_bool("Export sample budget to Excel? (yes/no): "):
        output_path = input(
            "Enter Excel file name (example: sample_budget.xlsx): "
        ).strip()
        if not output_path:
            output_path = "sample_budget.xlsx"

        export_budget_summary(
            summary,
            output_path,
            include_tithing=include_tithing,
        )
        print(f"Sample budget exported to {output_path}")


def main():
    if "--cli" in sys.argv:
        run_cli()
        return

    launch_gui()


if __name__ == "__main__":
    main()
