from my_site import application
from my_site import flatpages
from abc import abstractmethod, ABCMeta


class PagingStrategies:
    ListViewPagingStrategy = 0
    SinglePostPagingStrategy = 1


class ListViewPagingStrategy:
    def apply_paging():
        pass


class SinglePostPagingStrategy:
    def apply_paging():
        pass


paging_strategies = {PagingStrategies.ListViewPagingStrategy: ListViewPagingStrategy(), PagingStrategies.SinglePostPagingStrategy: SinglePostPagingStrategy()}


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
        return PostList(application, flatpages, self.parsed_url_arguments, PagingStrategies.ListViewPagingStrategy)

    def population_method(self, model_object):
        model_object.populate_post_list_get_all_posts()

    def paging_hook(self, model_object):
        model_object.total_number_of_pages = model_object.calculate_total_pages()
        model_object.apply_paging()


class ModelObjectBuilderBySinglePost(ModelObjectBuilder):
    def __init__(self, post_data):
        self.post_data = post_data

    def initialize_model_object(self):
        criteria = ModelObjectBuilderCriteria()
        return PostList(application, flatpages, criteria, PagingStrategies.SinglePostPagingStrategy, 1)

    def population_method(self, model_object):
        model_object.populate_post_list_get_single_post(self.post_data)

    def paging_hook(self, model_object):
        model_object.total_number_of_pages = model_object.calculate_total_pages()
        model_object.apply_paging()


class ModelObjectBuilderCriteria:
    def __init__(self, page=0, tag=None, category=None):
        self.page = page
        self.tag = tag
        self.category = category


class PostList(list):
    def __init__(self, application, flatpages, criteria, paging_strategy_type, posts_per_page=None):
        super(PostList, self).__init__()
        self.application = application
        self.flatpages = flatpages
        self.criteria = criteria
        self._total_number_of_pages = 0
        self._total_post_count = 0
        self.paging_strategy_function = paging_strategies[paging_strategy_type]
        if not posts_per_page:
            self.posts_per_page = self.application.config['HOME_PAGE_ARTICLES_PER_PAGE_COUNT']
        else:
            self.posts_per_page = posts_per_page

    def populate_post_list_get_all_posts(self):
        for a_file in self.flatpages:
            if a_file.path.startswith(self.application.config['BLOG_DIR']):
                self.append(a_file)
        self.sort(key=lambda item: item.meta['date'], reverse=True)

    def populate_post_list_get_single_post(self, post):
        self.append(post)

    def apply_paging(self):
        if self.criteria.page is None or self.criteria.page == 0:
            del self[self.posts_per_page:]
            return
        else:
            if self.criteria.page < 0:
                raise SystemError()
            if self.criteria.page > self._total_number_of_pages:
                raise SystemError()

            paging_offset = self.posts_per_page * self.criteria.page
            del self[paging_offset + self.posts_per_page:len(self)]
            del self[0:paging_offset]

    def calculate_total_pages(self):
        return int(self._total_post_count / self.posts_per_page) + 1

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
