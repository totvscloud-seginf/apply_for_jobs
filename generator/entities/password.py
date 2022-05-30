class Password:
    def __init__(self, value, expiration_date, maximum_views, views):
        self.value = value
        self.expiration_date = expiration_date
        self.maximum_views = maximum_views
        self.views = views

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def expiration_date(self):
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, expiration_date):
        self.__expiration_date = expiration_date

    @property
    def maximum_views(self):
        return self.__maximum_views

    @maximum_views.setter
    def maximum_views(self, maximum_views):
        self.__maximum_views = maximum_views

    @property
    def views(self):
        return self.__views

    @views.setter
    def views(self, views):
        self.__views = views
