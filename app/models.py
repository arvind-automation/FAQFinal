from datetime import datetime, timezone

from app import db


class FAQCategory(db.Model):
    __tablename__ = "faq_categories"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    faqs = db.relationship(
        "FAQ",
        backref="category",
        lazy=True,
        order_by="FAQ.sort_order",
        cascade="all, delete-orphan",
    )


class FAQ(db.Model):
    __tablename__ = "faqs"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("faq_categories.id"), nullable=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    is_top = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)


class JourneyStage(db.Model):
    __tablename__ = "journey_stages"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)


class Benefit(db.Model):
    __tablename__ = "benefits"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)


class Spoc(db.Model):
    __tablename__ = "spocs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    function_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(512), nullable=False)
    spoc_type = db.Column(db.String(32), nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    helpful = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
