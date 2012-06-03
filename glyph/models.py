from glyph import db
from sqlalchemy.ext.declarative import declared_attr


# Ruler / Tablet many-to-many table
ruler_tablet = db.Table("ruler_tablet",
    db.Column("id",
        db.Integer(), primary_key=True),
    db.Column("ruler_id",
        db.Integer(), db.ForeignKey("ruler.id"), nullable=False),
    db.Column("tablet_id",
        db.Integer(), db.ForeignKey("tablet.id"), nullable=False))


# Sub-Period / Dynasty many-to-many table
subperiod_dynasty = db.Table("subperiod_dynasty",
    db.Column("id",
        db.Integer(), primary_key=True),
    db.Column("dynasty_id",
        db.Integer(), db.ForeignKey("dynasty.id"), nullable=False),
    db.Column("subperiod_id",
        db.Integer(), db.ForeignKey("sub_period.id"), nullable=False))


class GlyphMixin(object):
    """
    Provides some common attributes to our models
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}

    id =  db.Column(db.Integer, primary_key=True)


class Tablet(db.Model, GlyphMixin):
    museum_number = db.Column(
        db.String(75), nullable=False, unique=True)
    medium_id = db.Column(
        db.Integer(), db.ForeignKey('medium.id'), nullable=False)
    script_type_id = db.Column(
        db.Integer(), db.ForeignKey('script_type.id'), nullable=True)
    city_id = db.Column(
        db.Integer(), db.ForeignKey('city.id'), nullable=True)
    city_site_id = db.Column(
        db.Integer(), db.ForeignKey('city_site.id'), nullable=True)
    origin_city_id = db.Column(
        db.Integer(), db.ForeignKey('city.id'), nullable=True)
    publication = db.Column(
        db.String(200), nullable=True)
    period_id = db.Column(
        db.Integer(), db.ForeignKey('period.id'), nullable=False)
    sub_period_id = db.Column(
        db.Integer(), db.ForeignKey('sub_period.id'), nullable=True)
    from_id = db.Column(
        db.Integer(), db.ForeignKey('correspondent.id'), nullable=True)
    to_id = db.Column(
        db.Integer(), db.ForeignKey('correspondent.id'), nullable=True)
    language_id = db.Column(
        db.Integer(), db.ForeignKey('language.id'), nullable=True)
    year_id = db.Column(
        db.Integer(), db.ForeignKey('year.id'), nullable=True)
    month = db.Column(
        db.String(10), nullable=True)
    day = db.Column(
        db.String(10), nullable=True)
    dynasty_id = db.Column(
        db.Integer(), db.ForeignKey('dynasty.id'), nullable=True)
    text_vehicle_id = db.Column(
        db.Integer(), db.ForeignKey('text_vehicle.id'), nullable=True)
    locality_id = db.Column(
        db.Integer(), db.ForeignKey('locality.id'), nullable=True)
    sub_locality_id = db.Column(
        db.Integer(), db.ForeignKey('sub_locality.id'), nullable=True)
    notes = db.Column(
        db.String(500), nullable=True)
    method_id = db.Column(
        db.Integer(), db.ForeignKey('method.id'), nullable=True)
    genre_id = db.Column(
        db.Integer(), db.ForeignKey('genre.id'), nullable=True)
    function_id = db.Column(
        db.Integer(), db.ForeignKey('function.id'), nullable=True)
    # relations
    year = db.relationship("Year",
        backref="tablets")
    medium = db.relationship("Medium",
        backref="tablets")
    script_type = db.relationship("Script_Type",
        backref="tablets")
    locality = db.relationship("Locality",
        backref="tablets")
    sub_locality = db.relationship("Sub_Locality",
        backref="tablets")
    city = db.relationship("City", primaryjoin="City.id == Tablet.city_id",
        backref="tablets")
    city_site = db.relationship("City_Site",
        primaryjoin="City_Site.id == Tablet.city_site_id",
        backref="tablets")
    origin_city = db.relationship("City",
        primaryjoin="City.id == Tablet.origin_city_id",
        backref="origin_tablets")
    period = db.relationship("Period",
        backref="tablets")
    sub_period = db.relationship("Sub_Period",
        backref="tablets")
    sent_from = db.relationship("Correspondent",
        primaryjoin="Correspondent.id == Tablet.from_id",
        backref="tablets_from")
    sent_to = db.relationship("Correspondent",
        primaryjoin="Correspondent.id == Tablet.to_id",
        backref="tablets_to")
    text_vehicle = db.relationship("Text_Vehicle",
        backref="tablets")
    language = db.relationship("Language",
        backref="tablets")
    method = db.relationship("Method",
        backref="tablets")
    genre = db.relationship("Genre",
        backref="tablets")
    function = db.relationship("Function",
        backref="tablets")
    dynasty = db.relationship("Dynasty",
        backref="tablets")
    
    def __init__(self, **kwargs):
        """
        this will obviously fall over if you forget a required column:
        medium and period are both required
        """
        self.museum_number = kwargs.get("museum_number")
        self.medium = kwargs.get("medium")
        self.script_type = kwargs.get("script_type")
        self.locality = kwargs.get("locality")
        self.sub_locality = kwargs.get("sub_locality")
        self.city = kwargs.get("city")
        self.city_site = kwargs.get("city_site")
        self.origin_city = kwargs.get("origin_city")
        self.publication = kwargs.get("publication")
        self.period = kwargs.get("period")
        self.sub_period = kwargs.get("sub_period")
        self.sent_from = kwargs.get("sent_from")
        self.sent_to = kwargs.get("sent_to")
        self.year = kwargs.get("year")
        self.month = kwargs.get("month")
        self.day = kwargs.get("day")
        self.text_vehicle = kwargs.get("text_vehicle")
        self.notes = kwargs.get("notes")
        self.language = kwargs.get("language")
        self.method = kwargs.get("method")
        self.genre = kwargs.get("genre")
        self.function = kwargs.get("function")
        self.dynasty = kwargs.get("dynasty")
        self.rulers = kwargs.get("rulers")


class Non_Ruler_Corresp(db.Model, GlyphMixin):
    """
    This holds correspondents who aren't rulers
    """
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Correspondent(db.Model, GlyphMixin):
    """
    A correspondent can be a ruler or a non-ruler
    Note use of @property to return the correct value
    """
    ruler_id = db.Column(
        db.Integer(), db.ForeignKey("ruler.id"), nullable=True)
    non_ruler_id = db.Column(
        db.Integer, db.ForeignKey("non_ruler_corresp.id"), nullable=True)
    # relations
    ruler = db.relationship("Ruler",
        uselist=False, backref="correspondent")
    non_ruler = db.relationship("Non_Ruler_Corresp",
        uselist=False, backref="correspondent")

    def __init__(self, ruler=None, non_ruler=None):
        assert (ruler is None) ^ (non_ruler is None)
        if ruler:
            self.ruler = ruler
        if non_ruler:
            self.non_ruler = non_ruler

    @property
    def name(self):
        return self.ruler.name if self.ruler else self.non_ruler.name


class Locality(db.Model, GlyphMixin):
    area = db.Column(db.String(100), nullable=False, unique=True)
    # relations
    sub_localities = db.relationship("Sub_Locality", backref="locality")
    cities = db.relationship("City", backref="locality")

    def __init__(self, area, sub_localities=None):
        self.area = area
        if sub_localities:
            self.sub_localities = sub_localities


class Sub_Locality(db.Model, GlyphMixin):
    name = db.Column(db.String(100), nullable=False, unique=True)
    locality_id = db.Column(
        db.Integer(), db.ForeignKey("locality.id"), nullable=True)

    def __init__(self, name, locality):
        self.name = name
        self.locality = locality


class City(db.Model, GlyphMixin):
    name = db.Column(db.String(100), nullable=False, unique=True)
    locality_id = db.Column(
        db.Integer(), db.ForeignKey('locality.id'), nullable=True)
    # relations
    sites = db.relationship("City_Site", backref="city")

    def __init__(self, name, locality=None, sites=None):
        self.name = name
        if locality:
            self.locality = locality
        if sites:
            self.sites = sites


class City_Site(db.Model, GlyphMixin):
    name = db.Column(db.String(100), nullable=False, unique=True)
    city_id = db.Column(
        db.Integer(), db.ForeignKey("city.id"), nullable=False)

    def __init__(self, name, city):
        self.name = name
        self.city = city


class Method(db.Model, GlyphMixin):
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Script_Type(db.Model, GlyphMixin):
    script = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, script):
        self.script = script


class Year(db.Model, GlyphMixin):
    year = db.Column(db.String(14), nullable=False, unique=True)
    eponym_id = db.Column(
        db.Integer(), db.ForeignKey("eponym.id"), nullable=True)
    # relations
    eponym = db.relationship("Eponym", uselist=False, backref="year")

    def __init__(self, year, eponym=None):
        self.year = year
        if eponym:
            self.eponym = eponym


class Medium(db.Model, GlyphMixin):
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Genre(db.Model, GlyphMixin):
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Language(db.Model, GlyphMixin):
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Function(db.Model, GlyphMixin):
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Text_Vehicle(db.Model, GlyphMixin):
    name = db.Column(db.String(100), nullable=False, unique=True)
    bm_catalogue = db.Column(db.String(100), nullable=True)
    cdli = db.Column(db.String(100), nullable=True)

    def __init__(self, name, bm_catalogue=None, cdli=None):
        self.name = name
        if bm_catalogue:
            self.bm_catalogue = bm_catalogue
        if cdli:
            self.cdli = cdli


class Eponym(db.Model, GlyphMixin):
    """
    Like 'Year of Glad', but for rulers
    """
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name, year=None):
        self.name = name


class Period(db.Model, GlyphMixin):
    name = db.Column(db.String(150), nullable=False, unique=True)
    # should these be links to year?
    from_date = db.Column(db.String(50), nullable=False)
    to_date = db.Column(db.String(50), nullable=False)
    # relations
    sub_periods = db.relationship("Sub_Period", backref="period")
    rulers = db.relationship("Ruler", backref="period")

    def __init__(self, name, sub_period=None):
        self.name = name
        if sub_period:
            self.sub_period = sub_period


class Sub_Period(db.Model, GlyphMixin):
    name = db.Column(db.String(100), nullable=False, unique=True)
    period_id = db.Column(
        db.Integer(), db.ForeignKey("period.id"), nullable=False)
    # relations
    rulers = db.relationship("Ruler", backref="sub_period")

    def __init__(self, name, period):
        self.name = name
        self.period = period


class Ruler(db.Model, GlyphMixin):
    name = db.Column(db.String(100), nullable=False, unique=True)
    period_id = db.Column(
        db.Integer(), db.ForeignKey("period.id"), nullable=False)
    sub_period_id = db.Column(
        db.Integer(), db.ForeignKey("sub_period.id"), nullable=True)
    # relations
    dynasties = db.relationship("Ruler_Dynasty", backref="rulers")
    tablets = db.relationship(
        "Tablet", secondary=ruler_tablet, backref="rulers")

    def __init__(self,
        name, start_year=None, end_year=None,
        tablets=None, period=None, sub_period=None):

        self.name = name
        if start_year:
            self.start_year = start_year
        if end_year:
            self.end_year = end_year
        if tablets:
            self.tablets = tablets
        if period:
            self.period = period
        if sub_period:
            self.sub_period = sub_period


class Dynasty(db.Model, GlyphMixin):
    name = db.Column(db.String(100), nullable=False, unique=True)
    sub_periods = db.relationship(
        "Sub_Period", secondary=subperiod_dynasty, backref="dynasties")

    def __init__(self, name):
        self.name = name


class Ruler_Dynasty(db.Model, GlyphMixin):
    """
    This is an association object linking Rulers and Dynasties
    It also includes a rim_ref column for each ruler/dynasty combo
    and start and end years
    """
    ruler_id = db.Column(
        db.Integer(), db.ForeignKey("ruler.id"), nullable=False)
    dynasty_id = db.Column(
        db.Integer(), db.ForeignKey("dynasty.id"), nullable=False)
    rim_ref = db.Column(db.String(75), nullable=False, unique=True)
    start_year_id = db.Column(
        db.Integer(), db.ForeignKey("year.id"), nullable=True)
    end_year_id = db.Column(
        db.Integer(), db.ForeignKey("year.id"), nullable=True)
    end_year_id
    # relations
    dynasty = db.relationship("Dynasty", backref="ruler_dynasties")
    start_year = db.relationship("Year",
        primaryjoin="Year.id == Ruler_Dynasty.start_year_id",
        backref="dynasty_start_years")
    end_year = db.relationship("Year",
        primaryjoin="Year.id == Ruler_Dynasty.end_year_id",
        backref="dynasty_end_years")

    def __init__(self, rim_ref, dynasty=None):
        self.rim_ref = rim_ref
        if dynasty:
            self.dynasty = Dynasty(dynasty)
