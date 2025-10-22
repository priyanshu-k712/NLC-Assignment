from pptx import Presentation

def generate_pptx(json_code):
    path = "data/output.pptx"  # added extension for clarity
    ppt = Presentation()
    slide_layout = ppt.slide_layouts[1]  # Title and Content layout

    for slide_data in json_code:
        slide = ppt.slides.add_slide(slide_layout)
        title_shape = slide.shapes.title
        content_shape = slide.placeholders[1]  # body placeholder

        # Title
        title_shape.text = slide_data.get('title', 'Untitled Slide')

        # Text content
        tf = content_shape.text_frame
        tf.clear()

        content = slide_data.get('content', '') or slide_data.get('bullets', '')

        if isinstance(content, str):
            tf.text = content
        elif isinstance(content, list):
            for i, bullet_text in enumerate(content):
                if i == 0:
                    tf.text = bullet_text
                else:
                    p = tf.add_paragraph()
                    p.text = bullet_text
                    p.level = 0

    ppt.save(path)
    return path
