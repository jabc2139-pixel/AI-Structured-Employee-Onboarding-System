# AI-Structured-Employee-Onboarding-System

A Streamlit application that generates a complete, structured onboarding
package for a new employee, downloadable as a PDF, with optional welcome
email delivery via SMTP.

## Features

- Employee Name, Employee Email, Manager Name, Joining Date inputs
- Role and Department dropdown selectors
- Professional welcome email generation
- Actual email sending via SMTP (Gmail, Outlook, SendGrid SMTP relay, etc.)
- Structured 7-day onboarding plan
- Required documents checklist
- IT access checklist based on department
- Role-based training resources
- FAQs for new employees
- Full onboarding package exported as a downloadable PDF
- Input validation with clear success/error messages

## Requirements

- Python 3.8+
- streamlit
- reportlab

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
   pip install streamlit reportlab
   ```

## Run the App

```bash
streamlit run app.py
```

The app opens automatically in your default browser (typically at
`http://localhost:8501`).

## Usage

1. Fill in **Employee Name**, **Employee Email**, **Manager Name**,
   **Joining Date**, and select **Role** and **Department** from the
   dropdowns.
2. (Optional) Check **Send welcome email now via SMTP** and provide:
   - SMTP Host (e.g., `smtp.gmail.com`)
   - SMTP Port (e.g., `587`)
   - Sender Email (SMTP username)
   - Sender App Password (use an app-specific password, not your main
     account password, for providers like Gmail)
3. Click **Generate Onboarding Package**.
4. Review the welcome email, 7-day plan, document checklist, IT access
   checklist, training resources, and FAQs.
5. Click **Download Onboarding Package (PDF)** to save the full package.

## Notes on Email Sending

- The app uses Python's built-in `smtplib` over TLS — no third-party API
  keys required, just standard SMTP credentials.
- Credentials entered in the form are used only for that session and are
  never written to disk.
- For Gmail, enable 2-Step Verification and generate an
  [App Password](https://myaccount.google.com/apppasswords) to use as the
  Sender App Password.

## Notes

- The app runs entirely offline aside from the optional SMTP email step.
- Role and department matching is case-insensitive; unrecognized custom
  values fall back to sensible default checklists/resources.
