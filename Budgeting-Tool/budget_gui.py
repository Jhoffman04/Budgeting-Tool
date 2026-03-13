import tkinter as tk
from tkinter import filedialog, font, messagebox, ttk

from budget_engine import MARITAL_STATUSES, calculate_budget_summary, export_budget_summary
from sample_budget import format_percentage


COLORS = {
    "bg": "#f3efe7",
    "panel": "#fffdf8",
    "panel_alt": "#f7f2ea",
    "accent": "#0f766e",
    "accent_soft": "#d8f0ec",
    "text": "#1f2937",
    "muted": "#6b7280",
    "border": "#ddd4c5",
    "success": "#17643c",
    "warning": "#a16207",
}


class BudgetPlannerApp:
    def __init__(self, root):
        self.root = root
        self.summary = None
        self.current_include_tithing = False

        self.root.title("Budgeting Tool")
        self.root.geometry("1320x860")
        self.root.minsize(1120, 760)
        self.root.configure(bg=COLORS["bg"])

        self.font_family = self.pick_font_family()
        self.configure_styles()
        self.build_layout()

    def pick_font_family(self):
        available = set(font.families())
        for family in ("Avenir Next", "SF Pro Display", "Helvetica Neue", "Aptos", "Segoe UI"):
            if family in available:
                return family
        return "TkDefaultFont"

    def configure_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.root.option_add("*Font", (self.font_family, 11))

        style.configure(
            "App.TFrame",
            background=COLORS["bg"],
        )
        style.configure(
            "Card.TFrame",
            background=COLORS["panel"],
            relief="flat",
            borderwidth=1,
        )
        style.configure(
            "AltCard.TFrame",
            background=COLORS["panel_alt"],
            relief="flat",
            borderwidth=1,
        )
        style.configure(
            "Title.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            font=(self.font_family, 28, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["muted"],
            font=(self.font_family, 12),
        )
        style.configure(
            "SectionTitle.TLabel",
            background=COLORS["panel"],
            foreground=COLORS["text"],
            font=(self.font_family, 16, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background=COLORS["panel"],
            foreground=COLORS["text"],
            font=(self.font_family, 11),
        )
        style.configure(
            "Muted.TLabel",
            background=COLORS["panel"],
            foreground=COLORS["muted"],
            font=(self.font_family, 10),
        )
        style.configure(
            "Hero.TLabel",
            background=COLORS["accent"],
            foreground="#ffffff",
            font=(self.font_family, 12),
        )
        style.configure(
            "HeroTitle.TLabel",
            background=COLORS["accent"],
            foreground="#ffffff",
            font=(self.font_family, 22, "bold"),
        )
        style.configure(
            "MetricLabel.TLabel",
            background=COLORS["panel_alt"],
            foreground=COLORS["muted"],
            font=(self.font_family, 10),
        )
        style.configure(
            "MetricValue.TLabel",
            background=COLORS["panel_alt"],
            foreground=COLORS["text"],
            font=(self.font_family, 20, "bold"),
        )
        style.configure(
            "TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text"],
        )
        style.configure(
            "TEntry",
            fieldbackground="#fffdfa",
            foreground=COLORS["text"],
            padding=8,
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
        )
        style.map(
            "TEntry",
            bordercolor=[("focus", COLORS["accent"])],
            lightcolor=[("focus", COLORS["accent"])],
            darkcolor=[("focus", COLORS["accent"])],
        )
        style.configure(
            "TCombobox",
            fieldbackground="#fffdfa",
            foreground=COLORS["text"],
            padding=6,
            arrowsize=16,
        )
        style.configure(
            "Accent.TButton",
            background=COLORS["accent"],
            foreground="#ffffff",
            borderwidth=0,
            focusthickness=3,
            focuscolor=COLORS["accent"],
            padding=(16, 12),
            font=(self.font_family, 11, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#115e59"), ("disabled", "#8fa5a2")],
            foreground=[("disabled", "#f6f4ef")],
        )
        style.configure(
            "Secondary.TButton",
            background=COLORS["accent_soft"],
            foreground=COLORS["accent"],
            borderwidth=0,
            padding=(16, 12),
            font=(self.font_family, 11, "bold"),
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#c2e8e1"), ("disabled", "#e9e4db")],
            foreground=[("disabled", COLORS["muted"])],
        )
        style.configure(
            "TCheckbutton",
            background=COLORS["panel"],
            foreground=COLORS["text"],
        )
        style.configure(
            "Budget.Treeview",
            background="#fffdfa",
            fieldbackground="#fffdfa",
            foreground=COLORS["text"],
            rowheight=34,
            bordercolor=COLORS["border"],
            font=(self.font_family, 10),
        )
        style.configure(
            "Budget.Treeview.Heading",
            background=COLORS["panel_alt"],
            foreground=COLORS["text"],
            relief="flat",
            font=(self.font_family, 10, "bold"),
        )
        style.map(
            "Budget.Treeview",
            background=[("selected", COLORS["accent_soft"])],
            foreground=[("selected", COLORS["text"])],
        )

    def build_layout(self):
        container = ttk.Frame(self.root, style="App.TFrame", padding=24)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=5)
        container.columnconfigure(1, weight=6)
        container.rowconfigure(1, weight=1)

        header = ttk.Frame(container, style="App.TFrame")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="Budget Planning Studio", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            header,
            text="Model taxes, estimate take-home pay, and turn the result into a clean monthly budget in one place.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.build_input_panel(container)
        self.build_results_panel(container)

    def build_input_panel(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card.grid(row=1, column=0, sticky="nsew", padx=(0, 16))
        card.columnconfigure(0, weight=1)

        ttk.Label(card, text="Plan Inputs", style="SectionTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            card,
            text="Fill in your income, filing status, and location details. Home and giving inputs are optional.",
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 18))

        form = ttk.Frame(card, style="Card.TFrame")
        form.grid(row=2, column=0, sticky="nsew")
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        self.income_var = tk.StringVar()
        self.marital_var = tk.StringVar(value=MARITAL_STATUSES[1])
        self.state_var = tk.StringVar()
        self.charitable_var = tk.StringVar(value="0")
        self.tithing_var = tk.BooleanVar(value=False)
        self.owns_home_var = tk.BooleanVar(value=False)
        self.home_value_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="Ready for your first scenario.")

        self.build_field(form, "Annual income", self.income_var, 0, 0, "$85,000")
        self.build_dropdown(
            form,
            "Marital status",
            self.marital_var,
            list(MARITAL_STATUSES.values()),
            0,
            1,
        )
        self.build_field(form, "State", self.state_var, 1, 0, "GA or Georgia")
        self.build_field(form, "Other charitable giving", self.charitable_var, 1, 1, "$0")

        checks = ttk.Frame(form, style="Card.TFrame")
        checks.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        checks.columnconfigure(0, weight=1)
        checks.columnconfigure(1, weight=1)

        ttk.Checkbutton(
            checks,
            text="Include 10% tithing",
            variable=self.tithing_var,
        ).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(
            checks,
            text="Include home ownership estimate",
            variable=self.owns_home_var,
            command=self.toggle_home_value_state,
        ).grid(row=0, column=1, sticky="w")

        self.home_value_entry = self.build_field(
            form,
            "Home value",
            self.home_value_var,
            3,
            0,
            "$350,000",
        )
        self.toggle_home_value_state()

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.grid(row=3, column=0, sticky="ew", pady=(22, 0))
        actions.columnconfigure(0, weight=0)
        actions.columnconfigure(1, weight=0)
        actions.columnconfigure(2, weight=1)

        ttk.Button(
            actions,
            text="Calculate Budget",
            style="Accent.TButton",
            command=self.calculate,
        ).grid(row=0, column=0, sticky="w")
        self.export_button = ttk.Button(
            actions,
            text="Export to Excel",
            style="Secondary.TButton",
            command=self.export,
            state="disabled",
        )
        self.export_button.grid(row=0, column=1, sticky="w", padx=(12, 0))

        self.status_label = ttk.Label(
            card,
            textvariable=self.status_var,
            style="Muted.TLabel",
        )
        self.status_label.grid(row=4, column=0, sticky="w", pady=(14, 0))

    def build_results_panel(self, parent):
        panel = ttk.Frame(parent, style="App.TFrame")
        panel.grid(row=1, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(2, weight=1)

        hero = ttk.Frame(panel, style="Card.TFrame", padding=0)
        hero.grid(row=0, column=0, sticky="ew")
        hero.columnconfigure(0, weight=1)

        hero_inner = tk.Frame(hero, bg=COLORS["accent"], padx=24, pady=24)
        hero_inner.pack(fill="both", expand=True)
        ttk.Label(
            hero_inner,
            text="Monthly Take-Home",
            style="Hero.TLabel",
        ).grid(row=0, column=0, sticky="w")
        self.hero_value = ttk.Label(
            hero_inner,
            text="$0.00",
            style="HeroTitle.TLabel",
        )
        self.hero_value.grid(row=1, column=0, sticky="w", pady=(6, 4))
        self.hero_caption = ttk.Label(
            hero_inner,
            text="Run a calculation to see your after-tax monthly budget.",
            style="Hero.TLabel",
        )
        self.hero_caption.grid(row=2, column=0, sticky="w")

        metrics = ttk.Frame(panel, style="App.TFrame")
        metrics.grid(row=1, column=0, sticky="ew", pady=(16, 16))
        for index in range(4):
            metrics.columnconfigure(index, weight=1)

        self.metric_vars = {
            "federal_tax": tk.StringVar(value="$0.00"),
            "state_tax": tk.StringVar(value="$0.00"),
            "total_tax": tk.StringVar(value="$0.00"),
            "effective_rate": tk.StringVar(value="0.00%"),
        }
        self.build_metric_card(metrics, 0, "Federal Tax", self.metric_vars["federal_tax"])
        self.build_metric_card(metrics, 1, "State Tax", self.metric_vars["state_tax"])
        self.build_metric_card(metrics, 2, "Total Tax", self.metric_vars["total_tax"])
        self.build_metric_card(metrics, 3, "Effective Rate", self.metric_vars["effective_rate"])

        lower = ttk.Frame(panel, style="App.TFrame")
        lower.grid(row=2, column=0, sticky="nsew")
        lower.columnconfigure(0, weight=4)
        lower.columnconfigure(1, weight=3)
        lower.rowconfigure(0, weight=1)

        budget_card = ttk.Frame(lower, style="Card.TFrame", padding=20)
        budget_card.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        budget_card.columnconfigure(0, weight=1)
        budget_card.rowconfigure(1, weight=1)

        ttk.Label(budget_card, text="Suggested Monthly Budget", style="SectionTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )

        columns = ("expense", "allocation", "amount")
        self.budget_tree = ttk.Treeview(
            budget_card,
            columns=columns,
            show="headings",
            style="Budget.Treeview",
        )
        self.budget_tree.heading("expense", text="Category")
        self.budget_tree.heading("allocation", text="Allocation")
        self.budget_tree.heading("amount", text="Amount")
        self.budget_tree.column("expense", width=240, anchor="w")
        self.budget_tree.column("allocation", width=100, anchor="center")
        self.budget_tree.column("amount", width=120, anchor="e")
        self.budget_tree.grid(row=1, column=0, sticky="nsew", pady=(14, 0))

        scrollbar = ttk.Scrollbar(
            budget_card,
            orient="vertical",
            command=self.budget_tree.yview,
        )
        self.budget_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(14, 0))

        details_card = ttk.Frame(lower, style="AltCard.TFrame", padding=20)
        details_card.grid(row=0, column=1, sticky="nsew")
        details_card.columnconfigure(0, weight=1)

        ttk.Label(
            details_card,
            text="Calculation Details",
            style="SectionTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")

        self.detail_vars = {
            "gross_income": tk.StringVar(value="$0.00"),
            "standard_deduction": tk.StringVar(value="$0.00"),
            "deduction_used": tk.StringVar(value="$0.00"),
            "taxable_income": tk.StringVar(value="$0.00"),
            "fica_tax": tk.StringVar(value="$0.00"),
            "property_tax": tk.StringVar(value="$0.00"),
            "allocated_budget": tk.StringVar(value="$0.00"),
            "remaining_budget": tk.StringVar(value="$0.00"),
        }

        detail_rows = [
            ("Gross income", "gross_income"),
            ("Standard deduction", "standard_deduction"),
            ("Deduction used", "deduction_used"),
            ("Taxable income", "taxable_income"),
            ("FICA tax", "fica_tax"),
            ("Property tax", "property_tax"),
            ("Budget allocated", "allocated_budget"),
            ("Unallocated cash", "remaining_budget"),
        ]
        for row_index, (label, key) in enumerate(detail_rows, start=1):
            self.build_detail_row(details_card, row_index, label, self.detail_vars[key])

    def build_field(self, parent, label, variable, row, column, placeholder):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.grid(row=row, column=column, sticky="ew", padx=(0, 14) if column == 0 else (0, 0), pady=(0, 14))
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text=label, style="Body.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))
        entry = ttk.Entry(frame, textvariable=variable)
        entry.grid(row=1, column=0, sticky="ew")
        ttk.Label(frame, text=placeholder, style="Muted.TLabel").grid(row=2, column=0, sticky="w", pady=(6, 0))
        return entry

    def build_dropdown(self, parent, label, variable, values, row, column):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.grid(row=row, column=column, sticky="ew", pady=(0, 14))
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text=label, style="Body.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))
        dropdown = ttk.Combobox(
            frame,
            textvariable=variable,
            values=values,
            state="readonly",
        )
        dropdown.grid(row=1, column=0, sticky="ew")
        return dropdown

    def build_metric_card(self, parent, column, label, value_var):
        card = ttk.Frame(parent, style="AltCard.TFrame", padding=18)
        card.grid(row=0, column=column, sticky="ew", padx=(0, 12) if column < 3 else (0, 0))
        ttk.Label(card, text=label, style="MetricLabel.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(card, textvariable=value_var, style="MetricValue.TLabel").grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )

    def build_detail_row(self, parent, row, label, value_var):
        line = ttk.Frame(parent, style="AltCard.TFrame")
        line.grid(row=row, column=0, sticky="ew", pady=(10 if row == 1 else 6, 0))
        line.columnconfigure(0, weight=1)

        ttk.Label(
            line,
            text=label,
            style="MetricLabel.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            line,
            textvariable=value_var,
            style="Body.TLabel",
        ).grid(row=0, column=1, sticky="e")

    def toggle_home_value_state(self):
        state = "normal" if self.owns_home_var.get() else "disabled"
        self.home_value_entry.configure(state=state)

    def parse_currency(self, value, field_name):
        cleaned = value.replace("$", "").replace(",", "").strip()
        if cleaned == "":
            raise ValueError(f"{field_name} is required.")

        amount = float(cleaned)
        if amount < 0:
            raise ValueError(f"{field_name} cannot be negative.")
        return amount

    def get_marital_status_code(self):
        for code, label in MARITAL_STATUSES.items():
            if label == self.marital_var.get():
                return code
        raise ValueError("Choose a marital status.")

    def calculate(self):
        try:
            income = self.parse_currency(self.income_var.get(), "Annual income")
            charitable = self.parse_currency(
                self.charitable_var.get(),
                "Other charitable giving",
            )
            home_value = 0
            if self.owns_home_var.get():
                home_value = self.parse_currency(self.home_value_var.get(), "Home value")

            marital_status = self.get_marital_status_code()
            state = self.state_var.get().strip()
            if not state:
                raise ValueError("State is required.")

            include_tithing = self.tithing_var.get()
            summary = calculate_budget_summary(
                income=income,
                marital_status=marital_status,
                state=state,
                include_tithing=include_tithing,
                charitable_giving=charitable,
                owns_home=self.owns_home_var.get(),
                home_value=home_value,
            )
        except ValueError as error:
            self.status_var.set(str(error))
            self.export_button.configure(state="disabled")
            messagebox.showerror("Invalid input", str(error))
            return

        self.current_include_tithing = include_tithing
        self.summary = summary
        if not summary["supported"]:
            self.status_var.set("State tax model not available for that location yet.")
            self.render_unsupported(summary)
            return

        self.status_var.set("Calculation updated. You can export the monthly budget when ready.")
        self.render_summary(summary)

    def render_unsupported(self, summary):
        details = summary["taxable_income_details"]
        self.hero_value.configure(text="$0.00")
        self.hero_caption.configure(
            text="State tax support is incomplete for that state, so the full budget view is unavailable."
        )
        self.metric_vars["federal_tax"].set(self.format_currency(summary["federal_tax"]))
        self.metric_vars["state_tax"].set("Unsupported")
        self.metric_vars["total_tax"].set("Pending")
        self.metric_vars["effective_rate"].set("Pending")
        self.detail_vars["gross_income"].set(self.format_currency(details["gross_income"]))
        self.detail_vars["standard_deduction"].set(self.format_currency(details["standard_deduction"]))
        self.detail_vars["deduction_used"].set(self.format_currency(details["deduction_used"]))
        self.detail_vars["taxable_income"].set(self.format_currency(details["taxable_income"]))
        self.detail_vars["fica_tax"].set(self.format_currency(summary["fica_tax"]))
        self.detail_vars["property_tax"].set(self.format_currency(summary["property_tax"]))
        self.detail_vars["allocated_budget"].set("Pending")
        self.detail_vars["remaining_budget"].set("Pending")
        self.export_button.configure(state="disabled")
        for item in self.budget_tree.get_children():
            self.budget_tree.delete(item)

    def render_summary(self, summary):
        details = summary["taxable_income_details"]
        self.hero_value.configure(text=self.format_currency(summary["monthly_income"]))
        self.hero_caption.configure(
            text=f"Annual take-home pay: {self.format_currency(summary['take_home'])}"
        )
        self.metric_vars["federal_tax"].set(self.format_currency(summary["federal_tax"]))
        self.metric_vars["state_tax"].set(self.format_currency(summary["state_tax"]))
        self.metric_vars["total_tax"].set(self.format_currency(summary["total_tax"]))
        self.metric_vars["effective_rate"].set(f"{summary['effective_rate']:.2f}%")

        self.detail_vars["gross_income"].set(self.format_currency(details["gross_income"]))
        self.detail_vars["standard_deduction"].set(self.format_currency(details["standard_deduction"]))
        self.detail_vars["deduction_used"].set(self.format_currency(details["deduction_used"]))
        self.detail_vars["taxable_income"].set(self.format_currency(details["taxable_income"]))
        self.detail_vars["fica_tax"].set(self.format_currency(summary["fica_tax"]))
        self.detail_vars["property_tax"].set(self.format_currency(summary["property_tax"]))
        self.detail_vars["allocated_budget"].set(self.format_currency(summary["allocated_budget"]))
        self.detail_vars["remaining_budget"].set(self.format_currency(summary["remaining_budget"]))
        self.export_button.configure(state="normal")

        for item in self.budget_tree.get_children():
            self.budget_tree.delete(item)

        for item in summary["budget_items"]:
            allocation = "Fixed" if item["percentage"] is None else format_percentage(item["percentage"])
            self.budget_tree.insert(
                "",
                "end",
                values=(
                    item["expense"],
                    allocation,
                    self.format_currency(item["amount"]),
                ),
            )

    def export(self):
        if not self.summary or not self.summary.get("supported"):
            messagebox.showinfo(
                "Nothing to export",
                "Run a supported calculation first so there is a monthly budget to export.",
            )
            return

        output_path = filedialog.asksaveasfilename(
            title="Export Budget",
            defaultextension=".xlsx",
            filetypes=[("Excel workbook", "*.xlsx")],
            initialfile="sample_budget.xlsx",
        )
        if not output_path:
            return

        try:
            export_budget_summary(
                self.summary,
                output_path,
                include_tithing=self.current_include_tithing,
            )
        except OSError as error:
            messagebox.showerror("Export failed", str(error))
            return

        self.status_var.set(f"Budget exported to {output_path}")
        messagebox.showinfo("Export complete", f"Saved budget workbook to:\n{output_path}")

    def format_currency(self, amount):
        return f"${amount:,.2f}"


def launch_gui():
    root = tk.Tk()
    BudgetPlannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
