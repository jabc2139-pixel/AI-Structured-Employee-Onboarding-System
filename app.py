"""
AI-Structured Employee Onboarding System
Streamlit application that generates a complete onboarding package
(welcome email, 7-day plan, document checklist, IT access checklist,
FAQs, role-based training resources) and exports it as a PDF.
Optionally sends the welcome email via SMTP.
"""

import io
import re
import smtplib
import ssl
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    Table,
    TableStyle,
    PageBreak,
)

# ----------------------------------------------------------------------------
# Configuration data
# ----------------------------------------------------------------------------
ROLES = [
    "Software Engineer",
    "Data Analyst",
    "Product Manager",
    "HR Specialist",
    "Sales Executive",
    "Marketing Specialist",
    "Other",
]

DEPARTMENTS = [
    "Engineering",
    "Human Resources",
    "Sales",
    "Marketing",
    "Finance",
    "IT",
    "Other",
]

ROLE_TRAINING = {
    "software engineer": [
        "Internal Git & code review guidelines",
        "System architecture walkthrough (Confluence/Wiki)",
        "Coding standards and style guide",
        "CI/CD pipeline overview",
        "Access to sandbox/dev environment",
    ],
    "data analyst": [
        "Data warehouse & schema documentation",
        "BI tool training (Power BI / Tableau / Looker)",
        "SQL style guide and query best practices",
        "Data governance and privacy policy",
    ],
    "product manager": [
        "Product roadmap and vision deck",
        "Agile/Scrum process overview",
        "Stakeholder map and communication channels",
        "Customer feedback and analytics tools",
    ],
    "hr specialist": [
        "HRIS system training",
        "Employment law and compliance basics",
        "Company policies and employee handbook",
        "Conflict resolution and interview training",
    ],
    "sales executive": [
        "CRM tool training (Salesforce/HubSpot)",
        "Sales playbook and pitch deck",
        "Pricing and product catalog",
        "Negotiation and objection-handling workshop",
    ],
    "marketing specialist": [
        "Brand guidelines and tone of voice",
        "Marketing automation tool training",
        "Content calendar and campaign workflow",
        "Analytics and reporting dashboards",
    ],
}

DEFAULT_TRAINING = [
    "Company orientation e-learning module",
    "Role-specific shadowing with a team mentor",
    "Internal knowledge base and documentation portal",
    "Tools and software relevant to the role (to be confirmed with manager)",
]

DEPARTMENT_IT_ACCESS = {
    "engineering": [
        "Company email & calendar",
        "Git repository access (GitHub/GitLab)",
        "Cloud platform access (AWS/Azure/GCP)",
        "IDE licenses (VS Code, JetBrains, etc.)",
        "CI/CD and deployment tools",
        "VPN and remote access setup",
    ],
    "human resources": [
        "Company email & calendar",
        "HRIS / HR management system",
        "Payroll system access",
        "Document management system",
        "Employee self-service portal",
    ],
    "sales": [
        "Company email & calendar",
        "CRM system (Salesforce/HubSpot)",
        "Video conferencing tools",
        "Sales enablement platform",
        "VPN for remote client access",
    ],
    "marketing": [
        "Company email & calendar",
        "Marketing automation platform",
        "Social media management tools",
        "Design software (Adobe/Canva)",
        "Analytics dashboards (Google Analytics, etc.)",
    ],
    "finance": [
        "Company email & calendar",
        "Accounting/ERP system access",
        "Expense management tool",
        "Financial reporting dashboards",
        "Restricted-access approval for sensitive data",
    ],
    "it": [
        "Company email & calendar",
        "Admin/root access to internal systems",
        "Ticketing system (Jira/ServiceNow)",
        "Network monitoring tools",
        "VPN and security certificates",
    ],
}

DEFAULT_IT_ACCESS = [
    "Company email & calendar",
    "Shared drive / document management system",
    "Internal communication tool (Slack/Teams)",
    "VPN access (if remote)",
]

