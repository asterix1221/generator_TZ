from docx import Document
from docx.shared import Inches, Pt
from typing import Dict, Any
import json


def generate_docx(specification: Dict[str, Any], title: str) -> bytes:
    doc = Document()
    
    doc.add_heading(title, level=0)
    
    def add_section(heading: str, content: Any):
        doc.add_heading(heading, level=1)
        if isinstance(content, list):
            for item in content:
                doc.add_paragraph(f"• {item}")
        else:
            doc.add_paragraph(str(content))
    
    sections = [
        ("Цель", specification.get("goal")),
        ("Описание", specification.get("description")),
        ("Функциональные требования", specification.get("functional_requirements")),
        ("Требования к БД", specification.get("db_requirements")),
        ("Стек технологий", specification.get("tech_stack")),
        ("Список фич", specification.get("features"))
    ]
    
    for heading, content in sections:
        if content:
            add_section(heading, content)
    
    doc.add_paragraph()
    doc.add_paragraph(f"Тип проекта: {specification.get('type', 'N/A')}")
    doc.add_paragraph(f"Уровень сложности: {specification.get('complexity', 'N/A')}")
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def generate_pdf(specification: Dict[str, Any], title: str) -> bytes:
    from weasyprint import HTML
    from io import BytesIO
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; margin-top: 20px; }}
            ul {{ margin-left: 20px; }}
            li {{ margin-bottom: 5px; }}
            .meta {{ color: #7f8c8d; font-size: 12px; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        
        <h2>Цель</h2>
        <p>{specification.get('goal', '')}</p>
        
        <h2>Описание</h2>
        <p>{specification.get('description', '')}</p>
        
        <h2>Функциональные требования</h2>
        <ul>
            {"".join(f"<li>{item}</li>" for item in specification.get('functional_requirements', []))}
        </ul>
        
        <h2>Требования к БД</h2>
        <ul>
            {"".join(f"<li>{item}</li>" for item in specification.get('db_requirements', []))}
        </ul>
        
        <h2>Стек технологий</h2>
        <ul>
            {"".join(f"<li>{item}</li>" for item in specification.get('tech_stack', []))}
        </ul>
        
        <h2>Список фич</h2>
        <ul>
            {"".join(f"<li>{item}</li>" for item in specification.get('features', []))}
        </ul>
        
        <div class="meta">
            <p>Тип проекта: {specification.get('type', 'N/A')}</p>
            <p>Уровень сложности: {specification.get('complexity', 'N/A')}</p>
        </div>
    </body>
    </html>
    """
    
    return HTML(string=html_content).write_pdf()


def generate_trello_json(specification: Dict[str, Any], title: str) -> dict:
    features = specification.get("features", [])
    if not features:
        features = specification.get("functional_requirements", [])[:5]
    
    lists = [
        {
            "name": "To Do",
            "cards": [{"name": feat} for feat in features[:3]]
        },
        {
            "name": "In Progress",
            "cards": []
        },
        {
            "name": "Done",
            "cards": []
        }
    ]
    
    return {
        "board_name": f"TZ: {title}",
        "lists": lists
    }


from io import BytesIO