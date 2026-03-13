from zipfile import ZIP_DEFLATED, ZipFile


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


def export_sample_budget_to_excel(
    monthly_income,
    output_path,
    include_tithing=False,
    property_tax_monthly=0,
):
    budget_items = build_sample_budget(
        monthly_income,
        include_tithing=include_tithing,
        property_tax_monthly=property_tax_monthly,
    )
    rows = [
        ["Sample Monthly Budget", "", ""],
        [f"Based on monthly take-home pay of ${monthly_income:.2f}", "", ""],
        ["", "", ""],
        ["Expense", "Percentage", "Amount"],
    ]

    for item in budget_items:
        percentage = "" if item["percentage"] is None else f"{item['percentage'] * 100:.0f}%"
        rows.append([item["expense"], percentage, item["amount"]])

    write_simple_xlsx(output_path, rows)


def build_sheet_xml(rows):
    row_xml = []

    for row_index, row in enumerate(rows, start=1):
        cells = []

        for column_index, value in enumerate(row, start=1):
            cell_reference = f"{column_letter(column_index)}{row_index}"

            if isinstance(value, (int, float)) and value != "":
                cells.append(
                    f'<c r="{cell_reference}"><v>{value}</v></c>'
                )
            else:
                escaped_value = escape_xml(str(value))
                cells.append(
                    f'<c r="{cell_reference}" t="inlineStr"><is><t>{escaped_value}</t></is></c>'
                )

        row_xml.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(row_xml)}</sheetData>'
        "</worksheet>"
    )


def column_letter(index):
    letters = ""

    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters

    return letters


def escape_xml(value):
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def write_simple_xlsx(output_path, rows):
    content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>"""

    root_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    workbook_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sample Budget" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>"""

    workbook_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>"""

    sheet_xml = build_sheet_xml(rows)

    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as workbook:
        workbook.writestr("[Content_Types].xml", content_types_xml)
        workbook.writestr("_rels/.rels", root_rels_xml)
        workbook.writestr("xl/workbook.xml", workbook_xml)
        workbook.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        workbook.writestr("xl/worksheets/sheet1.xml", sheet_xml)
