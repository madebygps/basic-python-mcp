from pathlib import Path
import csv
import logging
from datetime import datetime
from fastmcp import FastMCP
from enum import Enum


# Enum for payment methods
class PaymentMethod(Enum):
    AMEX = "amex"
    VISA = "visa"
    CASH = "cash"


# Security: Basic audit logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("ExpensesMCP")

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
EXPENSES_FILE = SCRIPT_DIR / "expenses.csv"

# Create the MCP server
mcp = FastMCP("Expenses Tracker")


@mcp.resource("resource://expenses")
async def get_expenses_data():
    """Get raw expense data from CSV file"""
    # Security: Audit log
    logger.info("Expenses data accessed")

    try:
        with open(EXPENSES_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expenses_data = list(reader)

        # Format the data cleanly for the LLM
        csv_content = f"Expense data ({len(expenses_data)} entries):\n\n"
        for expense in expenses_data:
            csv_content += (
            f"Date: {expense['date']}, "
            f"Amount: ${expense['amount']}, "
            f"Category: {expense['category']}, "
            f"Description: {expense['description']}, "
            f"Payment: {expense['payment_method']}\n"
            )

        return csv_content

    except FileNotFoundError:
        logger.error("Expenses file not found")
        return "Error: Expense data unavailable"
    except Exception as e:
        logger.error(f"Error reading expenses: {str(e)}")
        return "Error: Unable to retrieve expense data"


@mcp.tool
async def add_expense(
    date: str,
    amount: float,
    category: str,
    description: str,
    payment_method: PaymentMethod,
):
    """Add a new expense to the expenses.csv file.

    payment_method: The payment method used. Must be one of: card, cash.
    """
    # Input validation
    try:
        datetime.fromisoformat(date)
        if amount <= 0:
            return "Error: Amount must be positive"
    except ValueError as e:
        return f"Error: {str(e)}"

    # Audit log before action
    logger.info(f"Adding expense: ${amount} for {description}")

    try:
        # Check if the CSV file exists, if not create it with headers
        file_exists = EXPENSES_FILE.exists()

        with open(EXPENSES_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # If file doesn't exist, write headers first
            if not file_exists:
                writer.writerow(
                    ["date", "amount", "category", "description", "payment_method"]
                )

            # Write the new expense (use standardized payment method value)
            writer.writerow([date, amount, category, description, payment_method.value])

        return f"Successfully added expense: ${amount} for {description} on {date}"

    except Exception as e:
        # Security: Don't expose internal errors
        logger.error(f"Error adding expense: {str(e)}")
        return "Error: Unable to add expense"


@mcp.prompt
def create_expense_prompt(
    date: str, amount: float, category: str, description: str, payment_method: str
) -> str:
    """Generate a prompt to add a new expense using the add_expense tool."""

    logger.info(f"Expense prompt created for: {description}")

    return f"""Please add the following expense:
- Date: {date}
- Amount: ${amount}
- Category: {category}
- Description: {description}
- Payment Method: {payment_method}

Use the `add_expense` tool to record this transaction."""


if __name__ == "__main__":
    logger.info("MCP Expenses server starting")
    mcp.run()
