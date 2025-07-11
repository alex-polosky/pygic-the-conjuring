from dataclasses import dataclass, fields
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from typing import Any, Dict, ForwardRef, Tuple, Optional, Union, get_origin, get_args


class _ImmutableDict(dict):
    def __init__(self, has_init=True, *args, **kwargs):
        self.__has_init = has_init
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        if not getattr(self, '__has_init', False) and key not in self: dict.__setitem__(self, key, val)


def auto_convert_nested(cls):
    """Class decorator that adds automatic nested dataclass conversion."""
    original_init = cls.__init__

    def init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        if not getattr(cls, '__field_types', None):
            cls.__field_types = {k: v for k,v in {
                field.name: get_field_type(field.type)
                for field in fields(cls)
            }.items() if v}

        for field_name, field_type_container in cls.__field_types.items():
            field_type, field_container = field_type_container
            value = getattr(self, field_name, None)
            if not value:
                continue
            if field_container:
                if field_container in (dict, _ImmutableDict):
                    instance = field_container(**{field_type[0](k): field_type[1](v) for k,v in value.items()})
                elif hasattr(field_type, '__dataclass_fields__'):
                    field_names = [field.name for field in fields(field_type)]
                    instance = field_container([
                        field_type(**{
                            k:v
                            for k,v in item.items()
                            if k in field_names
                        })
                        for item in value
                    ])
                elif field_container in (set, tuple, list):
                    instance = field_container([x for x in value])
                else:
                    instance = field_container(value)
            elif field_type == date:
                instance = datetime.strptime(value, '%Y-%m-%d').date()
            elif field_type:
                if isinstance(value, dict):
                    instance = field_type(**value)
                elif hasattr(field_type, '__dataclass_fields__'):
                    field_names = [field.name for field in fields(field_type)]
                    instance = field_type(**{k:v for k,v in value.items() if k in field_names})
                else:
                    instance = field_type(value)
            else:
                instance = value
            object.__setattr__(self, field_name, instance)

    cls.__init__ = init
    return cls


def get_field_type(field_type: type[Any] | str | Any):
    container = None
    origin = get_origin(field_type)
    args = get_args(field_type)

    # Optional[T] -> T
    if origin is Union and len(args) == 2 and type(None) in args:
        actual_type = args[0] if args[1] is type(None) else args[1]
        return get_field_type(actual_type)

    # Dicts
    if origin in (_ImmutableDict, dict) and len(args) == 2:
        field_type = (args[0], args[1])
        container = origin

    # Tuple[T]
    if origin in (tuple, list, set) and len(args) == 1:
        field_type = args[0]
        container = origin

    # ForwardRef
    if type(field_type) is ForwardRef:
        if not field_type.__forward_evaluated__:
            field_type._evaluate(globals(), locals(), frozenset())
        field_type = field_type.__forward_value__

    # dataclass
    if hasattr(field_type, '__dataclass_fields__'):
        return (field_type, container)

    return (field_type, container)


@auto_convert_nested
@dataclass(frozen=True)
class Card:
    id: UUID
    '''A unique ID for this card in Scryfall's database'''
    lang: str
    '''A language code for this printing'''
    object: str
    '''A content type for this object, always card'''
    layout: str
    '''A computer-readable designation for this card's layout'''
    prints_search_uri: str
    '''A link to where you can begin paginating all re/prints for this card on Scryfall's API'''
    rulings_uri: str
    '''A link to this card's rulings list on Scryfall's API'''
    scryfall_uri: str
    '''A link to this card's permapage on Scryfall's website'''
    uri: str
    '''A link to this card object on Scryfall's API'''
    arena_id: Optional[int] = None
    '''This card's Arena ID, if any. A large percentage of cards are not available on Arena and do not have this ID'''
    mtgo_id: Optional[int] = None
    '''This card's Magic Online ID (also known as the Catalog ID), if any'''
    mtgo_foil_id: Optional[int] = None
    '''This card's foil Magic Online ID (also known as the Catalog ID), if any'''
    multiverse_ids: Optional[Tuple[int]] = None
    '''This card's multiverse IDs on Gatherer, if any'''
    tcgplayer_id: Optional[int] = None
    '''This card's ID on TCGplayer's API, also known as the productId'''
    tcgplayer_etched_id: Optional[int] = None
    '''This card's ID on TCGplayer's API, for its etched version if that version is a separate product'''
    cardmarket_id: Optional[int] = None
    '''This card's ID on Cardmarket's API, also known as the idProduct'''
    oracle_id: Optional[UUID] = None
    '''A unique ID for this card's Oracle identity'''
    reversible_card: Optional[bool] = None
    '''Whether this card is reversible'''


