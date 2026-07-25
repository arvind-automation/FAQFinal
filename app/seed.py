"""Seed portal content from the original FAQ data."""

from app import db
from app.models import Benefit, FAQ, FAQCategory, JourneyStage, Spoc

TOP_FAQS = [
    ("What is GCC?", "The Global Capability Centre (GCC) is a value-led capability platform designed to strengthen select corporate and enabling activities across Arvind's businesses. It is a centralized hub leveraging advanced technologies, standardized processes, and deeper functional expertise to support the Group's growth journey."),
    ("Why is GCC being created?", "As the Arvind Group scales, our enabling functions need to operate with greater predictability and depth. The GCC allows business leaders to dedicate more time to what truly matters — customers, markets, and growth — while reducing time spent on coordination, reconciliations, and operational follow-ups."),
    ("Is this about reducing headcount?", "No. This is not a headcount reduction initiative. The GCC is being set up to strengthen capabilities, improve efficiency, and enable greater scalability through better processes, technology, and functional depth."),
    ("Will my role change?", "The immediate priority is business continuity while employees continue to deliver in their area of specialization. As the GCC evolves, technology and best practices may reshape certain roles — creating more specialized, value-added opportunities for growth."),
    ("Will my reporting manager change?", "Reporting structures may evolve as part of the GCC design. Details specific to each role will be shared through one-on-one interactions and workshops during the transition. Employees may connect with the GCC HR SPOC for any questions."),
    ("Will I need to relocate?", "The Arvind GCC will operate from Ahmedabad. However, moving to the GCC does not automatically mean physical relocation. In some cases, employees may transition to the GCC while continuing from their current work location, depending on business and operational requirements. If relocation is required, it will be discussed individually with adequate notice and appropriate support."),
    ("What happens if I do not want to relocate?", "The transition is driven by how roles and work are structured, not purely by personal choice. Arvind is committed to handling the process with openness, care, and clear communication. No one will be moved without a detailed conversation, a transparent process, and enough time to prepare. Employees with specific concerns should connect with the GCC HR SPOC."),
    ("Will my salary change?", "Salary will not be impacted by the transition. As part of moving to the GCC, employees will transition to the GCC benefits framework, which is designed to provide an enhanced employee experience."),
    ("Will my benefits change?", "Employees will transition to the GCC benefits framework, designed to provide an enhanced employee experience. Details of applicable benefits will be shared separately."),
    ("Will working hours change?", "Yes. Employees will move to a 5-day work week (Monday to Friday). Standard working hours will be 9:30 AM to 6:30 PM, with flexibility to start up to 60 minutes later while completing the required 9-hour workday."),
    ("Will my performance rating change?", "No. The performance rating for the previous cycle has already been concluded and will remain unaffected. For the ongoing cycle, performance will be evaluated based on contributions throughout the year — both prior to joining the GCC and within the GCC — to ensure a fair and comprehensive assessment."),
    ("Will I receive a new appointment letter?", "Yes. Since the entity is changing, a new appointment letter will be issued. Service continuity and gratuity will be protected from the Group Date of Joining."),
    ("When will I receive system access?", "Employees shall receive new credentials and system access on 1 September 2026. In the initial phase, core ERP and current systems will remain unchanged."),
]

