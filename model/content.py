from difflib import SequenceMatcher


class Content(object):
    def __init__(self, title, date, body):
        self.title = title
        self.date = date
        self.body = body

    def __str__(self):
        return self.title + self.date + self.body

    def change_ratio(self, revision):
        return 1 - SequenceMatcher(None, str(self.from_revision(revision)), str(self), False).ratio()

    @classmethod
    def from_revision(cls, revision):
        return cls(revision['title'], revision['published_at'], revision['body'])

    @classmethod
    def from_article(cls, article):
        return cls(article.title, article.date, article.body)