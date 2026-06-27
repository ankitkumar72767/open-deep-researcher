from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(report_text):

    pdf_file = "research_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    story = []

    for line in report_text.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        if line.startswith("#"):
            line = line.replace("#", "")
            story.append(
                Paragraph(line, styles["Heading2"])
            )

        else:
            story.append(
                Paragraph(line, styles["BodyText"])
            )

        story.append(
            Spacer(1, 4)
        )

    doc.build(story)

    return pdf_file