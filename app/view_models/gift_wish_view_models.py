from app.models.user import User


class TradeInfo(object):
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    @staticmethod
    def __map_to_trade(single):
        """

        :param single: 单个gift或wish
        :return:
        """
        if single.create_datetime:
            time = single.create_datetime.strftime("%Y-%m-%d")
        else:
            time = "未知"
        return dict(
            user_name=User.query.filter_by(id=single.uid).first().nickname,
            time=time,
            id=single.id
        )