CATEGORIES = [
    {
        "slug": "understanding-gcc",
        "title": "Understanding GCC",
        "description": "The purpose, scope, and vision of the Arvind Global Capability Centre.",
        "faqs": [
            ("What is the Global Capability Centre (GCC)?", "The GCC is a value-led capability platform designed to strengthen select corporate and enabling activities that cut across Arvind's businesses. It is a centralized hub that will leverage advanced technologies, standardized processes, and deeper functional expertise to support the Group's growth journey."),
            ("Why are we setting up the GCC?", "As the Arvind Group scales, our enabling functions need to operate with greater predictability and depth. The GCC allows business leaders to dedicate more time to what truly matters — customers, markets, and growth — while reducing time spent on coordination, reconciliations, and operational follow-ups."),
            ("What specific functions and capabilities will the GCC handle?", "To start with, the Arvind GCC will cover functions such as HR, Finance, Procurement, and IT."),
            ("Is this about reducing headcount?", "No. This is not a headcount reduction initiative. The GCC is being set up to strengthen capabilities, improve efficiency, and enable greater scalability through better processes, technology, and functional depth. The intent is to build an operating model that can support business growth and evolving needs more effectively."),
            ("Is the GCC simply a back office?", "No. The GCC is not a transaction-only centre. It is envisioned as a capability centre and transformation platform. Over time, it will drive process excellence, analytics, automation, and new ways of working across the Arvind Group."),
            ("Does this change how our businesses are run?", "No. Ownership and decision-making remain with the businesses, exactly as they are today. The GCC strengthens execution behind the businesses — reliably and at scale."),
        ],
    },
    {
        "slug": "role-reporting",
        "title": "Your Role & Reporting",
        "description": "Clarity on role continuity, reporting structures, and day-to-day impact.",
        "faqs": [
            ("What happens to my current role?", "The immediate priority is to ensure business continuity while employees continue to deliver in their area of specialization. As the GCC evolves, technology, automation, and best practices may reshape certain roles. This evolution is intended to create more specialized, value-added roles and expand opportunities for learning, growth, and enterprise-wide impact."),
            ("Will my reporting structure change?", "Reporting structures may evolve as part of the GCC design. Details specific to each role will be shared through one-on-one interactions and workshops during the transition. Employees may connect with the GCC HR SPOC for any questions."),
            ("How does the GCC impact me?", "Work will continue as-is in the initial phase. As the GCC starts introducing standardized processes across entities, stronger analytics, automation of routine activities, and deeper specialization, employees will have more space to focus on higher-value work."),
        ],
    },
    {
        "slug": "working-model",
        "title": "Working Model & Relocation",
        "description": "Location, work-week structure, and relocation considerations.",
        "faqs": [
            ("Will I need to relocate?", "The Arvind GCC will operate from Ahmedabad. However, moving to the GCC does not automatically mean physical relocation. This applies to both Ahmedabad-based and non-Ahmedabad teams. In some cases, employees may transition to the GCC as part of the new operating model while continuing from their current work location, depending on business and operational requirements. If relocation is required, it will be discussed individually, with adequate notice and appropriate support."),
            ("What if I prefer not to move to the GCC?", "The transition is driven by how roles and work are structured, and not purely by personal choice. Arvind is committed to handling the process with openness, care, and clear communication. No one will be moved without a detailed conversation, a transparent process, and enough time to prepare. Employees with specific concerns should connect with the GCC HR SPOC."),
            ("Will working hours change?", "Yes. As part of the transition to Arvind GCC, employees will move to a 5-day work week from Monday to Friday. Standard working hours will be 9:30 AM to 6:30 PM, with flexibility to start up to 60 minutes later while completing the required 9-hour workday. This change is designed to provide greater flexibility and support better work-life balance while ensuring business needs continue to be met."),
        ],
    },
    {
        "slug": "career-growth",
        "title": "Career Growth",
        "description": "New pathways, exposure, and long-term development opportunities.",
        "faqs": [
            ("Will my role evolve over time?", "Not immediately. As the GCC matures and moves from stabilization into transformation, roles may be enhanced. Any such changes will be communicated clearly and well in advance."),
            ("What new opportunities does the GCC open up?", "The GCC can provide broader exposure across businesses, hands-on experience with automation, analytics, and AI-led workflows, cross-functional collaboration, and over time, the possibility to move between the GCC and retained organization as part of structured career progression."),
        ],
    },
    {
        "slug": "performance-kras",
        "title": "Performance & KRAs",
        "description": "How ratings, goals, and variable pay will be handled through the transition.",
        "faqs": [
            ("Will this transition impact my current performance rating?", "No. The performance rating for the previous cycle has already been concluded and will remain unaffected by the transition to the GCC. For the ongoing performance cycle, performance will be evaluated based on contributions throughout the year, including both work prior to joining the GCC and contributions within the GCC, to ensure a fair and comprehensive assessment."),
            ("Will my goals or KRAs change?", "As the transition to GCC progresses, goals and KRAs will be aligned with GCC priorities and ways of working. Some existing goals may continue, while others may be updated to reflect new responsibilities, standardized processes, technology enablement, and enterprise-wide objectives. Managers will discuss these changes and ensure expectations are clear."),
            ("How will variable pay be handled during the transition year?", "Variable pay for the transition year will be calculated on a pro-rata basis, based on the period of service in the respective organization and business unit during the performance year. Applicable performance outcomes and variable pay plans of each organization will be considered for the corresponding period of service."),
        ],
    },
    {
        "slug": "comp-benefits",
        "title": "Compensation & Benefits",
        "description": "Salary, appointment letter, PF, NPS, insurance and other continuity details.",
        "faqs": [
            ("Will my salary or benefits change?", "Salary will not be impacted by the transition. As part of moving to the GCC, employees will transition to the GCC benefits framework, which is designed to provide an enhanced employee experience. Details of applicable benefits will be shared separately."),
            ("Will I receive a new appointment letter?", "Yes. Since the entity is changing, a new appointment letter will be issued."),
            ("Will my gratuity and service continuity be protected?", "Yes. Service continuity and gratuity will be protected from the Group Date of Joining."),
            ("What happens to my PF and NPS?", "PF and NPS are expected to continue as per existing terms. For details relevant to individual cases, employees should reach out to the GCC HR SPOC."),
            ("What about existing loans, advances, or car lease?", "These are expected to continue as per existing terms. For confirmation on specific cases, employees should connect with the GCC HR SPOC."),
            ("Will my Mediclaim and insurance continue?", "Coverage is expected to continue as per existing terms. For policy-specific details, employees should connect with the GCC HR SPOC."),
        ],
    },
    {
        "slug": "relocation-support",
        "title": "Relocation Support",
        "description": "Support available for employees relocating to Ahmedabad.",
        "faqs": [
            ("What relocation support will be available?", "For employees relocating to Ahmedabad, the GCC offers comprehensive relocation support to ensure a smooth transition. Support may include: temporary accommodation up to 15 days at the joining location; joining travel reimbursement for employee and family as per grade-based domestic travel eligibility; household goods transportation reimbursement based on distance caps; vehicle transportation support for eligible grades; brokerage reimbursement of one month's rent subject to documents; house deposit support as an interest-free advance recovered over 10 monthly instalments; local conveyance support for a limited period based on grade eligibility; and either one pre-joining visit of up to 3 days or one post-joining relocation leave of 3 days (both cannot be availed together). All joining-related expense claims must be submitted within one year from the date of joining."),
            ("What should I do to prepare before transitioning?", "A clear checklist covering pending reimbursements, tax declarations, leave regularisation, and open workflows will be shared well ahead of the transition date."),
        ],
    },
    {
        "slug": "onboarding-systems",
        "title": "Onboarding, Systems & Access",
        "description": "Timelines for credentials, system access, and continuity of tools.",
        "faqs": [
            ("When will I receive new credentials and system access?", "Employees shall receive new credentials and system access on 1 September 2026."),
            ("Will my existing systems continue to work?", "Yes, in the initial phase. Core ERP and current systems will remain unchanged. If new tools are introduced later, employees will receive adequate training and support."),
        ],
    },
    {
        "slug": "how-we-work",
        "title": "How We Work Together",
        "description": "Governance, SLAs and operating rhythms between the GCC and businesses.",
        "faqs": [
            ("How will the GCC and businesses coordinate on a daily basis?", "The GCC and businesses will coordinate through a well-defined governance framework with Service Level Agreements, a clear RACI matrix, and dashboards offering real-time visibility. Operating rhythms will be co-created with business leaders so collaboration feels natural rather than imposed."),
        ],
    },
]

