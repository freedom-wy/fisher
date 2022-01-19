from urllib.parse import urlparse


def split_url(url1, url2):
    split_url1 = urlparse(url1)
    split_url2 = urlparse(url2)
    if split_url1.netloc == split_url2.netloc:
        return True


if __name__ == '__main__':
    split_url("https://www.baidu.com", "https://www.google.com")
