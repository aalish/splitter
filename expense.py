import json
import os

def add_expense():
    print("-------------------------------------------------------------------------\n\n")
    if os.path.isfile('expense_data.json'):
        with open('expense_data.json', 'r') as f:
            data = json.load(f)
        # Add the 'expenses' key if it doesn't exist
            if 'expenses' not in data:
                data['expenses'] = []
    else:
        data={}
        data['expenses'] = []
    with open('expense_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    expense = {}
    expense['name'] = input("Enter the expense name: ")
    expense['amount'] = int(input("Enter the expense amount: "))
    expense['paid_by'] = input("Who paid the expense: ")
    shared_by = input("Enter names of the people who shared the expense (comma separated): ")
    expense['shared_by'] = [name.strip() for name in shared_by.split(',')]
    with open('expense_data.json', 'r') as f:
        data = json.load(f)
        data['expenses'].append(expense)
    with open('expense_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f"{expense['name']} expense added successfully.\n")
    print("-------------------------------------------------------------------------\n\n")

def view_expense():
    print("-------------------------------------------------------------------------\n\n")
    with open('expense_data.json', 'r') as f:
        data = json.load(f)
        if not data['expenses']:
            print("No expenses found.")
            return
        for expense in data['expenses']:
            print(f"Expense Name: {expense['name']}")
            print(f"Expense Amount: {expense['amount']}")
            print(f"Paid By: {expense['paid_by']}")
            for shared in expense['shared_by']:
                print(f"{shared} owes ${(expense['amount']/len(expense['shared_by'])):.2f}")
            print()
    print("-------------------------------------------------------------------------\n\n")

def equalize_payments():
    print("-------------------------------------------------------------------------")
    with open('expense_data.json', 'r') as f:
        data = json.load(f)
        if not data['expenses']:
            print("No expenses found.")
            return
        people = []
        for expense in data['expenses']:
            people.append(expense['paid_by'])
            for shared in expense['shared_by']:
                people.append(shared)
        people = list(set(people))
        payments = {person: 0 for person in people}
        for expense in data['expenses']:
            amount_per_person = expense['amount'] / len(expense['shared_by'])
            for shared in expense['shared_by']:
                payments[shared] += amount_per_person
            payments[expense['paid_by']] -= expense['amount']
        for person in payments:
            if payments[person] < 0:
                for other_person in payments:
                    if payments[other_person] > 0:
                        amount = min(abs(payments[person]), payments[other_person])
                        payments[person] += amount
                        payments[other_person] -= amount
                        print(f"{other_person} pays ${amount:.2f} to {person}.")
                        if payments[person] == 0:
                            break
    print("-------------------------------------------------------------------------\n\n")

def main():
    while True:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Equalize Payments")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_expense()
        elif choice == 2:
            view_expense()
        elif choice == 3:
            equalize_payments()
        elif choice == 4:
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == '__main__':
    main()
