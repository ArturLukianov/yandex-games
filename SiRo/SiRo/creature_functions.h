#ifndef CREATURE_FUNCTIONS_H
#define CREATURE_FUNCTIONS_H

std::map<int,CREATURE>creature_base;
int m_base_id = 1;

int put_creature_to_map(CREATURE creature, int x, int y)
{
    if(m_base_id > 10000)m_base_id = 1;
    if(x > 0 && y > 0 && x < SCREEN_SYMW && y < SCREEN_SYMH && npc_field[y][x] == 0 && field[y][x] != 1)
    {
        npc_field[y][x] = m_base_id;
        creature_base[m_base_id] = creature;
        return m_base_id++;
    }
    return -1;
}

#endif // CREATURE_FUNCTIONS_H
