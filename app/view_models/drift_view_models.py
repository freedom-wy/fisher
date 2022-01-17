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
