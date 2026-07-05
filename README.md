# AI-Structured-Employee-Onboarding-System

A Streamlit application that generates a complete, structured onboarding
package for a new employee based on their **Name**, **Role**, and
**Department**.

## Features

Given an employee's name, role, and department, the app generates:

1. A professional welcome email
2. A structured 7-day onboarding plan
3. A checklist of required documents
4. An IT access checklist based on department
5. FAQs for new employees
6. Training resources based on role

## Requirements

- Python 3.8+
- Streamlit

## Setup

1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd AI-Structured-Employee-Onboarding-System
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install streamlit
   ```

## Run the App

```bash
streamlit run app.py
```

The app will open automatically in your default browser (typically at
`http://localhost:8501`).

## Usage

1. Enter the employee's **Name**, **Role**, and **Department** in the form.
2. Click **Generate Onboarding Package**.
3. Review the generated welcome email, onboarding plan, document checklist,
   IT access checklist, FAQs, and training resources.

## Notes

- The app runs entirely offline — no external APIs are used.
- Role and department matching is case-insensitive; unrecognized roles or
  departments fall back to sensible default checklists/resources.
