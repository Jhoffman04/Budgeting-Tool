BASE_BUDGET_PERCENTAGES = [
    ("Rent/Mortgage", 0.30),
    ("Home & Car Insurance", 0.05),
    ("Health Insurance", 0.05),
    ("Retirement", 0.10),
    ("Cable/Internet", 0.03),
    ("Cell Phone", 0.03),
    ("Utilities", 0.05),
    ("Car Gas", 0.05),
    ("Student Loans", 0.07),
    ("Emergency Savings", 0.07),
    ("Groceries Week 1", 0.04),
    ("Groceries Week 2", 0.04),
    ("Groceries Week 3", 0.04),
    ("Groceries Week 4", 0.04),
    ("Entertainment", 0.02),
    ("Misc Expenses", 0.02),
]


def build_sample_budget(monthly_income, include_tithing=False, property_tax_monthly=0):
    budget_percentages = list(BASE_BUDGET_PERCENTAGES)

    if include_tithing:
        budget_percentages.insert(0, ("Tithing", 0.10))

    budget_items = [
        {
            "expense": expense,
            "percentage": percentage,
            "amount": round(monthly_income * percentage, 2),
        }
        for expense, percentage in budget_percentages
    ]

    if property_tax_monthly > 0:
        budget_items.insert(
            1 if include_tithing else 0,
            {
                "expense": "Property Tax",
                "percentage": None,
                "amount": round(property_tax_monthly, 2),
            },
        )

    return budget_items


def print_sample_budget(monthly_income, include_tithing=False, property_tax_monthly=0):
    budget_items = build_sample_budget(
        monthly_income,
        include_tithing=include_tithing,
        property_tax_monthly=property_tax_monthly,
    )

    print("")
    print("Sample Monthly Budget:")
    print(f"Based on monthly take-home pay of ${monthly_income:.2f}")

    for item in budget_items:
        if item["percentage"] is None:
            print(f"{item['expense']}: ${item['amount']:.2f}")
            continue

        percent_label = f"{item['percentage'] * 100:.0f}%"
        print(f"{item['expense']}: {percent_label} = ${item['amount']:.2f}")