JOURNEY_STAGES = [
    ("Current State", "Existing business operations and enabling functions continue."),
    ("Stabilization", "Ensure business continuity and employee clarity."),
    ("Standardization", "Common processes, governance, and operating rhythms."),
    ("Automation", "Reduce repetitive tasks through technology and workflow automation."),
    ("Analytics", "Use dashboards and insights for better decision-making."),
    ("Transformation", "Build scalable, specialized, future-ready capabilities."),
]

BENEFITS = [
    ("5-Day Work Week", "Monday to Friday for better work-life balance."),
    ("Flexible Timings", "Start up to 60 minutes later within a 9-hour workday."),
    ("Enhanced Employee Experience", "A modern benefits framework designed for you."),
    ("Cross Functional Exposure", "Work across HR, Finance, Procurement, and IT."),
    ("Automation & AI Exposure", "Hands-on with modern workflows and AI-led tools."),
    ("Career Development", "Structured pathways and specialized growth tracks."),
]

HR_SPOCS = [
    ("Rahul Gupta", "Head - HR, GCC", "rahul.gupta01@arvind.in"),
    ("Manish Upadhyaya", "Talent Acquisition", "manish.upadhyaya@arvind.in"),
    ("M. Durga Prasanth", "Employee Life Cycle Management", "durga.prasanth@arvind.in"),
    ("Prashant Sharma", "HR Transformation & Analytics", "Prashant.Sharma@arvind.in"),
    ("Vinit Shah", "Payroll", "Vinit.shah@arvind.in"),
]

