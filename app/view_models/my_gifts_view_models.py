from app.view_models.book_view_models import SingleBookViewModel


class CollectionMygifts(object):
    def __init__(self, mygifts_source_data, wish_count_list):
        # 方便传递数据
        self.__mygifts_source_data = mygifts_source_data
        self.__wish_count_list = wish_count_list

        self.gifts = self.__parse()

    def __parse(self):
        """
        不建议在方法中直接修改实例变量
        :return:
        """
        temp_gifts = []
        # 遍历礼物表中所有数据
        for gift in self.__mygifts_source_data:
            # 到心愿列表中去查询数量
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    # 处理循环嵌套的精妙代码
    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count.get("isbn"):
                count = wish_count.get("count")
                break
        # 调用的是gift下的book属性,不是外键
        # my_gift = SingleMygift(gift.id, SingleBookViewModel(gift.book), count)
        my_gift = {
            "id": gift.id,
            "book": SingleBookViewModel(gift.book),
            "wishes_count": count
        }
        return my_gift


# class SingleMygift(object):
#     def __init__(self, id, book, count):
#         self.id = id
#         # 图书数据
#         self.book = book
#         self.wishes_count = count
