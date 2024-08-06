import csv
from operator import itemgetter
from datetime import datetime


def display_menu():
    print("\nExpense Tracker")
    print("1. Record Expense")
    print("2. View Expenses")
    print("3. Exit")


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


def view_expenses():
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            expenses = [row for row in reader if len(row) == 4]

            if not expenses:
                print("No expenses recorded.")
                return

            sorted_expenses = sorted(
                expenses, key=itemgetter(3, 0)
            )

            print("\nExpenses:")
            for expense in sorted_expenses:
                print(
                    f"Date: {expense[3]}, Amount: {expense[0]}, Category: {expense[1]}, Description: {expense[2]}"
                )
    except FileNotFoundError:
        print("No expense data found.")


def main():
    while True:
        display_menu()
        choice = input("Select an option: ")

        if choice == "1":
            record_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
