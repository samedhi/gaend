from google.appengine.ext import ndb


class GaendModel(ndb.Model):
    """The Base class that all `gaend` Models inherit from"""
    pass


class GaendWriteMixin():
    """Mixin class indicating this model should have write endpoints created

    Inheriting from this class means that gaend.routes will automatically
    create REST HTTP JSON endpoints for POST, PUT, & DELETE for this class"""
    pass


class GaendReadMixin():
    """Mixin class indicating this model should have a read endpoint created

    Inheriting from this class means that gaend.routes will automatically
    create REST HTTP JSON endpoints for this class"""
    pass


class GaendFullModel(GaendModel, GaendWriteMixin, GaendReadMixin):
    """Abstract class indicating this model will have all endpoints created

    Inheriting from this class means that the handlers in gaend.routes will
    automatically create REST HTTP JSON endpoints for this model."""
    pass
