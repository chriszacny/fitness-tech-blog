from abc import abstractmethod, ABCMeta
from my_site import application
from my_site import flatpages


class Post:
    def __init__(self, post_data):
        self.data = post_data


class ModelObject:
    def __init__(self, page=0):
        self.paging = Paging()


class Paging:
    pass


class SummaryModelObject(ModelObject):
    def __init__(self, page=0):
        super(SummaryModelObject, self).__init__(page)


class SingleBlogPostModelObject(ModelObject):
    def __init__(self, slugname):
        super(SingleBlogPostModelObject, self).__init__()
        self.post_data = get_post_by_slugname(slugname)
        self.post = Post(self.post_data)


def get_post_by_slugname(name):
    path = '{}/{}'.format(application.config['BLOG_DIR'], name)
    post = flatpages.get_or_404(path)
    return post