@auto_convert_nested
@dataclass(frozen=True)
class CardGameplay:
    color_identity: Tuple[str]
    '''This card's color identity'''
    keywords: Tuple[str]
    '''An array of keywords that this card has, such as 'Flying' and 'Cumulative upkeep' '''
    legalities: _ImmutableDict[str, str]
    '''An object describing the legality of this card across play formats'''
    name: str
    '''The name of this card. If this card has multiple faces, this field will contain both names separated by ␣//␣'''
    cmc: Optional[Decimal] = None
    '''The mana value of this card'''
    type_line: Optional[str] = None
    '''The type line of this card'''
    oracle_text: Optional[str] = None
    '''The Oracle text for this face, if any'''
    mana_cost: Optional[str] = None
    '''The mana cost for this face. This value will be any empty string "" if the cost is absent'''
    colors: Optional[Tuple[str]] = None
    '''This face's colors, if the game defines colors for the individual face of this card'''
    all_parts: Optional[Tuple['RelatedCard']] = None
    '''If this card is closely related to other cards, this property will be an array with Related Card Objects'''
    card_faces: Optional[Tuple['CardFace']] = None
    '''Card Face objects, if this card is multifaced'''
    color_indicator: Optional[Tuple[str]] = None
    '''The colors in this card's color indicator, if any. A null value for this field indicates the card does not have one'''
    defense: Optional[str] = None
    '''This card's defense, if any'''
    edhrec_rank: Optional[int] = None
    '''This card's overall rank/popularity on EDHREC'''
    game_changer: Optional[bool] = None
    '''Whether this card is on the Commander Game Changer list'''
    hand_modifier: Optional[str] = None
    '''This card's hand modifier, if it is Vanguard card'''
    life_modifier: Optional[str] = None
    '''This card's life modifier, if it is Vanguard card'''
    loyalty: Optional[str] = None
    '''This loyalty if any. Note that some cards have loyalties that are not numeric, such as X'''
    penny_rank: Optional[int] = None
    '''This card's rank in Penny Dreadful'''
    power: Optional[str] = None
    '''This card's power, if any. Note that some cards have powers that are not numeric, such as *'''
    produced_mana: Optional[Tuple[str]] = None
    '''Colors of mana that this card could produce'''
    reserved: Optional[bool] = None
    '''Whether this card is on the Reserved List'''
    toughness: Optional[str] = None
    '''This card's toughness, if any. Note that some cards have toughnesses that are not numeric, such as *'''


@auto_convert_nested
@dataclass(frozen=True)
class CardPrint:
    artist: str
    '''The name of the illustrator of this card'''
    booster: bool
    '''Whether this card is found in booster packs'''
    border_color: str
    '''The border color of this card: black, white, borderless, yellow, silver, or gold'''
    collector_number: str
    '''This card's collector number'''
    digital: bool
    '''Whether this card was only released in a video game'''
    finishes: Tuple[str]
    '''An array of computer-readable flags that indicate if this card can come in foil, nonfoil, or etched finishes'''
    frame: str
    '''This card's frame layout'''
    full_art: bool
    '''Whether this card has a full art treatment'''
    games: Tuple[str]
    '''A list of games that this card print is available in, paper, arena, and/or mtgo'''
    highres_image: bool
    '''Whether this card has a high-resolution image'''
    image_status: str
    '''A computer-readable indicator for the state of this card's image, one of missing, placeholder, lowres, or highres_scan'''
    oversized: bool
    '''Whether this card is oversized'''
    prices: _ImmutableDict[str, str]
    '''An object containing daily price information for this card'''
    rarity: str
    '''The rarity of this card: common, uncommon, rare, special, mythic, or bonus'''
    related_uris: _ImmutableDict[str, str]
    '''An object listing related pages for this card'''
    released_at: date
    '''The date this card was first released'''
    reprint: bool
    '''Whether this card is a reprint'''
    scryfall_set_uri: str
    '''A link to this card's set on Scryfall's API'''
    set_name: str
    '''This card's full set name'''
    set_search_uri: str
    '''A link to where you can begin paginating this card's set on the Scryfall API'''
    set_type: str
    '''The type of set this printing was released in'''
    set_uri: str
    '''A link to this card's set object on Scryfall's API'''
    set: str
    '''This card's set code'''
    set_id: UUID
    '''This card's Set ID on Scryfall'''
    story_spotlight: bool
    '''Whether this card is a Story Spotlight'''
    textless: bool
    '''Whether this card is textless'''
    variation: bool
    '''Whether this card is a variation of another printing'''
    artist_ids: Optional[Tuple[UUID]] = None
    '''The IDs of the artists that illustrated this card. Newly spoiled cards may not have this field yet'''
    attraction_lights: Optional[Tuple[int]] = None
    '''The lit attraction lights on this card, if any'''
    card_back_id: Optional[UUID] = None
    '''The ID of the card back design present on this card'''
    content_warning: Optional[bool] = None
    '''Whether this card requires a content warning'''
    flavor_name: Optional[str] = None
    '''The just-for-fun name printed on the card'''
    flavor_text: Optional[str] = None
    '''The flavor text, if any'''
    frame_effects: Optional[Tuple[str]] = None
    '''This card's frame effects, if any'''
    illustration_id: Optional[UUID] = None
    '''A unique identifier for the card artwork that remains consistent across reprints'''
    image_uris: Optional[_ImmutableDict[str, str]] = None
    '''An object listing available imagery for this card'''
    printed_name: Optional[str] = None
    '''The name on this card as originally printed'''
    printed_text: Optional[str] = None
    '''The text on this card as originally printed'''
    printed_type_line: Optional[str] = None
    '''The type line on this card as originally printed'''
    promo: Optional[bool] = None
    '''Whether this card is a promotional print'''
    promo_types: Optional[Tuple[str]] = None
    '''An array of strings describing what categories of promo cards this card falls into'''
    purchase_uris: Optional[_ImmutableDict[str, str]] = None
    '''An object containing links to this card's listing on major marketplaces'''
    variation_of: Optional[UUID] = None
    '''The ID of the card that this card is a variation of, if any'''
    security_stamp: Optional[str] = None
    '''The security stamp on this card, if any'''
    watermark: Optional[str] = None
    '''This card's watermark, if any'''
    preview: Optional['Preview'] = None
    '''An object describing the preview for this card, if any'''

