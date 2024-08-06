import csv
from datetime import datetime
from collections import defaultdict


def display_menu():
    print("\nExpense Tracker")
    print("1. Record Expense")
    print("2. View Expenses")
    print("3. Filter Expenses")
    print("4. Show Summary")
    print("5. Generate Report")
    print("6. Exit")


def record_expense():
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be positive. Please try again.")
                continue
        except ValueError:
            print("Invalid amount. Please enter a numerical value.")
            continue

        category = input("Enter category: ")
        description = input("Enter description: ")

        with open("expenses.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [amount, category, description, datetime.now().strftime("%Y-%m-%d")]
            )

        print("Expense recorded successfully.")
        break


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    print("\nExpenses:")
    for expense in expenses:
        print(
            f"Date: {expense[3]}, Amount: {expense[0]}, Category: {expense[1]}, Description: {expense[2]}"
        )


def filter_expenses():
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            expenses = [row for row in reader if len(row) == 4]

            if not expenses:
                print("No expenses recorded.")
                return

            filter_type = input(
                "Filter by (1) Category, (2) Date Range, or (3) Multiple Categories: "
            )

            if filter_type == "1":
                category = input("Enter category to filter by: ")
                filtered_expenses = [
                    exp
                    for exp in expenses
                    if exp[1].strip().lower() == category.strip().lower()
                ]
                view_expenses(filtered_expenses)
            elif filter_type == "2":
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
                view_expenses(filtered_expenses)
            elif filter_type == "3":
                categories = input("Enter categories separated by commas: ").split(",")
                categories = [cat.strip().lower() for cat in categories]
                filtered_expenses = [
                    exp for exp in expenses if exp[1].strip().lower() in categories
                ]
                view_expenses(filtered_expenses)
            else:
                print("Invalid filter option.")
    except FileNotFoundError:
        print("No expense data found.")


def show_summary():
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            expenses = [row for row in reader if len(row) == 4]

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
    except FileNotFoundError:
        print("No expense data found.")


def generate_report():
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            expenses = [row for row in reader if len(row) == 4]

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
    except FileNotFoundError:
        print("No expense data found.")


def main():
    while True:
        display_menu()
        choice = input("Select an option: ")

        if choice == "1":
            record_expense()
        elif choice == "2":
            try:
                with open("expenses.csv", mode="r") as file:
                    reader = csv.reader(file)
                    expenses = [row for row in reader if len(row) == 4]
                view_expenses(expenses)
            except FileNotFoundError:
                print("No expense data found.")
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            generate_report()
        elif choice == "6":
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
