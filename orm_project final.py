# FINTRACK PRO – CLI FINANCE MANAGER

# add_category-> add expense category
# add_expense-> add new expense
# update_expense-> update expense
# delete_expense-> delete expense
# search_by_date-> search expenses by date
# category_analytics-> category wise total spending
# set_budget-> set monthly budget
# budget_alert-> check if budget exceeded


from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///fintrack.db")

# Base class
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


# Category Table
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # One category → many expenses
    expenses = relationship("Expense", back_populates="category")


# Expense Table
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    amount = Column(Float)
    date = Column(String)

    #link expenses to category
    category_id = Column(Integer, ForeignKey("categories.id"))

    # to access category from expense 
    category = relationship("Category", back_populates="expenses")


# Subscription Table
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float)
    next_date = Column(String)


# Budget Table
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True)
    month = Column(String)
    limit = Column(Float)


# Create all tables
Base.metadata.create_all(engine)


def add_category():
    name = input("Category name: ")
    session.add(Category(name=name))
    session.commit()
    print("Category added")


def add_expense():
    title = input("Expense title: ")
    amount = float(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ")
    category_id = int(input("Category ID: "))

    session.add(Expense(title=title, amount=amount, date=date, category_id=category_id))
    session.commit()
    print("Expense added")


def update_expense():
    eid = int(input("Expense ID: "))
    expense = session.query(Expense).filter(Expense.id == eid).first()

    if expense:
        expense.title = input("Updated title: ")
        expense.amount = float(input("Updated amount: "))
        expense.date = input("Updated date (YYYY-MM-DD): ")
        session.commit()
        print("Expense updated")
    else:
        print("Expense not found")


def delete_expense():
    eid = int(input("Expense ID: "))
    expense = session.query(Expense).filter(Expense.id == eid).first()

    if expense:
        session.delete(expense)
        session.commit()
        print("Expense deleted")
    else:
        print("Expense not found")


def search_by_date():
    date = input("Enter date (YYYY-MM-DD): ")
    expenses = session.query(Expense).filter(Expense.date == date).all()

    if expenses:
        for i in expenses:
            print(i.title, "→ ₹", e.amount)
    else:
        print("No expenses found")


def category_analytics():
    sql = text("""
    SELECT categories.name, SUM(expenses.amount)
    FROM categories
    JOIN expenses ON categories.id = expenses.category_id
    GROUP BY categories.name
    """)

    result = session.execute(sql)

    print("\nCategory Wise Expense Report")
    for row in result:
        print(row[0], "→", row[1])


def set_budget():
    month = input("Month (YYYY-MM): ")
    limit = float(input("Budget limit: "))

    session.add(Budget(month=month, limit=limit))
    session.commit()
    print("Monthly budget set")


def budget_alert():
    month = input("Month (YYYY-MM): ")

    total = session.execute(
        text("SELECT SUM(amount) FROM expenses WHERE date LIKE :m"),
        {"m": f"{month}%"}
    ).scalar() or 0

    budget = session.query(Budget).filter(Budget.month == month).first()

    if budget and total > budget.limit:
        print("⚠ Budget exceeded")
    else:
        print("Within budget")


while True:
    print("""
===== FINTRACK PRO =====
1. Add Category
2. Add Expense
3. Update Expense
4. Delete Expense
5. Search Expense by Date
6. Category Analytics
7. Set Monthly Budget
8. Budget Alert
9. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        add_category()
    elif choice == "2":
        add_expense()
    elif choice == "3":
        update_expense()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        search_by_date()
    elif choice == "6":
        category_analytics()
    elif choice == "7":
        set_budget()
    elif choice == "8":
        budget_alert()
    elif choice == "9":
        print("Exiting FinTrack Pro")
        break
    else:
        print("Invalid choice")
