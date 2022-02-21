
# 与WebageItem对标的实体类
class WebPage():
    def __init__(self, Url, StateMent, Count):
        self.Url = Url
        self.StateMent = StateMent
        self.Count = Count
    # item转化entity
    def item2entity(webpage_item):
        Url = webpage_item['Url']
        StateMent = webpage_item['StateMent']
        Count = webpage_item['Count']
        return WebPage(Url, StateMent, Count)