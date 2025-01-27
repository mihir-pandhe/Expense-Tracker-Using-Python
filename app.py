import csv
from datetime import datetime
from collections import defaultdict


class ExpenseTracker:

    def __init__(self):
        self.menu_options = {
            "1": self.record_expense,
            "2": self.view_expenses,
            "3": self.filter_expenses,
            "4": self.show_summary,
            "5": self.generate_report,
            "6": self.exit_program,
        }
        self.file_path = "expenses.csv"

    def display_menu(self):
        print("\n--- Expense Tracker ---")
        print("1. Record Expense")
        print("2. View Expenses")
        print("3. Filter Expenses")
        print("4. Show Summary")
        print("5. Generate Report")
        print("6. Exit")
        print("-----------------------")

    def record_expense(self):
        while True:
            try:
                amount = float(input("Enter amount: "))
                if amount <= 0:
                    print("Amount must be positive. Please try again.")
                    continue
            except ValueError:
                print("Invalid amount. Please enter a numerical value.")
                continue

            category = input("Enter category: ").strip()
            description = input("Enter description: ").strip()

            if not category or not description:
                print("Category and description cannot be empty. Please try again.")
                continue

            try:
                with open(self.file_path, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [
                            amount,
                            category,
                            description,
                            datetime.now().strftime("%Y-%m-%d"),
                        ]
                    )
                print("Expense recorded successfully.")
            except IOError:
                print("An error occurred while writing to the file.")
            break

    def view_expenses(self):
        expenses = self.load_expenses()
        if not expenses:
            print("No expenses recorded.")
            return

        print("\nExpenses:")
        for expense in expenses:
            print(
                f"Date: {expense[3]}, Amount: {expense[0]}, Category: {expense[1]}, Description: {expense[2]}"
            )

    def filter_expenses(self):
        expenses = self.load_expenses()
        if not expenses:
            print("No expenses recorded.")
            return

        filter_type = input(
            "Filter by (1) Category, (2) Date Range, or (3) Multiple Categories: "
        )

        if filter_type == "1":
            self.filter_by_category(expenses)
        elif filter_type == "2":
            self.filter_by_date_range(expenses)
        elif filter_type == "3":
            self.filter_by_multiple_categories(expenses)
        else:
            print("Invalid filter option.")

    def filter_by_category(self, expenses):
        category = input("Enter category to filter by: ").strip().lower()
        filtered_expenses = [
            exp for exp in expenses if exp[1].strip().lower() == category
        ]
        self.view_expenses_list(filtered_expenses)

    def filter_by_date_range(self, expenses):
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        filtered_expenses = [
            exp
            for exp in expenses
            if start_date <= datetime.strptime(exp[3], "%Y-%m-%d") <= end_date
        ]
        self.view_expenses_list(filtered_expenses)

    def filter_by_multiple_categories(self, expenses):
        categories = input("Enter categories separated by commas: ").split(",")
        categories = [cat.strip().lower() for cat in categories]
        filtered_expenses = [
            exp for exp in expenses if exp[1].strip().lower() in categories
        ]
        self.view_expenses_list(filtered_expenses)

    def show_summary(self):
        expenses = self.load_expenses()
        if not expenses:
            print("No expenses recorded.")
            return

        total_expenses = sum(float(exp[0]) for exp in expenses)
        category_totals = defaultdict(float)

        for exp in expenses:
            category_totals[exp[1].strip()] += float(exp[0])

        print("\nSummary:")
        print(f"Total Expenses: ${total_expenses:.2f}")
        for category, total in category_totals.items():
            print(f"Total for {category}: ${total:.2f}")

    def generate_report(self):
        expenses = self.load_expenses()
        if not expenses:
            print("No expenses recorded.")
            return

        monthly_totals = defaultdict(float)
        category_totals = defaultdict(float)

        for exp in expenses:
            date = datetime.strptime(exp[3], "%Y-%m-%d")
            month = date.strftime("%Y-%m")
            monthly_totals[month] += float(exp[0])
            category_totals[exp[1].strip()] += float(exp[0])

        try:
            with open("report.txt", mode="w") as file:
                file.write("Expense Report\n\n")
                file.write("Monthly Totals:\n")
                for month, total in sorted(monthly_totals.items()):
                    file.write(f"{month}: ${total:.2f}\n")
                file.write("\nTop Spending Categories:\n")
                for category, total in sorted(
                    category_totals.items(), key=lambda x: x[1], reverse=True
                ):
                    file.write(f"{category}: ${total:.2f}\n")
            print("Report generated successfully. Check 'report.txt'.")
        except IOError:
            print("An error occurred while writing the report file.")

    def load_expenses(self):
        try:
            with open(self.file_path, mode="r") as file:
                reader = csv.reader(file)
                return [row for row in reader if len(row) == 4]
        except FileNotFoundError:
            print("No expense data found.")
            return []
        except IOError:
            print("An error occurred while reading the file.")
            return []

    def view_expenses_list(self, expenses):
        if not expenses:
            print("No expenses found for the given criteria.")
        else:
            print("\nFiltered Expenses:")
            for expense in expenses:
                print(
                    f"Date: {expense[3]}, Amount: {expense[0]}, Category: {expense[1]}, Description: {expense[2]}"
                )

    def exit_program(self):
        print("Exiting Expense Tracker.")
        exit()

    def main(self):
        while True:
            self.display_menu()
            choice = input("Select an option: ").strip()
            action = self.menu_options.get(choice)
            if action:
                action()
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    ExpenseTracker().main()
