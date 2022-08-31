"""
MIT License

Copyright (c) 2022-present Baptiste#4040 (Discord)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
#This code is largerly inspired by discord.py, Rapptz
#https://github.com/Rapptz/discord.py


from __future__ import annotations

from typing import Callable, Any, Dict, List, Type, TypeVar
from .flags import BaseFlags, flag_value, fill_with_flags, alias_flag_value

__all__ = (
    'Permissions',
)

# A permission alias works like a regular flag but is marked
# So the PermissionOverwrite knows to work with it
class permission_alias(alias_flag_value):
    alias: str


def make_permission_alias(alias: str) -> Callable[[Callable[[Any], int]], permission_alias]:
    def decorator(func: Callable[[Any], int]) -> permission_alias:
        ret = permission_alias(func)
        ret.alias = alias
        return ret

    return decorator

P = TypeVar('P', bound='Permissions')

@fill_with_flags()
class Permissions(BaseFlags):
    """Wraps up the Taho permission value.

    The properties provided are two way. You can set and retrieve individual
    bits using the properties as if they were regular bools. This allows
    you to edit permissions.

    .. container:: operations

        .. describe:: x == y

            Checks if two permissions are equal.
        .. describe:: x != y

            Checks if two permissions are not equal.
        .. describe:: x <= y

            Checks if a permission is a subset of another permission.
        .. describe:: x >= y

            Checks if a permission is a superset of another permission.
        .. describe:: x < y

             Checks if a permission is a strict subset of another permission.
        .. describe:: x > y

             Checks if a permission is a strict superset of another permission.
        .. describe:: hash(x)

               Return the permission's hash.
        .. describe:: iter(x)

               Returns an iterator of ``(perm, value)`` pairs. This allows it
               to be, for example, constructed as a dict or a list of pairs.
               Note that aliases are not shown.

    Attributes
    -----------
    value: :class:`int`
        The raw value. This value is a bit array field of a 53-bit integer
        representing the currently available permissions. You should query
        permissions via the properties rather than using this raw value.
    """

    __slots__ = ()

    def __init__(self, permissions: int = 0, **kwargs: bool):
        if not isinstance(permissions, int):
            raise TypeError(f'Expected int parameter, received {permissions.__class__.__name__} instead.')

        self.value = permissions
        for key, value in kwargs.items():
            if key not in self.VALID_FLAGS:
                raise TypeError(f'{key!r} is not a valid permission name.')
            setattr(self, key, value)

    def is_subset(self, other: Permissions) -> bool:
        """Returns ``True`` if self has the same or fewer permissions as other."""
        if isinstance(other, Permissions):
            return (self.value & other.value) == self.value
        else:
            raise TypeError(f"cannot compare {self.__class__.__name__} with {other.__class__.__name__}")

    def is_superset(self, other: Permissions) -> bool:
        """Returns ``True`` if self has the same or more permissions as other."""
        if isinstance(other, Permissions):
            return (self.value | other.value) == self.value
        else:
            raise TypeError(f"cannot compare {self.__class__.__name__} with {other.__class__.__name__}")

    def is_strict_subset(self, other: Permissions) -> bool:
        """Returns ``True`` if the permissions on other are a strict subset of those on self."""
        return self.is_subset(other) and self != other

    def is_strict_superset(self, other: Permissions) -> bool:
        """Returns ``True`` if the permissions on other are a strict superset of those on self."""
        return self.is_superset(other) and self != other

    __le__ = is_subset
    __ge__ = is_superset
    __lt__ = is_strict_subset
    __gt__ = is_strict_superset

    @classmethod
    def none(cls: Type[P]) -> P:
        """A factory method that creates a :class:`Permissions` with all
        permissions set to ``False``."""
        return cls(0)

    @classmethod
    def all(cls: Type[P]) -> P:
        """A factory method that creates a :class:`Permissions` with all
        permissions set to ``True``.
        """
        return cls(0b111111111111111111111111111111111111111)


    @classmethod
    def general(cls: Type[P]) -> P:
        """A factory method that creates a :class:`Permissions` with all
        "General" permissions set to ``True``. The guild-specific
        permissions are currently:

        - :attr:`open_inventory`
        - :attr:`item_use`
        - :attr:`item_dump`
        - :attr:`craft_use`
        - :attr:`money_use`
        - :attr:`item_reload`
        - :attr:`hotbar_use`
        - :attr:`shop_buy`
        - :attr:`trade`
        - :attr:`pvp`
        - :attr:`job_exercise`
        - :attr:`sheets_create`
        - :attr:`roll`
        """
        return cls(0b00000000000000000001111111111111)
    
    @classmethod
    def all_information(cls: Type[P]) -> P:
        """A :class:`Permissions` with all information-specific permissions set to
        ``True`` and the guild-specific ones set to ``False``. The guild-specific
        permissions are currently:

        - :attr:`job_information`
        - :attr:`player_information`
        - :attr:`item_information`
        - :attr:`class_information`
        - :attr:`stat_information`
        - :attr:`account_information`
        - :attr:`bank_information`
        """
        return cls(0b00000000011111110000000000000000)

    @classmethod
    def roleplay_participation(cls: Type[P]) -> P:
        """A factory method that creates a :class:`Permissions` with all
        "Roleplay participation" permissions set to ``True``. The guild-specific
        permissions are currently:

        - :attr:`manage_npc`
        - :attr:`manage_shop`
        - :attr:`manage_account`
        """
        return cls(0b00000000000000001110000000000000)

    @classmethod
    def roleplay_configuration(cls: Type[P]) -> P:
        """A factory method that creates a :class:`Permissions` with all
        "Roleplay configuration" permissions set to ``True``. The guild-specific
        permissions are currently:

        - :attr:`manage_job`
        - :attr:`manage_item`
        - :attr:`manage_class`
        - :attr:`manage_stat`
        - :attr:`manage_bank`
        - :attr:`manage_admin_shop`
        - :attr:`manage_craft`
        - :attr:`manage_currency`
        """
        return cls(0b111000000001111100000000000000000000000)

    @classmethod
    def advanced_roleplay_configuration(cls: Type[P]) -> P:
        """A factory method that creates a :class:`Permissions` with all
        "Advanced Roleplay configuration" permissions set to ``True``. The guild-specific
        permissions are currently:

        - :attr:`sheets_configure`
        - :attr:`roleplay_configure`
        - :attr:`inventory_configure`
        - :attr:`roleplay_role_give`
        - :attr:`stat_give`
        - :attr:`player_reset`
        - :attr:`money_manage`
        """
        return cls(0b101111110000000000000000000000000000)


    def update(self, **kwargs: bool) -> None:
        r"""Bulk updates this permission object.

        Allows you to set multiple attributes by using keyword
        arguments. The names must be equivalent to the properties
        listed. Extraneous key/value pairs will be silently ignored.

        Parameters
        ------------
        \*\*kwargs
            A list of key/value pairs to bulk update permissions with.
        """
        for key, value in kwargs.items():
            if key in self.VALID_FLAGS:
                setattr(self, key, value)

    def handle_overwrite(self, allow: int, deny: int) -> None:
        # Basically this is what's happening here.
        # We have an original bit array, e.g. 1010
        # Then we have another bit array that is 'denied', e.g. 1111
        # And then we have the last one which is 'allowed', e.g. 0101
        # We want original OP denied to end up resulting in
        # whatever is in denied to be set to 0.
        # So 1010 OP 1111 -> 0000
        # Then we take this value and look at the allowed values.
        # And whatever is allowed is set to 1.
        # So 0000 OP2 0101 -> 0101
        # The OP is base  & ~denied.
        # The OP2 is base | allowed.
        self.value = (self.value & ~deny) | allow

    @flag_value
    def open_inventory(self) -> int:
        """:class:`bool`: Returns ``True`` if the player can open his inventory."""
        return 1 << 0

    @flag_value
    def item_use(self) -> int:
        """:class:`bool`: Returns ``True`` if the player can use items."""
        return 1 << 1

    @flag_value
    def item_dump(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can dump items (trash)."""
        return 1 << 2

    @flag_value
    def craft_do(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can do crafts."""
        return 1 << 3

    @flag_value
    def money_use(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can use his money. This includes deposit, withdraw, check his balance or pay other players."""
        return 1 << 4

    @flag_value
    def item_reload(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can reload items from his hotbar (if the item have the ammunition and the charger size properties defined)."""
        return 1 << 5

    @flag_value
    def hotbar_use(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can use his hotbar. This includes setting and removing items of/from the hotbar."""
        return 1 << 6

    @flag_value
    def shop_buy(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can buy this from the shops. This also includes the permission to see the shops."""
        return 1 << 7

    @flag_value
    def trade(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can trade with other players."""
        return 1 << 8

    @flag_value
    def pvp(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can attack other players."""
        return 1 << 9

    @flag_value
    def job_exercise(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can exercice his works."""
        return 1 << 10

    @flag_value
    def sheet_create(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can create his roleplay sheet."""
        return 1 << 11

    @flag_value
    def roll(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can use the roll command."""
        return 1 << 12

    @flag_value
    def manage_npc(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage a NPC.

        """
        return 1 << 13

    @flag_value
    def manage_shop(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage a shop. It is for player's shops, not for admin shops."""
        return 1 << 14

    @flag_value
    def manage_account(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can open an account in a bank."""
        return 1 << 15

    @flag_value
    def job_information(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can see information about the guild's jobs."""
        return 1 << 16

    @flag_value
    def player_information(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can see information about the guild's players."""
        return 1 << 17

    @flag_value
    def item_information(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can see information about the guild's items."""
        return 1 << 18

    @flag_value
    def class_information(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can see information about the guild's classes."""
        return 1 << 19

    @flag_value
    def stat_information(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can see information about the guild's stats."""
        return 1 << 20

    @flag_value
    def account_information(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can see information about the guild's accounts."""
        return 1 << 21

    @flag_value
    def bank_information(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can see information about the guild's banks."""
        return 1 << 22

    @flag_value
    def manage_job(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage jobs."""
        return 1 << 23

    @flag_value
    def manage_item(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage items."""
        return 1 << 24

    @flag_value
    def manage_class(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage classes."""
        return 1 << 25

    @flag_value
    def manage_stat(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage stats."""
        return 1 << 26

    @flag_value
    def manage_bank(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage banks."""
        return 1 << 27

    @flag_value
    def manage_admin_shop(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage admin shops (different of player shops, in admin shop you can have unlimited quantities)."""
        return 1 << 36
    
    @flag_value
    def manage_craft(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage crafts."""
        return 1 << 37
    
    @flag_value
    def manage_currency(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage currencies."""
        return 1 << 38

    @flag_value
    def sheet_configure(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can configure roleplay sheets."""
        return 1 << 28

    @flag_value
    def roleplay_configure(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can configure the roleplay (default money, ko life, rp channels, rp roles...)."""
        return 1 << 29

    @flag_value
    def inventory_manage(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage inventories. This includes giving items and removing items from other players' inventories."""
        return 1 << 30

    @flag_value
    def roleplay_role_give(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can add or remove roleplay configured roles from players."""
        return 1 << 31

    @flag_value
    def stat_give(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can add or remove stats from players."""
        return 1 << 32

    @flag_value
    def player_reset(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can reset other players. This excludes resetting all players, which is an owner-only permission."""
        return 1 << 33

    @flag_value
    def money_manage(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can manage money of other players. This includes giving and removing."""
        return 1 << 35

    @flag_value
    def bot_configuration(self) -> int:
        """:class:`bool`: Returns ``True`` if a player can configure the bot. This includes basic bot settings, such as prefix, language, etc."""
        return 1 << 34
    
    @make_permission_alias('bot_configuration')
    def bot_config(self) -> int:
        """:class:`bool`: An alias for :attr:`bot_configuration`.
        """
        return 1 << 34
    
    @property
    def list(self) -> List[int]:
        return list(dict.fromkeys([int(getattr(Permissions, f).flag) for f in self.VALID_FLAGS.keys() if getattr(self, f)]))

    
    def to_dict(self) -> Dict[str, bool]:
        response = {f:getattr(self, f) for f in self.VALID_FLAGS.keys().__reversed__()}
        response.update({
            "value": self.value,
            "list": ",".join((str(f) for f in self.list)),
        })
        return response

