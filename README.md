# Basic Python Expense Tracker MCP

A simple expense tracking application built as a **Model Context Protocol (MCP)** server using Python and FastMCP. This project demonstrates the most basic example on how to create an MCP server tool.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard that enables AI assistants to securely access external data sources and tools. This expense tracker serves as an MCP server that provides:

- **Tools**: Functions that AI assistants can call to perform actions
- **Resources**: Data sources that AI assistants can read
- **Prompts**: Templates for generating structured requests

## Prerequisites

- **Python 3.11+** (required by FastMCP)
- **uv** (recommended) or **pip** for package management

## Installation

1. **Install uv** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup the project:**

   ```bash
   git clone https://github.com/madebygps/basic-python-mcp.git
   cd basic-python-mcp
   uv sync
   ```

## Usage

### Running the MCP Server

Start the server using one of these methods:

```bash
uv run python main.py
```

The server will start and display connection information for MCP clients.

### Connecting to the Server

This MCP server can be used with any MCP-compatible client, such as:

- **Claude Desktop** (with MCP configuration)
- **VS Code**
- **MCP Client Tools**
- **Custom MCP applications**

#### VS Code Example

Add this configuration to your `.vscode/mcp.json` file to connect to the MCP server:

```json
{
   "servers": {
      "expense-tracker-mcp": {
         "type": "stdio",
         "command": "uv",
         "args": [
            "run",
            "main.py"
         ],
      }
   },
   "inputs": []
}
```

### Available MCP Components

#### 🛠️ Tools

**`add_expense`** - Add a new expense record

- `date` (string): Date in YYYY-MM-DD format
- `amount` (float): Expense amount
- `category` (string): Expense category (e.g., "food", "transport")
- `description` (string): Expense description
- `payment_method` (string): Payment method used

#### 📊 Resources

**`resource://expenses`** - Access all expense data

- Returns formatted expense data from the CSV file
- Includes total count and detailed expense information

#### 🤖 Prompts

**`create_expense_prompt`** - Generate structured expense creation prompts

- Creates natural language prompts for AI assistants
- Helps format expense data for the `add_expense` tool

### Example Usage with an AI Assistant

```text
"I spent $15.50 on lunch today at the cafe, paid with my credit card"
```

The AI assistant can use the MCP tools to:

1. Parse the natural language input
2. Call `add_expense` with the structured data
3. Confirm the expense was recorded