REQUIRED_DOCUMENTS = [
    "Signed offer letter / employment contract",
    "Government-issued ID proof",
    "Educational certificates and transcripts",
    "Previous employment relieving/experience letters",
    "Bank account details for payroll",
    "Tax identification documents",
    "Emergency contact information form",
    "Signed company policy acknowledgment forms",
    "Passport-size photographs",
    "Non-disclosure agreement (NDA), if applicable",
]

FAQS = [
    (
        "When will I receive my salary?",
        "Salary details, including pay cycle and disbursement dates, will be "
        "shared by the HR/Payroll team during your first week.",
    ),
    (
        "Who do I contact for IT issues?",
        "Reach out to the IT Helpdesk via the internal ticketing system or the "
        "designated support email/channel.",
    ),
    (
        "What is the dress code?",
        "Please refer to the employee handbook for department-specific dress "
        "code guidelines, or check with your manager.",
    ),
    (
        "How do I apply for leave?",
        "Leave requests can be submitted through the HR management system and "
        "require manager approval.",
    ),
    (
        "Who is my point of contact for onboarding questions?",
        "Your assigned HR onboarding buddy or your reporting manager will be "
        "your primary point of contact.",
    ),
    (
        "Is there a probation period?",
        "Probation period details, if applicable, are outlined in your offer "
        "letter/employment contract.",
    ),
]

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ----------------------------------------------------------------------------
# Content generators
# ----------------------------------------------------------------------------
def generate_welcome_email(name, role, department, manager_name, joining_date):
    return f"""Subject: Welcome to the Team, {name}!

Dear {name},

Welcome aboard! We are thrilled to have you join us as a {role} in the
{department} department, starting on {joining_date.strftime('%B %d, %Y')}.
Your reporting manager will be {manager_name}, who will support you
throughout your onboarding journey.

Over the next few days, you will receive a structured onboarding plan
to help you settle in, meet your colleagues, and get up to speed with
your responsibilities. Please don't hesitate to reach out to your
manager or the HR team if you have any questions along the way.

Once again, welcome to the company. We look forward to seeing you
thrive in your new role!

Best regards,
Human Resources Team
"""


def generate_7day_plan(role, department):
    return [
        (
            "Day 1 - Orientation",
            [
                "Attend company welcome/orientation session",
                "Receive laptop, ID badge, and access credentials",
                "Meet manager and immediate team members",
                "Review company policies and employee handbook",
            ],
        ),
        (
            "Day 2 - Department Introduction",
            [
                f"Overview of the {department} department's goals and structure",
                "Introduction to key stakeholders and cross-functional partners",
                "Walkthrough of department-specific tools and systems",
            ],
        ),
        (
            "Day 3 - Role-Specific Training",
            [
                f"Deep dive into responsibilities of a {role}",
                "Shadow a team member for hands-on learning",
                "Review ongoing projects relevant to the role",
            ],
        ),
        (
            "Day 4 - Systems & Tools",
            [
                "Complete IT systems setup and access verification",
                "Hands-on practice with core tools for the role",
                "Set up communication and collaboration channels",
            ],
        ),
        (
            "Day 5 - Process Deep Dive",
            [
                "Review workflows, SOPs, and reporting structures",
                "Attend a working session or team stand-up",
                "Clarify expectations and short-term goals with manager",
            ],
        ),
        (
            "Day 6 - Integration",
            [
                "Participate in a team activity or 1:1 coffee chats",
                "Begin contributing to a small initial task or project",
                "Check in with HR on any outstanding onboarding items",
            ],
        ),
        (
            "Day 7 - Review & Feedback",
            [
                "Review progress with manager",
                "Provide feedback on the onboarding experience",
                "Set goals for the next 30/60/90 days",
            ],
        ),
    ]


def get_it_access_checklist(department):
    return DEPARTMENT_IT_ACCESS.get(department.strip().lower(), DEFAULT_IT_ACCESS)


def get_training_resources(role):
    return ROLE_TRAINING.get(role.strip().lower(), DEFAULT_TRAINING)


# ----------------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------------
def validate_inputs(name, email, manager_name, role, department):
    errors = []
    if not name.strip():
        errors.append("Employee Name is required.")
    if not email.strip():
        errors.append("Employee Email is required.")
    elif not EMAIL_REGEX.match(email.strip()):
        errors.append("Employee Email format is invalid.")
    if not manager_name.strip():
        errors.append("Manager Name is required.")
    if not role or role.strip() == "":
        errors.append("Role must be selected.")
    if not department or department.strip() == "":
        errors.append("Department must be selected.")
    return errors


