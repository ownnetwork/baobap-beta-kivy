# MIT License -> LISCENCE.mit

from datetime import datetime
import json

"""
Adding chat content for a contact
"""
class AddChatContent(object):

    def __init__(self, chat_id: str, from_id: str, type: str, data: str, datatime: dict = []):
        try:
            with open(f'db/chat/{chat_id}.json', 'r+') as f:
                now = datetime.now()
                d = json.load(f)

                if not datatime:
                    year, month, day, hour, minute, second = str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute), str(now.second)
                elif datatime:
                    year, month, day, hour, minute, second = datatime['year'], datatime['month'], datatime['day'], datatime['hour'], datatime['minute'], datatime['second']

                if not d.get(year):
                    d.update({year: {}})
                    d = d.copy()

                if not d[year].get(month):
                    d[year].update({month: {}})
                    d = d.copy()

                if not d[year][month].get(day):
                    d[year][month].update({day: {}})
                    d = d.copy()

                seekdata = {
                        now.strftime(f"{hour}:{minute}:{second}"): {
                            "from_id": from_id,
                            "type": type,
                            "data": data}
                            }

                d[year][month][day].update(seekdata)
                f.seek(0)
                json.dump(d, f)
        except FileNotFoundError:
            with open(foldername, 'w') as f:
                json.dump({}, f)
            return self.add_chat_data(foldername, from_id, type, data)
