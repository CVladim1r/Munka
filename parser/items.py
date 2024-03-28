from scrapy.item import Item, Field

class SpecItem(Item):
    spec = Field()
    SpecName = Field()


class GtudataItem(Item):
    family = Field()
    name = Field()
    surname = Field()
    spec = Field()
    ball = Field()
    url = Field()
    pagespec = Field()