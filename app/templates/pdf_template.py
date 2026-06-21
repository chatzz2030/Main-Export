"""PDF HTML template and Jinja2 environment setup."""
from jinja2 import Environment, BaseLoader, select_autoescape
from app.config import BRAND_COLOR

PDF_TEMPLATE = """
<html>
<head>
<style>
    @page {
        margin: 2.2cm 2cm 2.5cm 2cm;
        @bottom-center {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 9px;
            color: #80868b;
        }
    }
    body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #333333; line-height: 1.6; font-size: 13px; }
    .brand-header { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 3px solid """ + BRAND_COLOR + """; padding-bottom: 6px; margin-bottom: 18px; }
    .brand-header .label { font-size: 11px; letter-spacing: 1px; text-transform: uppercase; color: """ + BRAND_COLOR + """; font-weight: bold; }
    .brand-header .date { font-size: 11px; color: #80868b; }
    h1 { color: #202124; font-size: 22px; margin: 4px 0 14px 0; }
    h2 { color: #202124; margin-top: 24px; font-size: 15px; border-left: 4px solid """ + BRAND_COLOR + """; padding-left: 8px; }
    h3 { color: """ + BRAND_COLOR + """; font-size: 13px; margin: 14px 0 4px 0; }
    .metadata { background-color: #f8f9fa; padding: 12px 14px; border-radius: 6px; margin-bottom: 18px; font-size: 12.5px; border: 1px solid #dadce0; }
    .metadata a { color: """ + BRAND_COLOR + """; text-decoration: none; font-weight: 600; word-break: break-all; }
    .thumb { max-width: 240px; border-radius: 6px; margin-bottom: 14px; display: block; }
    ul { padding-left: 20px; margin-top: 8px; }
    li { margin-bottom: 6px; }
    .topic-card { background: #fafbfc; border: 1px solid #e8eaed; border-radius: 6px; padding: 10px 14px; margin-bottom: 10px; }
    .closing { background: #f0f6ff; border-left: 4px solid """ + BRAND_COLOR + """; padding: 12px 16px; margin-top: 22px; font-style: italic; border-radius: 0 6px 6px 0; }
    .empty { color: #9aa0a6; font-style: italic; font-size: 12px; }
</style>
</head>
<body>
    <div class="brand-header">
        <span class="label">Video Synopsis</span>
        <span class="date">Generated {{ generated_on }}</span>
    </div>

    {% if meta.thumbnail_url %}
    <img class="thumb" src="{{ meta.thumbnail_url }}" />
    {% endif %}

    <h1>{{ meta.title }}</h1>

    <div class="metadata">
        {% if meta.channel_name %}<strong>Channel:</strong> {{ meta.channel_name }}<br/>{% endif %}
        <strong>Source Video:</strong>
        <a href="{{ meta.video_url }}">{{ meta.video_url }}</a>
    </div>

    <h2>Overall Synopsis</h2>
    <p>{{ summary.basic_summary.overall_synopsis }}</p>

    <h2>{{ summary.topics_covered.title }}</h2>
    {% if summary.topics_covered.topics %}
    <ul>{% for t in summary.topics_covered.topics %}<li>{{ t }}</li>{% endfor %}</ul>
    {% else %}<p class="empty">No topics provided.</p>{% endif %}

    <h2>Key Insights</h2>
    {% if summary.detailed_summary.key_insights %}
    <ul>{% for i in summary.detailed_summary.key_insights %}<li>{{ i }}</li>{% endfor %}</ul>
    {% else %}<p class="empty">No insights provided.</p>{% endif %}

    {% if summary.detailed_summary.topic_breakdown %}
    <h2>Topic Breakdown</h2>
    {% for item in summary.detailed_summary.topic_breakdown %}
    <div class="topic-card">
        <h3>{{ item.topic }}</h3>
        <p>{{ item.explanation }}</p>
    </div>
    {% endfor %}
    {% endif %}

    <h2>Action Items</h2>
    {% if summary.detailed_summary.action_items %}
    <ul>{% for a in summary.detailed_summary.action_items %}<li>{{ a }}</li>{% endfor %}</ul>
    {% else %}<p class="empty">No action items provided.</p>{% endif %}

    <div class="closing">{{ summary.closing_note }}</div>
</body>
</html>
"""

_jinja_env = Environment(loader=BaseLoader(), autoescape=select_autoescape(["html", "xml"]))
_pdf_template = _jinja_env.from_string(PDF_TEMPLATE)
