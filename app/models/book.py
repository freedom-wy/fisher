from sqlalchemy import Column, Integer, String


class Book():
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default="佚名")
    # 精装
    binding = Column(String(20))
    # 出版社
    publisher = Column(String(50))
    pages = Column(Integer)
    pubdate = Column(String(20))
    # unique 该字段不重复
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
