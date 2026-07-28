from flask import Blueprint, abort, jsonify, render_template, request, session

from app import db
from app.access_log import is_log_admin, record_access_log
from app.auth import is_authenticated
from app.models import AccessLog, Benefit, FAQ, FAQCategory, Feedback, JourneyStage, Spoc
from app.seed import seed_database

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if is_authenticated() and not session.get("page_view_logged"):
        record_access_log("page_view")
        session["page_view_logged"] = True

    categories = FAQCategory.query.order_by(FAQCategory.sort_order).all()
    top_faqs = FAQ.query.filter_by(is_top=True).order_by(FAQ.sort_order).all()
    journey_stages = JourneyStage.query.order_by(JourneyStage.sort_order).all()
    benefits = Benefit.query.order_by(Benefit.sort_order).all()
    hr_spocs = Spoc.query.filter_by(spoc_type="hr").order_by(Spoc.sort_order).all()
    finance_spocs = Spoc.query.filter_by(spoc_type="finance").order_by(Spoc.sort_order).all()
    gcc_spocs = Spoc.query.filter_by(spoc_type="gcc").order_by(Spoc.sort_order).all()
    total_faqs = FAQ.query.count()

    return render_template(
        "index.html",
        categories=categories,
        top_faqs=top_faqs,
        journey_stages=journey_stages,
        benefits=benefits,
        hr_spocs=hr_spocs,
        finance_spocs=finance_spocs,
        gcc_spocs=gcc_spocs,
        total_faqs=total_faqs,
    )


@main_bp.route("/admin/logs")
def admin_logs():
    if not is_log_admin():
        abort(403)

    page = max(request.args.get("page", 1, type=int), 1)
    per_page = 50

    pagination = AccessLog.query.order_by(AccessLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        "admin_logs.html",
        logs=pagination.items,
        pagination=pagination,
    )


@main_bp.route("/api/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json(silent=True) or {}
    helpful = data.get("helpful")

    if helpful is None or not isinstance(helpful, bool):
        return jsonify({"error": "helpful must be a boolean"}), 400

    feedback = Feedback(helpful=helpful)
    db.session.add(feedback)
    db.session.commit()

    return jsonify({"ok": True})


@main_bp.cli.command("init-db")
def init_db_command():
    """Initialize database tables and seed portal content."""
    db.create_all()
    seed_database()
    print("Database initialized and seeded.")
