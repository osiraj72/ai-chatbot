from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

text = """
Artificial Intelligence Engineering Guide

AI Engineers build intelligent systems that solve real problems.
The most important skills for AI engineers are:
1. Python programming
2. Building LLM applications
3. Working with APIs
4. Deploying applications

The average salary for an AI engineer is between $100,000 and $200,000 per year.
Top companies hiring AI engineers include Google, Microsoft, and OpenAI.
Pakistan has a growing demand for AI engineers especially in Karachi and Lahore.
"""

pdf.multi_cell(0, 10, text)
pdf.output("test.pdf")
print("PDF created!")