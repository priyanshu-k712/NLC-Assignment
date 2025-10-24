from pptx import Presentation


def generate_pptx(json_code):
    path = "data/output.pptx"
    ppt = Presentation()
    slide_layout = ppt.slide_layouts[1]

    for slide_data in json_code:
        slide = ppt.slides.add_slide(slide_layout)
        title_shape = slide.shapes.title
        content_shape = slide.placeholders[1]

        title_shape.text = slide_data.get('title', 'Untitled Slide')

        tf = content_shape.text_frame
        tf.clear()

        content = slide_data.get('content', '') or slide_data.get('bullets', '')

        if isinstance(content, str):
            tf.text = content
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
                    tf.text = bullet_text
                else:
                    p = tf.add_paragraph()
                    p.text = bullet_text
                    p.level = 0

    ppt.save(path)
    return path