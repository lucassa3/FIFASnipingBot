from model.actions import (
    select_textbox_filter,
    input_name,
    select_filter,
    cancel_filter,
)


class Filter:
    def __init__(
        self,
        name="",
        quality="",
        rarity="",
        chem_style="",
        league="",
        position="",
        nation="",
        club="",
        min_bid=0,
        max_bid=0,
        min_price=0,
        max_price=0,
        consumable_type="",
        chem_type="",
    ):
        self.name = name
        self.quality = quality
        self.rarity = rarity
        self.chem_style = chem_style
        self.league = league
        self.position = position
        self.nation = nation
        self.club = club
        self.min_bid = min_bid
        self.max_bid = max_bid
        self.min_price = min_price
        self.max_price = max_price
        self.consumable_type = consumable_type
        self.chem_type = chem_type

        self.textbox_fields = {"min_bid", "max_bid", "min_price", "max_price"}

    def update(self, d, **kwargs):
        for key in kwargs:
            if key in self.__dict__:
                if self.__dict__[key] != kwargs[key][1]:
                    if key in self.textbox_fields:
                        if kwargs[key][1]:
                            select_textbox_filter(d, kwargs[key][0], kwargs[key][1])
                    elif key == "name":
                        if kwargs[key][1]:
                            input_name(d, kwargs[key][1])
                    else:
                        if kwargs[key][1]:
                            select_filter(d, kwargs[key][0], kwargs[key][1])
                        else:
                            cancel_filter(d, self.__dict__[key])
                    setattr(self, key, kwargs[key][1])
            else:
                raise ValueError(
                    f"tried to modify filter {key}, but this filter does not exist!"
                )
