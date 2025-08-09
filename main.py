from pathlib import Path
import csv
from fastmcp import FastMCP, Context

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
EXPENSES_FILE = SCRIPT_DIR / "expenses.csv"

# Create the MCP server
mcp = FastMCP("Expenses Tracker")


@mcp.resource("resource://expenses")
async def get_expenses_data(ctx: Context):
    """Get raw expense data from CSV file"""
    try:
        with open(EXPENSES_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expenses_data = list(reader)

        # Format the data cleanly for the LLM
        csv_content = f"Expense data ({len(expenses_data)} entries):\n\n"
        for expense in expenses_data:
            csv_content += f"Date: {expense['date']}, Amount: ${expense['amount']}, Category: {expense['category']}, Description: {expense['description']}, Payment: {expense['payment_method']}\n"

        return csv_content

    except FileNotFoundError:
        return "Error: expenses.csv file not found"
    except Exception as e:
        return f"Error reading expenses.csv: {str(e)}"


@mcp.tool
async def add_expense(
    date: str, amount: float, category: str, description: str, payment_method: str
):
    """Add a new expense to the expenses.csv file"""
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

            # Write the new expense
            writer.writerow([date, amount, category, description, payment_method])

        return f"Successfully added expense: ${amount} for {description} on {date}"

    except Exception as e:
        return f"Error adding expense: {str(e)}"


@mcp.prompt
def create_expense_prompt(
    date: str, amount: float, category: str, description: str, payment_method: str
) -> str:
    """Generate a prompt to add a new expense using the add_expense tool."""
    return f"""Please add the following expense:
- Date: {date}
- Amount: ${amount}
- Category: {category}
- Description: {description}
- Payment Method: {payment_method}

Use the `add_expense` tool to record this transaction."""


if __name__ == "__main__":
    mcp.run()
