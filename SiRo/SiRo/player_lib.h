#ifndef PLAYER_LIB_H
#define PLAYER_LIB_H

ITEM player_current_weapon;
ITEM player_current_armor;

void renew_stats()
{
    player_atk = player_sp;
    if(weapon_on)
    {
        player_atk += player_current_weapon.get_atk();
    }
    player_def = player_tp;
    if(armor_on)
    {
        player_def += player_current_armor.get_def();
    }
    player_max_lp = player_tp * 2 + 10;
    if(player_lp > player_max_lp)
        player_lp = player_max_lp;
}

#endif // PLAYER_LIB_H
