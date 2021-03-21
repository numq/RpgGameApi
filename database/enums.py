import enum


class CharacterState(enum.IntEnum):
    IDLE = 0
    ACTIVE = 1


class NpcType(enum.Enum):
    FRIENDLY = 'FRIENDLY'
    NEUTRAL = 'NEUTRAL'
    AGRESSIVE = 'AGRESSIVE'


class AbilityElement(enum.Enum):
    FIRE = 'FIRE'
    ICE = 'ICE'


class EffectType(enum.Enum):
    DISABLE = 'DISABLE'
    HEAL = 'HEAL'
    DAMAGE = 'DAMAGE'


class ItemType(enum.IntEnum):
    WEAPON_RANGE = 0
    WEAPON_MAGIC = 1
    WEAPON_MELEE = 2
    RING = 3
    BODY = 4
    HEAD = 5
    BOOT = 6


class ItemRarity(enum.IntEnum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    LEGENDARY = 3
