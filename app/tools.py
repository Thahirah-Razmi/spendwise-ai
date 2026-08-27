from app.database import get_connection


def add_expense(
    amount: float,
    category: str,
    description: str
) -> str:
    """
    Add a new expense to the user's expense tracker.

    Args:
        amount: The amount of money spent.
        category: The expense category such as food, transport, shopping, or bills.
        description: A short description of the expense.

    Returns:
        A confirmation message containing the new expense ID.
    """

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO expenses (amount, category, description)
        VALUES (?, ?, ?)
        """,
        (amount, category, description)
    )

    connection.commit()

    expense_id = cursor.lastrowid

    connection.close()

    return (
        f"Expense #{expense_id} added successfully: "
        f"{amount:.2f} for {category} ({description})."
    )


def list_expenses() -> str:
    """
    List the user's recent expenses.

    Returns:
        A formatted list of recent expenses.
    """

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, amount, category, description, created_at
        FROM expenses
        ORDER BY created_at DESC
        LIMIT 20
        """
    ).fetchall()

    connection.close()

    if not rows:
        return "The user has no expenses."

    result = []

    for row in rows:
        result.append(
            f"#{row['id']} - "
            f"{row['amount']:.2f} - "
            f"{row['category']} - "
            f"{row['description']}"
        )

    return "\n".join(result)


def get_total_expenses() -> str:
    """
    Calculate the total amount of all user expenses.

    Returns:
        The total amount spent.
    """

    connection = get_connection()

    row = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses"
    ).fetchone()

    connection.close()

    return f"Total expenses: {row['total']:.2f}"


def get_expenses_by_category(category: str) -> str:
    """
    Calculate spending for a specific expense category.

    Supports broad categories such as "food" by including
    related expense categories.
    """

    connection = get_connection()

    category = category.strip().lower()

    category_groups = {
        "food": [
            "food",
            "groceries",
            "grocery",
            "lunch",
            "dinner",
            "breakfast",
            "snacks",
            "restaurant",
            "takeaway",
            "coffee",
        ],
        "transport": [
            "transport",
            "transportation",
            "fuel",
            "taxi",
            "uber",
            "bus",
            "train",
        ],
    }

    if category in category_groups:
        categories = category_groups[category]

        placeholders = ",".join("?" for _ in categories)

        row = connection.execute(
            f"""
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE LOWER(category) IN ({placeholders})
            """,
            categories
        ).fetchone()

    else:
        row = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE LOWER(category) = LOWER(?)
            """,
            (category,)
        ).fetchone()

    connection.close()

    return f"Total spent on {category}: {row['total']:.2f}"