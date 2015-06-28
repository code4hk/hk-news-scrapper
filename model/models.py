from model.content import Content
from pymongo import MongoClient
from datetime import datetime
from util.env import db_url
from util import logger


log = logger.get(__name__)


class Articles(object):
    def __init__(self):
        client = MongoClient(db_url())
        self.news = client.newsdiff.news
        self.revisions = client.newsdiff.revisions

    def save_entry(self, article):
        content = Content.from_article(article)
        news_cursor = self.news.find({"url": article.url})
        if news_cursor.count() == 0:
            log.info('new entry: %s', article.url)
            self.new_entry(article.code, article.url, article.lang, content)
        else:
            nid = news_cursor[0]['_id']
            revision_cursor = self.revisions.find({'nid': str(nid)})
            first_version = revision_cursor[0]
            count = revision_cursor.count()
            last_revision = revision_cursor[count - 1]
            if content.change_ratio(last_revision) > 0:
                log.info('entry version %s: %s', count, article.url)
                self.update_news_entry(nid, content.title, content.change_ratio(first_version), count)
                self.new_revision(nid, count, content)
            else:
                log.debug('entry not modified: %s', article.url)
                self.update_last_check_time(nid)

    def new_entry(self, publisher, url, lang, content):
        now = datetime.utcnow()
        news_entry = {"url": url,
                      "title": content.title,
                      "publisher": publisher,
                      "comments_no": 0,
                      "changes": 0,
                      "count": 1,
                      "lang": lang,
                      "created_at": now,
                      "updated_at": now,
                      "last_check": now
                      }
        result = self.news.insert_one(news_entry)
        self.new_revision(result.inserted_id, 0, content)

    def new_revision(self, nid, version, content):
        revision_entry = {"nid": str(nid),
                          "version": version,
                          "title": content.title,
                          "published_at": content.date,
                          "body": content.body,
                          "archive_time": datetime.utcnow()
                          }
        self.revisions.insert_one(revision_entry)

    def update_news_entry(self, nid, title, changes, count):
        now = datetime.utcnow()
        self.news.update_one({'_id': nid}, {'$set': {
            'title': title, 'changes': changes, "updated_at": now, "last_check": now, "count": count + 1}})

    def update_last_check_time(self, nid):
        self.news.update_one({"_id": nid}, {'$set': {"last_check": datetime.utcnow()}})

    def get_all_active_urls(self, days):
        log.info('getting urls changed within %s days', days)
        return self.news.find({'$where': 'this.updated_at > this.last_check-' + str(days * 86400000)}).distinct('url')
