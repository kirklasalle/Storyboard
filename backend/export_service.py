from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import zipfile
import io
import os
from typing import List, Dict, Any

class ExportService:
    @staticmethod
    def generate_pdf(project_name: str, frames: List[Dict[str, Any]], output_path: str):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 50, f"Storyboard: {project_name}")
        
        y_offset = height - 100
        for frame in frames:
            if y_offset < 200:
                c.showPage()
                y_offset = height - 50
                
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_offset, f"Scene {frame['scene_number']}: {frame['heading']}")
            y_offset -= 20
            
            # Placeholder for image (if local path exists)
            if frame.get('image_path') and os.path.exists(frame['image_path']):
                try:
                    img = ImageReader(frame['image_path'])
                    c.drawImage(img, 50, y_offset - 250, width=400, height=225) # 16:9 ratio
                    y_offset -= 260
                except:
                    c.drawString(50, y_offset, "[Image Placeholder]")
                    y_offset -= 20
            else:
                c.drawString(50, y_offset, "[Image Pending]")
                y_offset -= 20
                
            c.setFont("Helvetica", 10)
            text_object = c.beginText(50, y_offset)
            text_object.setFont("Helvetica", 10)
            description = frame.get('description', '')
            # Simple text wrap
            from reportlab.lib.utils import simpleSplit
            lines = simpleSplit(description, "Helvetica", 10, width - 100)
            for line in lines:
                text_object.textLine(line)
            c.drawText(text_object)
            
            y_offset -= (len(lines) * 12 + 40)
            
        c.save()

    @staticmethod
    def generate_zip(frames: List[Dict[str, Any]], zip_output_path: str):
        with zipfile.ZipFile(zip_output_path, 'w') as zipf:
            for frame in frames:
                if frame.get('image_path') and os.path.exists(frame['image_path']):
                    filename = f"scene_{frame['scene_number']}_{frame['intensity_type'].lower()}.jpg"
                    zipf.write(frame['image_path'], arcname=filename)
