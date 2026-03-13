from federal import calculate_federal_tax, calculate_fica_tax
from sample_budget import build_sample_budget, export_sample_budget_to_excel
from state import calculate_state_tax
from taxable_income import calculate_taxable_income


MARITAL_STATUSES = {
    1: "Single",
    2: "Married Filing Jointly / Qualifying Surviving Spouse",
    3: "Married Filing Separately",
    4: "Head of Household",
}


def calculate_property_tax(owns_home, home_value):
    if not owns_home:
        return 0

    return max(0, home_value) * 0.009


def calculate_budget_summary(
    income,
    marital_status,
    state,
    include_tithing=False,
    charitable_giving=0,
    owns_home=False,
    home_value=0,
):
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
    property_tax = calculate_property_tax(owns_home, home_value)

    if state_tax is None:
        return {
            "supported": False,
            "taxable_income_details": taxable_income_details,
            "federal_tax": federal_tax,
            "fica_tax": fica_tax,
            "state_tax": None,
            "property_tax": property_tax,
        }

    total_tax = federal_tax + fica_tax + state_tax + property_tax
    take_home = income - total_tax
    effective_rate = (total_tax / income) * 100 if income > 0 else 0
    monthly_income = take_home / 12 if take_home else 0
    budget_items = build_sample_budget(
        monthly_income,
        include_tithing=include_tithing,
        property_tax_monthly=property_tax / 12,
    )
    allocated_budget = sum(item["amount"] for item in budget_items)
    remaining_budget = monthly_income - allocated_budget

    return {
        "supported": True,
        "taxable_income_details": taxable_income_details,
        "federal_tax": federal_tax,
        "fica_tax": fica_tax,
        "state_tax": state_tax,
        "property_tax": property_tax,
        "total_tax": total_tax,
        "take_home": take_home,
        "effective_rate": effective_rate,
        "monthly_income": monthly_income,
        "budget_items": budget_items,
        "allocated_budget": allocated_budget,
        "remaining_budget": remaining_budget,
    }


def export_budget_summary(summary, output_path, include_tithing=False):
    export_sample_budget_to_excel(
        summary["monthly_income"],
        output_path,
        include_tithing=include_tithing,
        property_tax_monthly=summary["property_tax"] / 12,
    )
