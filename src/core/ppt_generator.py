from pptx import Presentation
from pptx.util import Pt, Inches



def generate_pptx(json_code):
    path = "data/output.pptx"
    ppt = Presentation()
    slide_layout = ppt.slide_layouts[1]


    for slide_data in json_code:
        slide = ppt.slides.add_slide(slide_layout)
        title_shape = slide.shapes.title
        content_shape = slide.placeholders[1]

        title_shape.text = slide_data.get('title', 'Untitled Slide')
        if title_shape.text_frame.paragraphs:
            title_para = title_shape.text_frame.paragraphs[0]
            title_para.font.size = Pt(32)
            title_para.font.bold = True

        tf = content_shape.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.auto_size = None

        tf.margin_left = Inches(0.1)
        tf.margin_right = Inches(0.1)
        tf.margin_top = Inches(0.1)
        tf.margin_bottom = Inches(0.1)

        content = slide_data.get('content', '') or slide_data.get('bullets', '')

        if isinstance(content, str):
            p = tf.paragraphs[0]
            p.text = content
            p.font.size = Pt(16)
            p.space_before = Pt(0)
            p.space_after = Pt(6)
            p.line_spacing = 1.2

        elif isinstance(content, list):
            for i, bullet_item in enumerate(content):

                bullet_text = ""
                if isinstance(bullet_item, str):
                    bullet_text = bullet_item
                elif isinstance(bullet_item, dict):
                    bullet_text = bullet_item.get('point',
                                                  bullet_item.get('bullet', bullet_item.get('item', str(bullet_item))))
                else:
                    bullet_text = str(bullet_item)

                if i == 0:
                    p = tf.paragraphs[0]
                    p.text = bullet_text
                else:
                    p = tf.add_paragraph()
                    p.text = bullet_text

                p.level = 0
                p.font.size = Pt(16)
                p.space_before = Pt(6)
                p.space_after = Pt(6)
                p.line_spacing = 1.15

    ppt.save(path)
    return path