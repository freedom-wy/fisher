from app.view_models.book_view_models import SingleBookViewModel


class MyGiftWishInfo(object):
    def __init__(self, my_gifts_wishes_source_data, gifts_wishes_isbn_count_list):
        # 方便传递数据
        self.__my_gifts_wishes_source_data = my_gifts_wishes_source_data
        self.__gifts_wishes_isbn_count_list = gifts_wishes_isbn_count_list

        self.trades = self.__parse()

    def __parse(self):
        """
        不建议在方法中直接修改实例变量
        :return:
        """
        temp = []
        # 遍历礼物表中所有数据
        for item in self.__my_gifts_wishes_source_data:
            # 到心愿列表和礼物列表中去查询数量
            my_gift_wish = self.matching(item)
            temp.append(my_gift_wish)
        return temp

    # 处理循环嵌套的精妙代码
    def matching(self, item):
        pass
        count = 0
        for item_count in self.__gifts_wishes_isbn_count_list:
            if item.isbn == item_count.get("isbn"):
                count = item_count.get("count")
                break
        # 调用的是gift下的book属性,不是外键
        # my_gift = SingleMygift(gift.id, SingleBookViewModel(gift.book), count)
        my_gift_wish = {
            "id": item.id,
            "book": SingleBookViewModel(item.book),
            "gifts_wishes_count": count
        }
        return my_gift_wish
