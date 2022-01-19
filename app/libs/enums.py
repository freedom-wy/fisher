from enum import Enum


class PendingStatus(Enum):
    """
    枚举
    交易的4种状态
    """
    # 等待
    Waiting = 1
    # 成功
    Success = 2
    # 拒绝
    Reject = 3
    # 撤销
    Redraw = 4

    @classmethod
    def pending_str(cls, status, key):
        """

        :param status: 对应1,2,3,4
        :param key: 对应requester和gifter
        :return:
        """
        key_map = {
            cls.Waiting: {
                "requester": "等待对方邮寄",
                "gifter": "等待你邮寄"
            },
            cls.Success: {
                "requester": "对方已邮寄",
                "gifter": "你已邮寄,交易完成"
            },
            cls.Reject: {
                "requester": "对方已拒绝",
                "gifter": "你已拒绝"
            },
            cls.Redraw: {
                "requester": "你已撤销",
                "gifter": "对方已撤销"
            }
        }
        return key_map[status][key]

