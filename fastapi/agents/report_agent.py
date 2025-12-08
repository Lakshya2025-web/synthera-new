from .state import State
import os
import uuid
import boto3
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from dotenv import load_dotenv
load_dotenv()
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client('s3', 
    region_name= os.getenv("COGNITO_REGION"),
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),)
def ensure_tmp_dir():
    tmp_dir = "/tmp/agent_reports"
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir

def make_iqvia_charts(iqvia:dict, base_dir: str):
    chart_paths = []
    vt = iqvia.get("volume_trend") or []
    if vt:
        years = [item.get("year") for item in vt]
        values = [item.get("value") for item in vt]
        plt.figure()
        plt.plot(years, values, marker="o")
        plt.xlabel("Year")
        plt.ylabel("Volume")
        plt.title("IQVIA Volume Trend")
        plt.tight_layout()
        path = os.path.join(base_dir, "iqvia_volume_trend.png")
        plt.savefig(path)
        plt.close()
        chart_paths.append(path)
    comps = iqvia.get("competitors") or []
    if comps:
        labels = [c.get("company") for c in comps]
        shares = [c.get("share") for c in comps]
        plt.figure()
        plt.bar(labels, shares)
        plt.xlabel("Company")
        plt.ylabel("Market Share (%)")
        plt.title("IQVIA Competitor Market Share")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        path = os.path.join(base_dir, "iqvia_competitors.png")
        plt.savefig(path)
        plt.close()
        chart_paths.append(path)
    return chart_paths

def make_clinical_charts(clinical: dict, base_dir:str):
    chart_paths = []
    dist = clinical.get("phase_distribution") or []
    if dist:
        phases = [d.get("phase") for d in dist]
        counts = [d.get("count") for d in dist]
        plt.figure()
        plt.bar(phases, counts)
        plt.xlabel("Phase")
        plt.ylabel("Number of Trials")
        plt.title("Clinical Trial Phase Distribution")
        plt.tight_layout()
        path = os.path.join(base_dir, "clinical_phase_distribution.png")
        plt.savefig(path)
        plt.close()
        chart_paths.append(path)
    return chart_paths  

def make_exim_charts(exim: dict, base_dir:str):
    chart_paths = []
    imp = exim.get("import_volume_mt") or []
    exp = exim.get("export_volume_mt") or []
    if imp or exp:
        years = sorted({*{i["year"] for i in imp}, *{e["year"] for e in exp}})
        imp_map = {i["year"]: i["value"] for i in imp}
        exp_map = {e["year"]: e["value"] for e in exp}
        imp_vals = [imp_map.get(y, 0) for y in years]
        exp_vals = [exp_map.get(y, 0) for y in years]
        x = range(len(years))
        plt.figure()
        width = 0.35
        plt.bar([i - width/2 for i in x], imp_vals, width=width, label="Import")
        plt.bar([i + width/2 for i in x], exp_vals, width=width, label="Export")
        plt.xticks(list(x), years)
        plt.xlabel("Year")
        plt.ylabel("Volume (MT)")
        plt.title("EXIM Import/Export Volume")
        plt.legend()
        plt.tight_layout()
        path = os.path.join(base_dir, "exim_import_export.png")
        plt.savefig(path)
        plt.close()
        chart_paths.append(path)
    return chart_paths

def make_patent_charts(patent: dict, base_dir:str):
    chart_paths = []
    timeline = patent.get("expiry_timeline") or []
    if timeline:
        years = [item.get("year") for item in timeline]
        counts = [item.get("count") for item in timeline]
        plt.figure()
        plt.bar(years, counts)
        plt.xlabel("Year")
        plt.ylabel("Patents Expiring")
        plt.title("Patent Expiry Timeline")
        plt.tight_layout()
        path = os.path.join(base_dir, "patent_expiry_timeline.png")
        plt.savefig(path)
        plt.close()
        chart_paths.append(path)
    return chart_paths   

