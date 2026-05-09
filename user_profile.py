from pypdf import PdfReader


class Profile:

    def __init__(self, name, linkedin_path, summary_path):
        self.name = name
        self.linkedin = self._load_linkedin(linkedin_path)
        self.summary = self._load_summary(summary_path)

    def _load_linkedin(self, path):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text

    def _load_summary(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
