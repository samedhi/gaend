from google.appengine.ext import ndb


class Gaend():
    """The Base class that all `gaend` Models inherit from"""
    pass


class GaendWriteMixin(Gaend):
    """Mixin class indicating this model should have write endpoints created

    Inheriting from this class means that gaend.routes will automatically
    create REST HTTP JSON endpoints for POST, PUT, & DELETE for this class"""
    pass


class GaendReadMixin(Gaend):
    """Mixin class indicating this model should have a read endpoint created

    Inheriting from this class means that gaend.routes will automatically
    create REST HTTP JSON endpoints for this class"""
    pass


class GaendFullMixin(Gaend, GaendWriteMixin, GaendReadMixin):
    """Mixin class indicating this model should have all endpoints created

    Inheriting from this class means that gaend.routes will automatically
    create all REST HTTP JSON endpoints for this class"""
    pass


class GaendFullModel(ndb.Model, GaendFullMixin):
    """Abstract class indicating this model will have all endpoints created"""
    pass
