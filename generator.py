# app/generator.py

import openai
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import uuid
import json

openai.api_key = os.getenv(\"OPENAI_API_KEY\")

def generate_thank_you_note(client_name, total_amount):
    prompt = (
        f\"Write a short, friendly thank-you note for a client named {client_name} "
        f"who made a purchase totaling ${total_amount}. Keep it warm and professional.\"
    )
    response = openai.ChatCompletion.create(
        model=\"gpt-4o\",
        messages=[
            {\"role\": \"system\", \"content\": \"You are a helpful assistant.\"},
            {\"role\": \"user\", \"content\": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_invoice(order_data, output_dir=\"invoices/\"):
    client_name = order_data[\"client_name\"]
    items = order_data[\"items\"]  # List of {description, quantity, unit_price}
    tax_rate = order_data.get(\"tax_rate\", 0.07)

    subtotal = sum(item[\"quantity\"] * item[\"unit_price\"] for item in items)
    tax = subtotal * tax_rate
    total = subtotal + tax

    # Get AI thank-you note
    thank_you_note = generate_thank_you_note(client_name, round(total, 2))

    # Create unique invoice ID
    invoice_id = str(uuid.uuid4())[:8]
    filename = f\"invoice_{invoice_id}.pdf\"
    file_path = os.path.join(output_dir, filename)

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    c.setFont(\"Helvetica-Bold\", 20)
    c.drawString(50, height - 50, \"INVOICE\")

    c.setFont(\"Helvetica\", 12)
    c.drawString(50, height - 80, f\"Invoice ID: {invoice_id}\")
    c.drawString(50, height - 100, f\"Date: {datetime.now().strftime('%Y-%m-%d')}\")
    c.drawString(50, height - 120, f\"Bill To: {client_name}\")

    # Table headers
    c.drawString(50, height - 160, \"Description\")
    c.drawString(300, height - 160, \"Quantity\")
    c.drawString(400, height - 160, \"Unit Price\")
    c.drawString(500, height - 160, \"Total\")

    y = height - 180
    for item in items:
        c.drawString(50, y, item[\"description\"])
        c.drawString(300, y, str(item[\"quantity\"]))
        c.drawString(400, y, f\"${item['unit_price']:.2f}\")
        line_total = item[\"quantity\"] * item[\"unit_price\"]
        c.drawString(500, y, f\"${line_total:.2f}\")
        y -= 20

    c.drawString(400, y - 10, \"Subtotal:\")
    c.drawString(500, y - 10, f\"${subtotal:.2f}\")

    c.drawString(400, y - 30, \"Tax:\")
    c.drawString(500, y - 30, f\"${tax:.2f}\")

    c.setFont(\"Helvetica-Bold\", 12)
    c.drawString(400, y - 50, \"Total:\")
    c.drawString(500, y - 50, f\"${total:.2f}\")

    # Thank you note
    c.setFont(\"Helvetica-Oblique\", 10)
    c.drawString(50, y - 80, f\"{thank_you_note}\")

    c.save()
    return {
        \"invoice_id\": invoice_id,
        \"file_path\": file_path,
        \"total\": total,
        \"thank_you_note\": thank_you_note
    }

if __name__ == \"__main__\":
    # Example order data
    order = {
        \"client_name\": \"Acme Corp.\",
        \"items\": [
            {\"description\": \"Web Design\", \"quantity\": 1, \"unit_price\": 1200},
            {\"description\": \"Hosting (6 months)\", \"quantity\": 1, \"unit_price\": 300}
        ],
        \"tax_rate\": 0.07
    }
    result = generate_invoice(order)
    print(\"Generated Invoice:\", result)
