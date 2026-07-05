"""
AI-Structured Employee Onboarding System
A Streamlit application that generates a complete onboarding package
(welcome email, 7-day plan, document checklist, IT access checklist,
FAQs, and training resources) based on employee name, role, and department.
"""

import streamlit as st

# ----------------------------------------------------------------------------
# Data: Role-based training resources
# ----------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------
# Data: Department-based IT access checklist
# ----------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------------
def generate_welcome_email(name, role, department):
    return f"""Subject: Welcome to the Team, {name}!

Dear {name},

Welcome aboard! We are thrilled to have you join us as a {role} in the
{department} department. Your skills and experience will be a great
addition to our team, and we are confident you will make a meaningful
impact here.

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


def generate_document_checklist():
    return [
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


def get_it_access_checklist(department):
    return DEPARTMENT_IT_ACCESS.get(department.strip().lower(), DEFAULT_IT_ACCESS)


def get_training_resources(role):
    return ROLE_TRAINING.get(role.strip().lower(), DEFAULT_TRAINING)


def generate_faqs():
    return [
        (
            "When will I receive my salary?",
            "Salary details, including pay cycle and disbursement dates, "
            "will be shared by the HR/Payroll team during your first week.",
        ),
        (
            "Who do I contact for IT issues?",
            "Reach out to the IT Helpdesk via the internal ticketing system "
            "or the designated support email/channel.",
        ),
        (
            "What is the dress code?",
            "Please refer to the employee handbook for department-specific "
            "dress code guidelines, or check with your manager.",
        ),
        (
            "How do I apply for leave?",
            "Leave requests can be submitted through the HR management "
            "system and require manager approval.",
        ),
        (
            "Who is my point of contact for onboarding questions?",
            "Your assigned HR onboarding buddy or your reporting manager "
            "will be your primary point of contact.",
        ),
        (
            "Is there a probation period?",
            "Probation period details, if applicable, are outlined in your "
            "offer letter/employment contract.",
        ),
    ]


# ----------------------------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="AI Onboarding System", page_icon="🧑‍💼", layout="centered")

    st.title("🧑‍💼 AI-Structured Employee Onboarding System")
    st.write(
        "Enter the new employee's details below to automatically generate a "
        "complete onboarding package."
    )

    with st.form("onboarding_form"):
        name = st.text_input("Employee Name")
        role = st.text_input("Role (e.g., Software Engineer, Data Analyst)")
        department = st.text_input("Department (e.g., Engineering, HR, Sales)")
        submitted = st.form_submit_button("Generate Onboarding Package")

    if submitted:
        if not name.strip() or not role.strip() or not department.strip():
            st.error("Please fill in all fields: Employee Name, Role, and Department.")
            return

        st.success(f"Onboarding package generated for {name}!")

        # 1. Welcome Email
        st.header("📧 Welcome Email")
        st.code(generate_welcome_email(name, role, department), language="text")

        # 2. 7-Day Onboarding Plan
        st.header("📅 7-Day Onboarding Plan")
        for day_title, tasks in generate_7day_plan(role, department):
            st.subheader(day_title)
            for task in tasks:
                st.markdown(f"- {task}")

        # 3. Required Documents Checklist
        st.header("📄 Required Documents Checklist")
        for doc in generate_document_checklist():
            st.checkbox(doc, key=f"doc_{doc}")

        # 4. IT Access Checklist (based on department)
        st.header("💻 IT Access Checklist")
        st.caption(f"Based on department: {department}")
        for item in get_it_access_checklist(department):
            st.checkbox(item, key=f"it_{item}")

        # 5. FAQs
        st.header("❓ FAQs for New Employees")
        for question, answer in generate_faqs():
            with st.expander(question):
                st.write(answer)

        # 6. Training Resources (based on role)
        st.header("🎓 Training Resources")
        st.caption(f"Based on role: {role}")
        for resource in get_training_resources(role):
            st.markdown(f"- {resource}")


if __name__ == "__main__":
    main()
