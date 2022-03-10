import json
import requests
from bs4 import BeautifulSoup



class Sksdb:


    def __init__(self):

        self.announcement = {}
        self.name = 'SKSDB'

        with open('userConfigs.json') as file:
            self.subscribers = json.load(file)[self.name]


    def __update_subscribers(self):

        with open('userConfigs.json') as file:
            user_configs = json.load(file)
            user_configs[self.name] = self.subscribers
            json_object = json.dumps(user_configs)

        with open('userConfigs.json', 'w') as file:
            file.write(json_object)


    def add_subscriber(self, user_id):

        if user_id not in self.subscribers:
            self.subscribers.append(user_id)
            self.__update_subscribers()


    def remove_subscriber(self, user_id):

        if user_id in self.subscribers:
            self.subscribers.remove(user_id)
            self.__update_subscribers()


    def get_announcement(self):

        r = requests.get('http://www.sksdb.hacettepe.edu.tr/bidbnew/index.php')
        r.encoding = 'utf-8'
        html_text = r.text

        soup = BeautifulSoup(html_text, 'lxml')
        announcement = soup.find_all('p')[8].find('a')

        title = announcement.text
        content = None
        url = announcement.get('href')

        self.announcement = {
            "title": title,
            "content": content,
            "url": url
        }

        with open('announcements.json') as file:
            oldAnnouncements = json.load(file)
            lastAnnouncementFromDB = oldAnnouncements['SKSDB'][0]

        if lastAnnouncementFromDB != self.announcement:
            with open('announcements.json', 'w', encoding='utf-8') as f:
                oldAnnouncements['SKSDB'][0] = self.announcement
                json_object = json.dumps(oldAnnouncements, indent=4, ensure_ascii=False)

                f.write(json_object)
        else:
            self.announcement = None

        return self.announcement