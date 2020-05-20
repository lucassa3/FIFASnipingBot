class Card:
    def __init__(self, elem):
        self.elem=elem

        inner_elem = elem.find_element_by_class_name("entityContainer")
        
        self.name = inner_elem.find_element_by_class_name("name").text
        self.idx = elem.id


class Player(Card):
    def __init__(self, elem):
        super().__init__(elem_id, name, card_type)
        
        overview_elem = .find_element_by_class_name("entityContainer") \
            .find_element_by_class_name("playerOverview")
        
        self.ovr = overview_elem.find_element_by_class_name("rating")
        self.position = overview_elem.find_element_by_class_name("position")


def card_builder(elem):
    if len(elem.find_elements_by_class_name("player-stats-data-component")) > 0:
        return Player(elem)
    return Card(elem)