@auto_convert_nested
@dataclass(frozen=True)
class CardFace:
    object: str
    '''A content type for this object, always card_face'''
    name: str
    '''The name of this particular face'''
    type_line: Optional[str] = None
    '''The type line of this particular face'''
    oracle_text: Optional[str] = None
    '''The Oracle text for this face, if any'''
    mana_cost: Optional[str] = None
    '''The mana cost for this face. This value will be any empty string "" if the cost is absent'''
    colors: Optional[Tuple[str]] = None
    '''This face's colors, if the game defines colors for the individual face of this card'''
    artist: Optional[str] = None
    '''The name of the illustrator of this card face. Newly spoiled cards may not have this field yet'''
    artist_id: Optional[UUID] = None
    '''The ID of the illustrator of this card face. Newly spoiled cards may not have this field yet'''
    cmc: Optional[Decimal] = None
    '''The mana value of this particular face, if the card is reversible'''
    color_indicator: Optional[Tuple[str]] = None
    '''The colors in this face's color indicator, if any'''
    defense: Optional[str] = None
    '''This face's defense, if any'''
    flavor_text: Optional[str] = None
    '''The flavor text, if any'''
    illustration_id: Optional[UUID] = None
    '''A unique identifier for the card face artwork that remains consistent across reprints'''
    image_uris: Optional[_ImmutableDict[str, str]] = None
    '''An object listing available imagery for this card face'''
    layout: Optional[str] = None
    '''The layout of this card face, if the card is reversible'''
    loyalty: Optional[str] = None
    '''This face's loyalty, if any'''
    oracle_id: Optional[UUID] = None
    '''A unique ID for this face's Oracle identity'''
    power: Optional[str] = None
    '''This face's power, if any. Note that some cards have powers that are not numeric, such as *'''
    printed_name: Optional[str] = None
    '''The name on this face as originally printed'''
    printed_text: Optional[str] = None
    '''The text on this face as originally printed'''
    printed_type_line: Optional[str] = None
    '''The type line on this face as originally printed'''
    toughness: Optional[str] = None
    '''This face's toughness, if any. Note that some cards have toughnesses that are not numeric, such as *'''
    watermark: Optional[str] = None
    '''This face's watermark, if any'''


@auto_convert_nested
@dataclass(frozen=True)
class RelatedCard:
    id: UUID
    '''An unique ID for this card in Scryfall's database'''
    object: str
    '''A content type for this object, always related_card'''
    component: str
    '''A field explaining what role this card plays in this relationship, one of token, meld_part, meld_result, or combo_piece'''
    name: str
    '''The name of this particular related card'''
    uri: str
    '''A URI where you can retrieve a full object describing this card on Scryfall's API'''
    type_line: Optional[str] = None
    '''The type line of this card'''


@auto_convert_nested
@dataclass(frozen=True)
class Preview:
    previewed_at: Optional[date] = None
    '''The date this card was previewed'''
    source_uri: Optional[str] = None
    '''A link to the preview for this card'''
    source: Optional[str] = None
    '''The name of the source that previewed this card'''


@dataclass(init=False, frozen=True)
class ScryfallCard(Card, CardGameplay, CardPrint):
    @classmethod
    def sub_classes(cls):
        return [
            c
            for c in cls.__mro__
            if c != cls and c != object and hasattr(c, '__dataclass_fields__')
        ]

    def __init__(self, **kwargs):
        known_fields = {f.name for f in fields(ScryfallCard)}
        filtered = {k:v for k,v in kwargs.items() if k in known_fields}
        for cls in self.sub_classes():
            field_objs = fields(cls)
            field_names = [field.name for field in field_objs]
            data = {k:v for k,v in filtered.items() if k in field_names}
            cls.__init__(self, **data)
