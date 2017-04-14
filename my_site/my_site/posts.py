from my_site import application
from my_site import flatpages
from abc import abstractmethod, ABCMeta


class ModelObjectBuilder(metaclass=ABCMeta):
    def builder_template_method(self):
        model_object = self.initialize_model_object()
        self.population_method(model_object)
        self.set_total_post_count(model_object)
        self.paging_hook(model_object)
        return model_object

    @abstractmethod
    def initialize_model_object(self):
        pass

    @abstractmethod
    def population_method(self, model_object):
        pass

    def set_total_post_count(self, model_object):
        model_object.total_post_count = len(model_object)

    def paging_hook(self, model_object):
        pass


class ModelObjectBuilderByCriteria(ModelObjectBuilder):
    def __init__(self, parsed_url_arguments):
        self.parsed_url_arguments = parsed_url_arguments

    def initialize_model_object(self):
        return PostList(application, flatpages, self.parsed_url_arguments)

    def population_method(self, model_object):
        model_object.populate_post_list_get_all_posts()

    def paging_hook(self, model_object):
        model_object.total_number_of_pages = model_object.calculate_total_pages()
        model_object.apply_paging()


class ModelObjectBuilderBySinglePost(ModelObjectBuilder):
    def __init__(self, post_data):
        self.post_data = post_data

    def initialize_model_object(self):
        criteria = ModelObjectBuilderCriteria(posts_per_page=1)
        return PostList(application, flatpages, criteria)

    def population_method(self, model_object):
        model_object.populate_post_list_get_single_post(self.post_data)

    def paging_hook(self, model_object):
        model_object.total_number_of_pages = model_object.calculate_total_pages()
        model_object.apply_paging()


class ModelObjectBuilderCriteria:
    def __init__(self, page=0, tag=None, category=None, posts_per_page=None):
        self.page = page
        self.tag = tag
        self.category = category
        if not posts_per_page:
            self.posts_per_page = application.config['HOME_PAGE_ARTICLES_PER_PAGE_COUNT']
        else:
            self.posts_per_page = posts_per_page


class Post:
    def __init__(self, next_post, previous_post, data):
        self.data = data
        self.next_post = next_post
        self.previous_post = previous_post

    def __repr__(self):
        next_post_name = ''
        previous_post_name = ''
        current_post_name = self.data.meta['slugname']
        if self.next_post is not None:
            next_post_name = self.next_post.data.meta['slugname']
        if self.previous_post is not None:
            previous_post_name = self.previous_post.data.meta['slugname']
        print('Post name: {}. Previous post: {}. Next post: {}'.format(current_post_name, next_post_name, previous_post_name))


class PostList(list):
    def __init__(self, application, flatpages, criteria):
        super(PostList, self).__init__()
        self.application = application
        self.flatpages = flatpages
        self.criteria = criteria
        self._total_number_of_pages = 0
        self._total_post_count = 0

    """
    def __repr__(self):
        for a_post in self:
            print(a_post)
    """

    def populate_post_list_get_all_posts(self):
        current_post = None
        previous_post = None
        for a_file in self.flatpages:
            if a_file.path.startswith(self.application.config['BLOG_DIR']):
                current_post = Post(None, previous_post, a_file)
                if previous_post is not None:
                    previous_post.next_post = current_post
                previous_post = current_post
                self.append(current_post)
        self.sort(key=lambda item: item.data.meta['date'], reverse=True)
        if self is not None:
            print(self)


    def populate_post_list_get_single_post(self, post_data):
        self.populate_post_list_get_all_posts()
        post_to_find = None
        for a_post in self:
            if a_post.data.meta['slugname'] == post_data.meta['slugname']:
                post_to_find = a_post
        self[:] = []
        self.append(post_to_find)

    def apply_paging(self):
        if self.criteria.page is None or self.criteria.page == 0:
            del self[self.criteria.posts_per_page:]
            return
        else:
            if self.criteria.page < 0:
                raise SystemError()
            if self.criteria.page > self._total_number_of_pages:
                raise SystemError()

            paging_offset = self.criteria.posts_per_page * self.criteria.page
            del self[paging_offset + self.criteria.posts_per_page:len(self)]
            del self[0:paging_offset]

    def calculate_total_pages(self):
        return int(self._total_post_count / self.criteria.posts_per_page) + 1

    @property
    def total_number_of_pages(self):
        return self._total_number_of_pages

    @total_number_of_pages.setter
    def total_number_of_pages(self, value):
        self._total_number_of_pages = value

    @property
    def total_post_count(self):
        return self._total_post_count

    @total_post_count.setter
    def total_post_count(self, value):
        self._total_post_count = value

    @property
    def has_previous_page(self):
        if self.criteria.page > 0:
            return True
        return False

    @property
    def has_next_page(self):
        if self.criteria.page < self.total_number_of_pages - 1:
            return True
        return False

    @property
    def previous_page_number(self):
        return self.criteria.page - 1

    @property
    def next_page_number(self):
        return self.criteria.page + 1

    @property
    def posts_per_page(self):
        return self.criteria.posts_per_page