def build_report_text(state: State) -> str:
    """
    Build a markdown-like text report from all agent outputs.
    """
    parts = []

    parts.append(f"# Intelligence Report\n")
    parts.append(f"**User Query:** {state.user_input}\n")

    if state.iqvia:
        iq = state.iqvia
        parts.append("## IQVIA Market Insights")
        ms = iq.get("market_size_usd")
        cagr = iq.get("cagr")
        parts.append(f"- Estimated market size: **{ms} USD**" if ms is not None else "- Market size: N/A")
        parts.append(f"- CAGR: **{cagr}%**" if cagr is not None else "- CAGR: N/A")

        comps = iq.get("competitors") or []
        if comps:
            parts.append("\n**Top Competitors:**")
            for c in comps:
                parts.append(f"- {c.get('company')}: {c.get('share')}% share")

    if state.exim:
        ex = state.exim
        parts.append("\n## EXIM Trade Insights")
        dep = ex.get("dependency_risk")
        if dep:
            parts.append(f"- Dependency risk: **{dep}**")
        sources = ex.get("top_import_sources") or []
        if sources:
            parts.append("**Top Import Sources:**")
            for s in sources:
                parts.append(f"- {s.get('country')}: {s.get('percent')}%")

    if state.clinical:
        cl = state.clinical
        parts.append("\n## Clinical Trial Pipeline")
        trials = cl.get("active_trials") or []
        if trials:
            parts.append("**Sample Active Trials:**")
            for t in trials[:5]:
                parts.append(
                    f"- {t.get('nct_id')}: {t.get('title')} "
                    f"({t.get('phase')}, {t.get('status')}, sponsor: {t.get('sponsor')})"
                )
        dist = cl.get("phase_distribution") or []
        if dist:
            parts.append("\n**Phase Distribution:**")
            for d in dist:
                parts.append(f"- {d.get('phase')}: {d.get('count')} trials")

    if state.patent:
        pt = state.patent
        parts.append("\n## Patent Landscape")
        patents = pt.get("patents") or []
        if patents:
            parts.append("**Key Patents:**")
            for p in patents[:5]:
                parts.append(
                    f"- {p.get('patent_number')} ({p.get('assignee')}), "
                    f"expiry {p.get('expiry_year')}, FTO risk: {p.get('fto_risk')}"
                )
        heat = pt.get("competitive_heatmap") or []
        if heat:
            parts.append("\n**Competitive Filing Heatmap (score 0–10):**")
            for h in heat:
                parts.append(f"- {h.get('company')}: {h.get('score')}")

    if state.web:
        parts.append("\n## Web Intelligence Summary\n")
        parts.append(state.web)

    if state.internal:
        parts.append("\n## Internal Document Summary\n")
        parts.append(state.internal)

    return "\n".join(parts)

def build_pdf(report_text: str, chart_paths, output_path: str):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    for line in report_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# "):
            story.append(Paragraph(stripped[2:], styles["Heading1"]))
        elif stripped.startswith("## "):
            story.append(Paragraph(stripped[3:], styles["Heading2"]))
        elif stripped.startswith("**") and stripped.endswith("**"):
            story.append(Paragraph(f"<b>{stripped[2:-2]}</b>", styles["Normal"]))
        else:
            story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 6))
    if chart_paths:
        story.append(PageBreak())
        story.append(Paragraph("Charts", styles["Heading1"]))
        story.append(Spacer(1, 12))
        for path in chart_paths:
            story.append(Image(path, width=400, height=250))
            story.append(Spacer(1, 12))
    doc.build(story)



def report_node(state: State):
    tmp_dir = ensure_tmp_dir()
    report_text = build_report_text(state)
    chart_paths = []
    if state.iqvia:
        chart_paths.extend(make_iqvia_charts(state.iqvia, tmp_dir))
    if state.exim:
        chart_paths.extend(make_exim_charts(state.exim, tmp_dir))
    if state.clinical:
        chart_paths.extend(make_clinical_charts(state.clinical, tmp_dir))
    if state.patent:
        chart_paths.extend(make_patent_charts(state.patent, tmp_dir))
    pdf_local_path = os.path.join(tmp_dir, f"report_{uuid.uuid4().hex}.pdf")
    build_pdf(report_text, chart_paths, pdf_local_path)
    file_key = f"reports/{uuid.uuid4().hex}.pdf"
    s3.upload_file(
        Filename=pdf_local_path,
        Bucket=S3_BUCKET_NAME,
        Key=file_key,
        ExtraArgs={"ContentType": "application/pdf"}
    )
    pdf_url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": S3_BUCKET_NAME, "Key": file_key},
        ExpiresIn=3600
    )
    return {
        "report": report_text,
        "pdf_s3_key": file_key,
        "pdf_url": pdf_url,
        "response": f"Report generated and uploaded.\nDownload: {pdf_url}"
    }
