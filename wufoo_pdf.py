import fpdf
import os
import re

class WufooPDF(object):
    def __init__(self):
        self.pdf = fpdf.FPDF(format='letter')
        self.pdf.add_font('dejavu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
        self.pdf.add_font('dejavub', '', 'fonts/DejaVuSansCondensed-Bold.ttf', uni=True)

    def append(self, entry, title=''):
        self.pdf.add_page()
        self.add_title(title)
        self.add_questions(entry)

    def save(self, out):
        self.pdf.output(out)

    def add_questions(self, questions):
        for (i, (question, answer)) in enumerate(questions):
            self.add_question(question, answer)

    def add_question(self, question, answer):
        self.add_header(question)
        lines = [l for l in self.preprocess_fpdf_text(answer).splitlines() if l != '']
        for answer_line in lines:
            self.add_paragraph(answer_line)
            self.add_spacing(4)

    def preprocess_fpdf_text(self, text):
        # https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python 
        # FPDF doesn't like emojis, so remove them here.
        emoji_pattern = re.compile('['
            u'\U0001F600-\U0001F64F'  # emoticons
            u'\U0001F300-\U0001F5FF'  # symbols & pictographs
            u'\U0001F680-\U0001F6FF'  # transport & map symbols
            u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
           ']+', flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)

        # FPDF doesn't correctly display tabs. Just convert to spaces.
        text = text.replace('\t', '    ')

        return text

    def add_title(self, title):
        self.pdf.set_font('dejavu', size=22)
        self.pdf.cell(0, txt=title, ln=1, align='C')
        self.pdf.cell(0, 10, ln=1)

    def add_header(self, txt):
        self.pdf.set_font('dejavub', size=14)
        self.pdf.multi_cell(0, 10, txt=txt, align='L')

    def add_cover_page(self, txt):
        self.pdf.add_page()
        self.pdf.set_font('dejavub', size=22)
        self.pdf.ln(110)
        self.pdf.multi_cell(0, 10, txt=txt, align='C')

    def add_paragraph(self, txt):
        self.pdf.set_font('dejavu', size=12)
        self.pdf.multi_cell(0, 10, txt=txt, align='L')

    def add_spacing(self, height=10):
        self.pdf.cell(0, height, ln=1)


