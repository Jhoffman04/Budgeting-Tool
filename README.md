# Budgeting Tool

This project is a Python budgeting planner that estimates taxes, calculates take-home pay, and turns the result into a sample monthly budget.

It supports both:

- a desktop GUI
- a command-line interface

## What The Program Does

The tool asks for a user's:

- annual income
- marital status
- state
- tithing preference
- charitable giving
- homeownership status
- home value

From that information, it calculates:

- taxable income
- federal income tax
- FICA tax
- state income tax
- estimated property tax
- annual take-home pay
- monthly take-home pay
- a suggested monthly budget breakdown

If the user is tithing, the budget automatically rebalances the other categories so the total budget still stays at 100%.

The tool can also export the sample monthly budget to an Excel `.xlsx` file.

## Main Features

- Filing-status-based taxable income calculation
- Standard deduction support
- Tithing and charitable giving adjustments
- State tax support for many U.S. states
- Estimated property tax using `0.9%` of home value
- Monthly sample budget generation
- Tithing-aware budget percentage rebalancing
- Excel export for the budget
- GUI and CLI interfaces

## Project Files

- `run_budget_calculator.py`: Main entry point for the app
- `budget_gui.py`: Desktop GUI
- `budget_engine.py`: Shared calculation logic
- `taxable_income.py`: Taxable income calculations
- `federal.py`: Federal tax brackets and FICA calculation
- `state.py`: State income tax logic
- `sample_budget.py`: Budget category allocation and Excel export

## Requirements

- Python 3
- `tkinter` available in your Python installation for the GUI

No third-party Excel package is required for export. The workbook export uses Python's standard library.

## How To Run

Open a terminal in the project folder:

```bash
cd "/Users/userName/Documents/New project/Budgeting-Tool"
```

### Run The GUI

```bash
python3 run_budget_calculator.py
```

This launches the desktop budgeting app.

### Run The CLI

```bash
python3 run_budget_calculator.py --cli
```

This runs the interactive command-line version.

## How To Use The Program

### In The GUI

1. Enter annual income.
2. Choose marital status.
3. Enter your state.
4. Choose whether you tithe.
5. Enter annual charitable giving outside of tithing.
6. Choose whether you own a home.
7. If you own a home, enter the home's value.
8. Run the calculation.
9. Review the tax summary, take-home pay, and monthly budget.
10. Export the budget to Excel if needed.

### In The CLI

The CLI will prompt you for the same information in the terminal and then print:

- taxable income details
- tax totals
- monthly take-home pay
- sample budget categories

At the end, it asks whether you want to export the sample budget to Excel.

## Budget Assumptions

The app uses a simplified planning model:

- Tithing is treated as `10%` of income when enabled.
- Property tax is estimated at `0.9%` of the home's value.
- Charitable giving is added to tithing for deduction comparison.
- The larger of standard deduction or charitable/tithing deductions is used for taxable income.
- FICA is calculated from gross income.
- State tax support depends on the states currently defined in `state.py`.

This tool is best used for planning and estimation, not official tax filing.

## Excel Export

When export is selected, the app creates an Excel `.xlsx` file containing:

- the sample monthly budget title
- monthly take-home amount
- each budget category
- the percentage allocation
- the monthly dollar amount

## Example Workflow

1. Run the program.
2. Enter income and filing details.
3. Add charitable giving and home value if applicable.
4. Review the estimated taxes.
5. Review the sample monthly budget.
6. Export the budget to Excel.

## Notes

- Some states may not have complete tax support yet.
- The budget is a sample plan, not a personalized financial recommendation.
- Rounding may cause very small differences in displayed monthly totals.