FINANCE_SPOCS = [
    ("Rajat Sapra", "Head - Finance, GCC", "rajat.sapra@arvind.in"),
    ("Saurabh Arora / Lalit Chhag", "Accounts Payable", "Saurabh.arora@arvind.in,lalit.chhag@arvind.in"),
    ("Sandeep Bhatt", "Record to Report", "Sandeep.bhatt@arvind.in"),
    ("Saurabh Arora", "Treasury", "Saurabh.arora@arvind.in"),
    ("Mahendra Tank", "Exports Account Receivables", "Mahendra.tank@arvind.in"),
    ("Jitendra Acharya", "Direct Tax", "Jitendra.acharya@arvind.in"),
    ("Surendra Zala", "Indirect Tax", "surendra.zala@arvind.in"),
]

GCC_SPOCS = [
    ("Ms. Shalom Christian", "GCC SPOC", "shalom.christian@arvind.in"),
]


def seed_database():
    if FAQCategory.query.first():
        return

    for i, (question, answer) in enumerate(TOP_FAQS):
        db.session.add(
            FAQ(
                question=question,
                answer=answer,
                is_top=True,
                sort_order=i,
            )
        )

    for cat_idx, cat in enumerate(CATEGORIES):
        category = FAQCategory(
            slug=cat["slug"],
            title=cat["title"],
            description=cat["description"],
            sort_order=cat_idx,
        )
        db.session.add(category)
        db.session.flush()

        for faq_idx, (question, answer) in enumerate(cat["faqs"]):
            db.session.add(
                FAQ(
                    category_id=category.id,
                    question=question,
                    answer=answer,
                    is_top=False,
                    sort_order=faq_idx,
                )
            )

    for i, (title, description) in enumerate(JOURNEY_STAGES):
        db.session.add(JourneyStage(title=title, description=description, sort_order=i))

    for i, (title, description) in enumerate(BENEFITS):
        db.session.add(Benefit(title=title, description=description, sort_order=i))

    for i, (name, fn, email) in enumerate(HR_SPOCS):
        db.session.add(
            Spoc(name=name, function_name=fn, email=email, spoc_type="hr", sort_order=i)
        )

    for i, (name, fn, email) in enumerate(FINANCE_SPOCS):
        db.session.add(
            Spoc(name=name, function_name=fn, email=email, spoc_type="finance", sort_order=i)
        )

    for i, (name, fn, email) in enumerate(GCC_SPOCS):
        db.session.add(
            Spoc(name=name, function_name=fn, email=email, spoc_type="gcc", sort_order=i)
        )

    db.session.commit()
