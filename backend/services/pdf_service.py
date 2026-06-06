import io
import json
import logging
from datetime import datetime, timezone
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

logger = logging.getLogger(__name__)

def _parse_field(field_val, default_val):
    if isinstance(field_val, str):
        try:
            return json.loads(field_val)
        except Exception:
            return field_val
    return field_val if field_val is not None else default_val

def generate_report_pdf(report_data: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterTitle', alignment=TA_CENTER, fontSize=28, leading=34, spaceAfter=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#111827')))
    styles.add(ParagraphStyle(name='CenterSubtitle', alignment=TA_CENTER, fontSize=16, leading=22, spaceAfter=24, fontName='Helvetica', textColor=colors.HexColor('#4B5563')))
    
    styles.add(ParagraphStyle(name='SectionHeader', alignment=TA_LEFT, fontSize=16, leading=22, spaceAfter=16, spaceBefore=24, fontName='Helvetica-Bold', textColor=colors.HexColor('#111827')))
    styles.add(ParagraphStyle(name='SubHeader', alignment=TA_LEFT, fontSize=13, leading=18, spaceAfter=10, spaceBefore=14, fontName='Helvetica-Bold', textColor=colors.HexColor('#374151')))
    
    styles.add(ParagraphStyle(name='NormalText', parent=styles['Normal'], fontSize=11, leading=18, spaceAfter=8, textColor=colors.HexColor('#374151')))
    styles.add(ParagraphStyle(name='BulletItem', parent=styles['Normal'], fontSize=11, leading=18, spaceAfter=6, leftIndent=15, textColor=colors.HexColor('#374151')))
    styles.add(ParagraphStyle(name='Footer', alignment=TA_CENTER, fontSize=9, leading=12, textColor=colors.HexColor('#9CA3AF')))
    
    Story = []
    
    def add_hr():
        Story.append(Spacer(1, 15))
        Story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB'), spaceBefore=0, spaceAfter=15))
    
    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------
    Story.append(Paragraph("ProjectReviewer", styles['CenterTitle']))
    Story.append(Paragraph("GitHub Project Analysis Report", styles['CenterSubtitle']))
    
    add_hr()
    
    # ---------------------------------------------------------
    # Repository Summary
    # ---------------------------------------------------------
    Story.append(Paragraph("Repository Summary", styles['SectionHeader']))
    
    repo_name = str(report_data.get("name", report_data.get("repo_name", "N/A")))
    repo_url = str(report_data.get("repo_url", "N/A"))
    project_type = str(report_data.get("project_type", "N/A"))
    language = str(report_data.get("language", "N/A"))
    
    analyzed_at = report_data.get("analyzed_at", datetime.now(timezone.utc).isoformat())
    if isinstance(analyzed_at, str):
        try:
            analyzed_at = datetime.fromisoformat(analyzed_at.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")
        except ValueError:
            pass
    elif isinstance(analyzed_at, datetime):
        analyzed_at = analyzed_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        
    summary_data = [
        [Paragraph("<b>Repository Name:</b>", styles['NormalText']), Paragraph(repo_name, styles['NormalText'])],
        [Paragraph("<b>Repository URL:</b>", styles['NormalText']), Paragraph(repo_url, styles['NormalText'])],
        [Paragraph("<b>Project Type:</b>", styles['NormalText']), Paragraph(project_type, styles['NormalText'])],
        [Paragraph("<b>Primary Language:</b>", styles['NormalText']), Paragraph(language, styles['NormalText'])],
        [Paragraph("<b>Analysis Date:</b>", styles['NormalText']), Paragraph(str(analyzed_at), styles['NormalText'])]
    ]
    
    t = Table(summary_data, colWidths=[130, 330])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    Story.append(t)
    
    add_hr()
    
    # ---------------------------------------------------------
    # Executive Summary
    # ---------------------------------------------------------
    Story.append(Paragraph("Executive Summary", styles['SectionHeader']))
    
    evaluation = _parse_field(report_data.get("evaluation", {}), {})
    if not isinstance(evaluation, dict):
        evaluation = {}
        
    score = evaluation.get("score", report_data.get("score", "N/A"))
    maturity = evaluation.get("maturity", report_data.get("maturity", "N/A"))
    potential = evaluation.get("potential_score", report_data.get("potential_score", "N/A"))
    
    exec_data = [
        [Paragraph("<b>Overall Score:</b>", styles['NormalText']), Paragraph(f"{score}/100", styles['NormalText'])],
        [Paragraph("<b>Project Maturity:</b>", styles['NormalText']), Paragraph(str(maturity).capitalize(), styles['NormalText'])],
        [Paragraph("<b>Potential Score:</b>", styles['NormalText']), Paragraph(f"{potential}/100", styles['NormalText'])]
    ]
    
    t2 = Table(exec_data, colWidths=[130, 330])
    t2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    Story.append(t2)
    Story.append(Spacer(1, 10))
    
    # Hardcode a professional summary sentence if none provided
    desc = report_data.get("description", "")
    if not desc or len(desc) < 10:
        desc = f"This repository demonstrates a {maturity.lower()} web application architecture. The project follows modern development practices and shows strong implementation quality in its primary language: {language}."
        
    Story.append(Paragraph("<b>Summary:</b>", styles['NormalText']))
    Story.append(Paragraph(desc, styles['NormalText']))
    
    add_hr()
    
    # ---------------------------------------------------------
    # Technology Stack
    # ---------------------------------------------------------
    technologies = _parse_field(report_data.get("technologies", []), [])
    if isinstance(technologies, dict):
        technologies = [technologies]
        
    Story.append(Paragraph("Technology Stack", styles['SectionHeader']))
    if not technologies:
        Story.append(Paragraph("No technologies detected.", styles['NormalText']))
    else:
        tech_list = []
        if isinstance(technologies, list):
            for t_item in technologies:
                if isinstance(t_item, dict):
                    tech_list.append(str(t_item.get("name", t_item.get("technology", "Unknown"))))
                else:
                    tech_list.append(str(t_item))
        elif isinstance(technologies, str):
            tech_list.append(technologies)
            
        for t_val in tech_list:
            Story.append(Paragraph(f"• {t_val}", styles['BulletItem']))
            
    add_hr()
        
    # ---------------------------------------------------------
    # Strengths
    # ---------------------------------------------------------
    capabilities = _parse_field(report_data.get("capabilities", report_data.get("features", [])), [])
    if isinstance(capabilities, dict):
        capabilities = [capabilities]
        
    Story.append(Paragraph("Strengths", styles['SectionHeader']))
    if not capabilities:
        Story.append(Paragraph("No strengths detected.", styles['NormalText']))
    else:
        if isinstance(capabilities, list):
            for cap in capabilities:
                if isinstance(cap, dict):
                    category = cap.get('category', cap.get('name', 'Feature'))
                    desc_val = cap.get('description', '')
                    text = f"✓ <b>{category}</b>: {desc_val}" if desc_val else f"✓ <b>{category}</b>"
                    Story.append(Paragraph(text, styles['BulletItem']))
                else:
                    Story.append(Paragraph(f"✓ {str(cap)}", styles['BulletItem']))
        elif isinstance(capabilities, str):
            Story.append(Paragraph(f"✓ {capabilities}", styles['BulletItem']))
            
    add_hr()
        
    # ---------------------------------------------------------
    # Missing Features
    # ---------------------------------------------------------
    missing = _parse_field(evaluation.get("missing_features", []), [])
    if isinstance(missing, dict):
        missing = [missing]
        
    if missing:
        Story.append(Paragraph("Missing Features", styles['SectionHeader']))
        if isinstance(missing, list):
            for m in missing:
                if isinstance(m, dict):
                    m_str = str(m.get('name', m.get('feature', 'Unknown Feature')))
                else:
                    m_str = str(m)
                Story.append(Paragraph(f"⚠ {m_str}", styles['BulletItem']))
        elif isinstance(missing, str):
            Story.append(Paragraph(f"⚠ {missing}", styles['BulletItem']))
            
        add_hr()
        
    # ---------------------------------------------------------
    # Improvement Recommendations
    # ---------------------------------------------------------
    recommendations = _parse_field(report_data.get("recommendations", []), [])
    if isinstance(recommendations, dict):
        recommendations = [recommendations]
        
    if recommendations:
        Story.append(Paragraph("Improvement Recommendations", styles['SectionHeader']))
        Story.append(Paragraph("<b>HIGH PRIORITY</b>", styles['SubHeader']))
        
        if isinstance(recommendations, list):
            for idx, rec in enumerate(recommendations, 1):
                if isinstance(rec, dict):
                    title = rec.get('title', rec.get('name', 'Improvement Suggestion'))
                    impact = rec.get('impact', 'High')
                    points = rec.get('points', '')
                    impact_str = f"{impact}" + (f" (+{points} Points)" if points else "")
                    reason = rec.get('reason', rec.get('description', 'Improves project quality and engineering standards.'))
                    
                    Story.append(Paragraph(f"<b>{idx}. {title}</b>", styles['NormalText']))
                    Story.append(Paragraph(f"Impact: {impact_str}", styles['BulletItem']))
                    Story.append(Paragraph("<b>Reason:</b>", styles['NormalText']))
                    Story.append(Paragraph(f"{reason}", styles['NormalText']))
                    Story.append(Spacer(1, 15))
                else:
                    Story.append(Paragraph(f"<b>{idx}. Improvement Suggestion</b>", styles['NormalText']))
                    Story.append(Paragraph(f"{str(rec)}", styles['NormalText']))
                    Story.append(Spacer(1, 15))
        elif isinstance(recommendations, str):
            Story.append(Paragraph(f"<b>1. Improvement Suggestion</b>", styles['NormalText']))
            Story.append(Paragraph(recommendations, styles['NormalText']))
            Story.append(Spacer(1, 15))
            
        add_hr()
        
    # ---------------------------------------------------------
    # Project Evaluation
    # ---------------------------------------------------------
    Story.append(Paragraph("Project Evaluation", styles['SectionHeader']))
    metrics = evaluation.get("metrics", {})
    if not isinstance(metrics, dict):
        metrics = {}
        
    arch_score = metrics.get("architecture_score", "N/A")
    sec_score = metrics.get("security_score", "N/A")
    doc_score = metrics.get("documentation_score", "N/A")
    dep_score = metrics.get("deployment_readiness", "N/A")
    maint_score = metrics.get("maintainability_score", "N/A")
    
    eval_data = [
        [Paragraph("Architecture Score:", styles['NormalText']), Paragraph(str(arch_score), styles['NormalText'])],
        [Paragraph("Security Score:", styles['NormalText']), Paragraph(str(sec_score), styles['NormalText'])],
        [Paragraph("Documentation Score:", styles['NormalText']), Paragraph(str(doc_score), styles['NormalText'])],
        [Paragraph("Deployment Readiness:", styles['NormalText']), Paragraph(str(dep_score), styles['NormalText'])],
        [Paragraph("Maintainability Score:", styles['NormalText']), Paragraph(str(maint_score), styles['NormalText'])]
    ]
    t3 = Table(eval_data, colWidths=[180, 280])
    t3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    Story.append(t3)
    
    add_hr()
    
    # ---------------------------------------------------------
    # Resume Highlights
    # ---------------------------------------------------------
    Story.append(Paragraph("Resume Highlights", styles['SectionHeader']))
    
    # Generate automatic highlights
    tech_str = ", ".join(tech_list[:3]) if 'tech_list' in locals() and tech_list else language
    highlight_1 = f"Developed a {project_type.lower()} architecture integrating core technologies such as {tech_str}."
    highlight_2 = f"Implemented {len(capabilities) if isinstance(capabilities, list) else 3} key features, enforcing robust engineering practices that achieved an overall code quality score of {score}/100."
    highlight_3 = f"Designed project workflows emphasizing strong architecture and maintainability standards, reaching a maturity level of '{maturity}'."
    
    Story.append(Paragraph(f"• {highlight_1}", styles['BulletItem']))
    Story.append(Paragraph(f"• {highlight_2}", styles['BulletItem']))
    Story.append(Paragraph(f"• {highlight_3}", styles['BulletItem']))
    
    add_hr()
    
    # ---------------------------------------------------------
    # Footer
    # ---------------------------------------------------------
    Story.append(Spacer(1, 20))
    Story.append(Paragraph("Generated by ProjectReviewer", styles['Footer']))
    Story.append(Paragraph(f"Generated On: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}", styles['Footer']))
    Story.append(Paragraph("This report is automatically generated based on repository analysis.", styles['Footer']))
    
    doc.build(Story)
    buffer.seek(0)
    return buffer
