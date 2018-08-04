from app.view_models.book import BookViewModel


class MyDrift(object):
    def __init__(self, drift_of_mine, drift_count_list):
        self.drifts = []
        # 绑定传入的参数方便使用
        self._drift_of_mine = drift_of_mine
        self._drift_count_list = drift_count_list
        # 调用转换方法
        self.drifts = self.__parse()

    # 整合视图模型数组
    def __parse(self):
        temp = []
        for drift in self._drift_of_mine:
            mydrift = self.__matching(drift)
            temp.append(mydrift)
        return temp
    
    def __matching(self, drift):
        count = 0
        # 遍历愿望清单数组，比对礼物和愿望的isbn，判断当前数据的需求数量
        for rift in self._drift_count_list:
            if drift.isbn == rift['isbn']:
                count = rift['count']
        r = {"id": drift.id, "book": BookViewModel(drift.book), "drifts_count": count}
        return r