# ----------------------------------------------------------------------------
# Email sending
# ----------------------------------------------------------------------------
def send_welcome_email(to_email, subject, body, smtp_host, smtp_port, smtp_user, smtp_password, use_tls=True):
    """
    Sends the welcome email using a supported SMTP-based email service
    (e.g., Gmail SMTP, Outlook SMTP, SendGrid SMTP relay).
    Returns (success: bool, message: str).
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            if use_tls:
                server.starttls(context=context)
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())

        return True, f"Welcome email successfully sent to {to_email}."
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP authentication failed. Check the sender email/password (or app password)."
    except smtplib.SMTPException as exc:
        return False, f"SMTP error occurred while sending email: {exc}"
    except Exception as exc:  # noqa: BLE001
        return False, f"Failed to send email: {exc}"


# ----------------------------------------------------------------------------
# PDF generation
# ----------------------------------------------------------------------------
def build_onboarding_pdf(name, email, manager_name, role, department, joining_date):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontSize=20, spaceAfter=6
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor("#1f3864"),
    )
    sub_heading_style = ParagraphStyle(
        "SubHeadingStyle",
        parent=styles["Heading3"],
        fontSize=11.5,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.HexColor("#2e5395"),
    )
    body_style = styles["Normal"]
    faq_q_style = ParagraphStyle(
        "FaqQ", parent=styles["Normal"], fontSize=10.5, spaceBefore=6, fontName="Helvetica-Bold"
    )

    story = []

    # Cover / summary
    story.append(Paragraph("Employee Onboarding Package", title_style))
    story.append(Spacer(1, 6))

    summary_data = [
        ["Employee Name", name],
        ["Employee Email", email],
        ["Role", role],
        ["Department", department],
        ["Manager", manager_name],
        ["Joining Date", joining_date.strftime("%B %d, %Y")],
    ]
    summary_table = Table(summary_data, colWidths=[1.8 * inch, 4.2 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#dbe5f1")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1f3864")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b0b8c4")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # Welcome email
    story.append(Paragraph("Welcome Email", heading_style))
    email_text = generate_welcome_email(name, role, department, manager_name, joining_date)
    for line in email_text.strip().split("\n"):
        story.append(Paragraph(line if line.strip() else "&nbsp;", body_style))
    story.append(PageBreak())

    # 7-day plan
    story.append(Paragraph("7-Day Onboarding Plan", heading_style))
    for day_title, tasks in generate_7day_plan(role, department):
        story.append(Paragraph(day_title, sub_heading_style))
        story.append(
            ListFlowable(
                [ListItem(Paragraph(t, body_style)) for t in tasks],
                bulletType="bullet",
                leftIndent=16,
            )
        )

    # Required documents
    story.append(Paragraph("Required Documents Checklist", heading_style))
    story.append(
        ListFlowable(
            [ListItem(Paragraph(d, body_style)) for d in REQUIRED_DOCUMENTS],
            bulletType="bullet",
            leftIndent=16,
        )
    )

    # IT access checklist
    story.append(Paragraph("IT Access Checklist", heading_style))
    story.append(Paragraph(f"Based on department: {department}", body_style))
    story.append(
        ListFlowable(
            [ListItem(Paragraph(i, body_style)) for i in get_it_access_checklist(department)],
            bulletType="bullet",
            leftIndent=16,
        )
    )

    # Training resources
    story.append(Paragraph("Training Resources", heading_style))
    story.append(Paragraph(f"Based on role: {role}", body_style))
    story.append(
        ListFlowable(
            [ListItem(Paragraph(r, body_style)) for r in get_training_resources(role)],
            bulletType="bullet",
            leftIndent=16,
        )
    )

    # FAQs
    story.append(Paragraph("FAQs for New Employees", heading_style))
    for q, a in FAQS:
        story.append(Paragraph(q, faq_q_style))
        story.append(Paragraph(a, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ----------------------------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="AI Onboarding System", page_icon="🧑‍💼", layout="centered")

    st.title("🧑‍💼 AI-Structured Employee Onboarding System")
    st.write(
        "Fill in the new employee's details to generate a complete onboarding "
        "package, download it as a PDF, and optionally email the welcome note."
    )

    if "package_ready" not in st.session_state:
        st.session_state.package_ready = False

    with st.form("onboarding_form"):
        st.subheader("Employee Details")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Employee Name *")
            manager_name = st.text_input("Manager Name *")
            role = st.selectbox("Role *", ROLES)
        with col2:
            email = st.text_input("Employee Email *")
            joining_date = st.date_input("Joining Date *", value=date.today())
            department = st.selectbox("Department *", DEPARTMENTS)

        st.subheader("Email Delivery (optional)")
        send_email = st.checkbox("Send welcome email now via SMTP")

        smtp_host = smtp_port = smtp_user = smtp_password = None
        if send_email:
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                smtp_host = st.text_input("SMTP Host", value="smtp.gmail.com")
                smtp_user = st.text_input("Sender Email (SMTP username)")
            with e_col2:
                smtp_port = st.number_input("SMTP Port", value=587, step=1)
                smtp_password = st.text_input("Sender App Password", type="password")
            st.caption(
                "Use an SMTP-supported provider (e.g., Gmail SMTP with an App "
                "Password, Outlook SMTP, or a SendGrid SMTP relay). Credentials "
                "are used only for this session and are not stored."
            )

        submitted = st.form_submit_button("Generate Onboarding Package")

    if submitted:
        errors = validate_inputs(name, email, manager_name, role, department)
        if send_email:
            if not smtp_host or not smtp_user or not smtp_password:
                errors.append("SMTP Host, Sender Email, and Sender App Password are required to send email.")

        if errors:
            for err in errors:
                st.error(err)
            st.session_state.package_ready = False
        else:
            st.session_state.update(
                name=name,
                email=email,
                manager_name=manager_name,
                role=role,
                department=department,
                joining_date=joining_date,
                package_ready=True,
            )
            st.success(f"Onboarding package generated for {name}!")

            if send_email:
                welcome_text = generate_welcome_email(name, role, department, manager_name, joining_date)
                subject = welcome_text.split("\n", 1)[0].replace("Subject: ", "")
                body = welcome_text.split("\n", 1)[1].strip()
                ok, message = send_welcome_email(
                    email, subject, body, smtp_host, int(smtp_port), smtp_user, smtp_password
                )
                if ok:
                    st.success(message)
                else:
                    st.error(message)

    if st.session_state.package_ready:
        name = st.session_state.name
        email = st.session_state.email
        manager_name = st.session_state.manager_name
        role = st.session_state.role
        department = st.session_state.department
        joining_date = st.session_state.joining_date

        st.divider()

        pdf_buffer = build_onboarding_pdf(name, email, manager_name, role, department, joining_date)
        st.download_button(
            label="⬇️ Download Onboarding Package (PDF)",
            data=pdf_buffer,
            file_name=f"{name.replace(' ', '_')}_onboarding_package.pdf",
            mime="application/pdf",
        )

        st.header("📧 Welcome Email")
        st.code(generate_welcome_email(name, role, department, manager_name, joining_date), language="text")

        st.header("📅 7-Day Onboarding Plan")
        for day_title, tasks in generate_7day_plan(role, department):
            st.subheader(day_title)
            for task in tasks:
                st.markdown(f"- {task}")

        st.header("📄 Required Documents Checklist")
        for doc_item in REQUIRED_DOCUMENTS:
            st.checkbox(doc_item, key=f"doc_{doc_item}")

        st.header("💻 IT Access Checklist")
        st.caption(f"Based on department: {department}")
        for item in get_it_access_checklist(department):
            st.checkbox(item, key=f"it_{item}")

        st.header("🎓 Training Resources")
        st.caption(f"Based on role: {role}")
        for resource in get_training_resources(role):
            st.markdown(f"- {resource}")

        st.header("❓ FAQs for New Employees")
        for question, answer in FAQS:
            with st.expander(question):
                st.write(answer)


if __name__ == "__main__":
    main()
