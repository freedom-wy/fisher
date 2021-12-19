def is_isbn_or_key(q):
    key_or_isbn = "key"
    if len(q) == 13 and q.isdigit():
        key_or_isbn = "isbn"
    short_q = q.replace('-', "")
    if len(q) == 10 and len(short_q) and short_q.isdigit():
        key_or_isbn = "isbn"
    return key_or_isbn
