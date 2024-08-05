import csv


def display_menu():
    print("\nExpense Tracker")
    print("1. Record Expense")
    print("2. Exit")


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
            writer.writerow([amount, category, description])

        print("Expense recorded successfully.")
        break


def main():
    while True:
        display_menu()
        choice = input("Select an option: ")

        if choice == "1":
            record_expense()
        elif choice == "2":
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
