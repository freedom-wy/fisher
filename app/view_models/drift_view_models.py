from app.libs.enums import PendingStatus


class DriftInfo(object):
    def __init__(self, user):
        self.nickname = user.nickname
        self.beans = user.beans
        self.email = user.email
        self.send_counter = user.send_counter
        self.receive_counter = user.receive_counter
        self.send_receive = self.handle_send_recive()

    def handle_send_recive(self):
        return "{send_counter}/{receive_counter}".format(send_counter=self.send_counter,
                                                         receive_counter=self.receive_counter)


class DriftViewModel(object):
    def __init__(self, drift, current_user_id):
        self.data = self.__parse(drift, current_user_id)

    def __parse(self, drift, current_user_id):
        """
        处理drift数据
        :param drift:
        :param current_user_id:
        :return:
        """
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.status, you_are)
        r = {
            "you_are": you_are,
            "drift_id": drift.id,
            "book_title": drift.book_title,
            "book_author": drift.book_author,
            "book_img": drift.book_img,
            "date": drift.create_datetime.strftime("%Y-%m-%d"),
            "operator": drift.requester_nickname if you_are != "requester" else drift.gifter_nickname,
            "message": drift.message,
            "address": drift.address,
            # 收件人姓名
            "recipient_name": drift.recipient_name,
            "mobile": drift.mobile,
            "status": drift.status,
            "status_str": pending_status
        }
        return r

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        """
        判断当前用户是请求者还是赠送者
        :param drift:
        :param current_user_id:
        :return:
        """
        you_are = "requester"
        if current_user_id == drift.gifter_id:
            you_are = "gifter"
        return you_are


class DriftCollection(object):
    def __init__(self, drifts, current_user_id):
        self.data = self.__parse(drifts, current_user_id)

    @staticmethod
    def __parse(drifts, current_user_id):
        temp = []
        for drift in drifts:
            temp.append(DriftViewModel(drift, current_user_id).data)
        return temp
