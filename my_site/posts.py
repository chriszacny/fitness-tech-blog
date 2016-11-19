class PostList(list):
    def __init__(self):
        super(PostList, self).__init__()

    @property
    def total_post_count(self):
        return len(self)


class Post:
    pass
