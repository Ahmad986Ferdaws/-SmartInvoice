# SmartInvoice

SmartInvoice is an AI-powered invoicing system that automates invoice creation, PDF generation, and custom client messages.

## Features
- Upload CSV/JSON orders
- Auto-generate PDF invoices
- AI-powered thank-you notes
- SQLite to store invoice status

## Setup
1. Add `.env` with your OpenAI API key.
2. Install: `pip install -r requirements.txt`
3. Run: `uvicorn app.main:app --reload`
