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


#class ModelObjectBuilderBySinglePost(ModelObjectBuilder):
#    raise NotImplementedError


def model_object_builder_by_single_post_name():
    raise NotImplementedError


def populate_post_list_get_all_posts(reference_list):
    for a_file in reference_list.flatpages:
        if a_file.path.startswith(reference_list.application.config['BLOG_DIR']):
            reference_list.append(a_file)
    reference_list.sort(key=lambda item: item.meta['date'], reverse=True)


class PostList(list):
    def __init__(self, application, flatpages, criteria):
        super(PostList, self).__init__()
        self.application = application
        self.flatpages = flatpages
        self.criteria = criteria
        self._total_number_of_pages = 0
        self._total_post_count = 0

    def populate_post_list_get_all_posts(self):
        for a_file in self.flatpages:
            if a_file.path.startswith(self.application.config['BLOG_DIR']):
                self.append(a_file)
        self.sort(key=lambda item: item.meta['date'], reverse=True)

    def populate_post_list_get_single_post(self, post_slugname):
        pass

    def apply_paging(self):
        posts_per_page = self.application.config['HOME_PAGE_ARTICLES_PER_PAGE_COUNT']

        if self.criteria.page is None or self.criteria.page == 0:
            del self[posts_per_page:]
            return
        else:
            if self.criteria.page < 0:
                raise SystemError()
            if self.criteria.page > self._total_number_of_pages:
                raise SystemError()

            paging_offset = posts_per_page * self.criteria.page
            del self[paging_offset + posts_per_page:len(self)]
            del self[0:paging_offset]

    def calculate_total_pages(self):
        return int(self._total_post_count / self.application.config['HOME_PAGE_ARTICLES_PER_PAGE_COUNT']) + 1

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
