#ifndef CREATURE_LIB_H
#define CREATURE_LIB_H

class CREATURE_STAMP
{
public:
    int creature_hp;
    int creature_atk;
    int creature_lvl;
    int creature_rep;
    int creature_spd;
    std::vector<int>creature_drop;
    char creature_sym;
    std::string creature_name;
    int drop_chance;
    CREATURE_STAMP(std::string name,int hp,int atk,int spd,int lvl,int rep,std::vector<int>drops,char sym,int chance)
    {
        creature_name = name;
        creature_hp = hp;
        creature_atk = atk;
        creature_lvl = lvl;
        creature_rep = rep;
        creature_sym = sym;
        creature_spd = spd;
        creature_drop.assign(drops.begin(),drops.end());
        drop_chance = chance;
    }
    CREATURE_STAMP()
    {

    }
};

class CREATURE
{
    int creature_hp;
    int creature_atk;
    int creature_lvl;
    int creature_rep;
    int creature_x;
    int creature_y;
    int t_rng;
    int drop_chance;
    int creature_spd;
    char creature_type;
    ITEM creature_drop;
    bool c_empty = 0;
    std::string creature_name;
public:
    CREATURE(std::string name,int hp,int atk,int spd,int lvl,int rep,int x,int y,ITEM drop,char type,int chance)
    {
        t_rng = std::rand() % 5;
        creature_name = name;
        creature_hp = hp;
        creature_atk = atk;
        creature_lvl = lvl;
        creature_rep = rep;
        creature_spd = spd;
        creature_x = x;
        creature_y = y;
        creature_drop = drop;
        creature_type = type;
        drop_chance = chance;
        c_empty = false;
    }

    CREATURE(CREATURE_STAMP creature_stamp,int x,int y,ITEM drop)
    {
        t_rng = std::rand() % 5;
        creature_name = creature_stamp.creature_name;
        creature_hp = creature_stamp.creature_hp;
        creature_atk = creature_stamp.creature_atk;
        creature_spd = creature_stamp.creature_spd;
        creature_lvl = creature_stamp.creature_lvl;
        creature_rep = creature_stamp.creature_rep;
        creature_x = x;
        creature_y = y;
        creature_drop = drop;
        creature_type = creature_stamp.creature_sym;
        drop_chance = creature_stamp.drop_chance;
        c_empty = false;
    }

    CREATURE()
    {
        c_empty = true;
    }
private:
    void move_creature_on_map(int nx, int ny)
    {
        if(npc_field[ny][nx] == 0 && field[ny][nx] != 1 && ny >= 0 && nx >= 0 && nx <= SCREEN_SYMW - 1 && ny <= SCREEN_SYMH - 1)
        {
            int creature_id = npc_field[creature_y][creature_x];
            npc_field[creature_y][creature_x] = 0;
            creature_x = nx;
            creature_y = ny;
            npc_field[creature_y][creature_x] = creature_id;
        }
        else if(npc_field[ny][nx] != 0  && field[ny][nx] != 1 && ny >= 0 && nx >= 0 && nx <= SCREEN_SYMW - 1 && ny <= SCREEN_SYMH - 1)
        {
            if(npc_field[ny][nx] == -1)
            {
                killers.push_back(creature_name);
                int pq;
                if(creature_atk <= 0)
                    pq = creature_atk;
                else
                    pq = std::max(0,creature_atk - player_def);
                player_hit += pq;
                message("H" + int_to_string(pq,true) + "b:" + creature_name + "|");
            }
            else
            {
                deal_true_damage(npc_field[ny][nx],creature_atk);
                message("F" + int_to_string(creature_atk,true) + "b:" + creature_name + "|");
            }
        }
    }
public:
    int get_atk()
    {
        return creature_atk;
    }
    int get_hp()
    {
        return creature_hp;
    }
    void move_creature()
    {
        for(int turns = 0; turns < creature_spd; turns++)
        {
            if(creature_rep == INTELLECT_STAY || creature_rep == INTELLECT_STUN)
            {

            }
            if(creature_rep == INTELLECT_RANDOM_WEP)
            {
                int rndn = std::rand()%4;
                if(rndn == 0)
                {
                    move_creature_on_map(creature_x+1,creature_y);
                }
                else if(rndn == 1)
                {
                    move_creature_on_map(creature_x,creature_y-1);
                }
                else if(rndn == 2)
                {
                    move_creature_on_map(creature_x-1,creature_y);
                }
                else if(rndn == 3)
                {
                    move_creature_on_map(creature_x,creature_y+1);
                }
            }
            if(creature_rep == INTELLECT_AGGRO_WEP)
            {
                if(std::rand() % 19 == 0)
                {
                    int rndn = std::rand()%4;
                    if(rndn == 0)
                    {
                        move_creature_on_map(creature_x+1,creature_y);
                    }
                    else if(rndn == 1)
                    {
                        move_creature_on_map(creature_x,creature_y-1);
                    }
                    else if(rndn == 2)
                    {
                        move_creature_on_map(creature_x-1,creature_y);
                    }
                    else if(rndn == 3)
                    {
                        move_creature_on_map(creature_x,creature_y+1);
                    }
                }
                else
                {
                    std::pair<int,int> used[SCREEN_SYMH + 2][SCREEN_SYMW + 2];
                    for(int i = 0; i < SCREEN_SYMH + 2; i ++)
                    {
                        for(int j =0; j < SCREEN_SYMW + 2; j ++)
                        {
                            used[i][j] = {-1,-1};
                        }
                    }
                    std::queue<std::pair<int,int> >st;
                    st.push({creature_x,creature_y});
                    used[creature_y][creature_x] = {0,0};
                    bool can_go = 0;
                    while(!st.empty())
                    {
                        int x = st.front().first;
                        int y = st.front().second;
                        st.pop();
                        if(x == player_x && y == player_y)
                        {
                            can_go = 1;
                            break;
                        }
                        if(x - 1 > 0 && used[y][x-1].first == -1 && used[y][x-1].second == -1 && field[y][x-1] == 0 && (npc_field[y][x-1] == 0 || npc_field[y][x-1] == -1))
                        {
                            st.push({x-1,y});
                            used[y][x-1] = {x,y};
                        }
                        if(x + 1 < SCREEN_SYMW && used[y][x+1].first == -1 && used[y][x+1].second == -1 && field[y][x+1] == 0 && (npc_field[y][x+1] == 0 || npc_field[y][x+1] == -1))
                        {
                            st.push({x+1,y});
                            used[y][x+1] = {x,y};
                        }
                        if(y - 1 > 0 && used[y-1][x].first == -1 && used[y-1][x].second == -1 && field[y-1][x] == 0 && (npc_field[y-1][x] == 0 || npc_field[y-1][x] == -1))
                        {
                            st.push({x,y-1});
                            used[y-1][x] = {x,y};
                        }
                        if(y + 1 < SCREEN_SYMH && used[y+1][x].first == -1 && used[y+1][x].second == -1 && field[y+1][x] == 0 && (npc_field[y+1][x] == 0 || npc_field[y+1][x] == -1))
                        {
                            st.push({x,y+1});
                            used[y+1][x] = {x,y};
                        }
                    }
                    if(can_go)
                    {
                        int lx = player_x,ly = player_y;
                        int tx = player_x,ty = player_y;
                        while(tx != creature_x || ty != creature_y)
                        {
                            lx = tx;
                            ly = ty;
                            tx = used[ly][lx].first;
                            ty = used[ly][lx].second;
                        }
                        move_creature_on_map(lx,ly);
                    }
                    else
                    {
                        if(creature_x < player_x)
                        {
                            move_creature_on_map(creature_x+1,creature_y);
                        }
                        else if(creature_y > player_y)
                        {
                            move_creature_on_map(creature_x,creature_y-1);
                        }
                        else if(creature_x > player_x)
                        {
                            move_creature_on_map(creature_x-1,creature_y);
                        }
                        else if(creature_y < player_y)
                        {
                            move_creature_on_map(creature_x,creature_y+1);
                        }
                    }
                }
            }
            if(creature_rep == INTELLECT_RANDOM_SCT)
            {
                int rndn = std::rand()%5;
                if(rndn == 0)
                {
                    move_creature_on_map(creature_x+1,creature_y);
                }
                else if(rndn == 1)
                {
                    move_creature_on_map(creature_x,creature_y-1);
                }
                else if(rndn == 2)
                {
                    move_creature_on_map(creature_x-1,creature_y);
                }
                else if(rndn == 3)
                {
                    move_creature_on_map(creature_x,creature_y+1);
                }
                else
                {
                    zap_spell(std::rand() % 5,creature_x,creature_y,std::rand() % (SCREEN_SYMW - 1) + 1,std::rand() % (SCREEN_SYMH - 1) + 1);
                }
            }
            if(creature_rep == INTELLECT_AGGRO_SCT)
            {
                int rndn = std::rand()%5;
                if(rndn == 0)
                {
                    move_creature_on_map(creature_x+1,creature_y);
                }
                else if(rndn == 1)
                {
                    move_creature_on_map(creature_x,creature_y-1);
                }
                else if(rndn == 2)
                {
                    move_creature_on_map(creature_x-1,creature_y);
                }
                else if(rndn == 3)
                {
                    move_creature_on_map(creature_x,creature_y+1);
                }
                else
                {
                    zap_spell(std::rand() % 5,creature_x,creature_y,player_x + std::rand() % 4 - 2,player_y + std::rand() % 4 - 2);
                }
            }
            if(creature_rep == INTELLECT_HELPER)
            {
                std::pair<int,int>tans = get_nearest_hostile(creature_x,creature_y);
                int t_x = tans.first;
                int t_y = tans.second;
                std::pair<int,int> used[SCREEN_SYMH + 2][SCREEN_SYMW + 2];
                for(int i = 0; i < SCREEN_SYMH + 2; i ++)
                {
                    for(int j =0; j < SCREEN_SYMW + 2; j ++)
                    {
                        used[i][j] = {-1,-1};
                    }
                }
                std::queue<std::pair<int,int> >st;
                st.push({creature_x,creature_y});
                used[creature_y][creature_x] = {0,0};
                bool can_go = 0;
                while(!st.empty())
                {
                    int x = st.front().first;
                    int y = st.front().second;
                    st.pop();
                    if(x == t_x && y == t_y)
                    {
                        can_go = 1;
                        break;
                    }
                    if(x - 1 > 0 && used[y][x-1].first == -1 && used[y][x-1].second == -1 && field[y][x-1] == 0 && (npc_field[y][x-1] == 0 || npc_field[y][x-1] == -1))
                    {
                        st.push({x-1,y});
                        used[y][x-1] = {x,y};
                    }
                    if(x + 1 < SCREEN_SYMW && used[y][x+1].first == -1 && used[y][x+1].second == -1 && field[y][x+1] == 0 && (npc_field[y][x+1] == 0 || npc_field[y][x+1] == -1))
                    {
                        st.push({x+1,y});
                        used[y][x+1] = {x,y};
                    }
                    if(y - 1 > 0 && used[y-1][x].first == -1 && used[y-1][x].second == -1 && field[y-1][x] == 0 && (npc_field[y-1][x] == 0 || npc_field[y-1][x] == -1))
                    {
                        st.push({x,y-1});
                        used[y-1][x] = {x,y};
                    }
                    if(y + 1 < SCREEN_SYMH && used[y+1][x].first == -1 && used[y+1][x].second == -1 && field[y+1][x] == 0 && (npc_field[y+1][x] == 0 || npc_field[y+1][x] == -1))
                    {
                        st.push({x,y+1});
                        used[y+1][x] = {x,y};
                    }
                }
                if(can_go)
                {
                    int lx = t_x,ly = t_y;
                    int tx = t_x,ty = t_y;
                    while(tx != creature_x || ty != creature_y)
                    {
                        lx = tx;
                        ly = ty;
                        tx = used[ly][lx].first;
                        ty = used[ly][lx].second;
                    }
                    move_creature_on_map(lx,ly);
                }
                else
                {
                    if(creature_x < t_x)
                    {
                        move_creature_on_map(creature_x+1,creature_y);
                    }
                    else if(creature_y > t_y)
                    {
                        move_creature_on_map(creature_x,creature_y-1);
                    }
                    else if(creature_x > t_x)
                    {
                        move_creature_on_map(creature_x-1,creature_y);
                    }
                    else if(creature_y < t_y)
                    {
                        move_creature_on_map(creature_x,creature_y+1);
                    }
                }
            }
            if(creature_rep == INTELLECT_THR)
            {
                int iy = abs(creature_y - player_y);
                int ix = abs(creature_x - player_x);
                if(t_rng * t_rng < iy * iy + ix * ix)
                {
                    if(std::rand() % 19 == 0)
                    {
                        int rndn = std::rand()%4;
                        if(rndn == 0)
                        {
                            move_creature_on_map(creature_x+1,creature_y);
                        }
                        else if(rndn == 1)
                        {
                            move_creature_on_map(creature_x,creature_y-1);
                        }
                        else if(rndn == 2)
                        {
                            move_creature_on_map(creature_x-1,creature_y);
                        }
                        else if(rndn == 3)
                        {
                            move_creature_on_map(creature_x,creature_y+1);
                        }
                    }
                    else
                    {
                        std::pair<int,int> used[SCREEN_SYMH + 2][SCREEN_SYMW + 2];
                        for(int i = 0; i < SCREEN_SYMH + 2; i ++)
                        {
                            for(int j =0; j < SCREEN_SYMW + 2; j ++)
                            {
                                used[i][j] = {-1,-1};
                            }
                        }
                        std::queue<std::pair<int,int> >st;
                        st.push({creature_x,creature_y});
                        used[creature_y][creature_x] = {0,0};
                        bool can_go = 0;
                        while(!st.empty())
                        {
                            int x = st.front().first;
                            int y = st.front().second;
                            st.pop();
                            if(x == player_x && y == player_y)
                            {
                                can_go = 1;
                                break;
                            }
                            if(x - 1 > 0 && used[y][x-1].first == -1 && used[y][x-1].second == -1 && field[y][x-1] == 0 && (npc_field[y][x-1] == 0 || npc_field[y][x-1] == -1))
                            {
                                st.push({x-1,y});
                                used[y][x-1] = {x,y};
                            }
                            if(x + 1 < SCREEN_SYMW && used[y][x+1].first == -1 && used[y][x+1].second == -1 && field[y][x+1] == 0 && (npc_field[y][x+1] == 0 || npc_field[y][x+1] == -1))
                            {
                                st.push({x+1,y});
                                used[y][x+1] = {x,y};
                            }
                            if(y - 1 > 0 && used[y-1][x].first == -1 && used[y-1][x].second == -1 && field[y-1][x] == 0 && (npc_field[y-1][x] == 0 || npc_field[y-1][x] == -1))
                            {
                                st.push({x,y-1});
                                used[y-1][x] = {x,y};
                            }
                            if(y + 1 < SCREEN_SYMH && used[y+1][x].first == -1 && used[y+1][x].second == -1 && field[y+1][x] == 0 && (npc_field[y+1][x] == 0 || npc_field[y+1][x] == -1))
                            {
                                st.push({x,y+1});
                                used[y+1][x] = {x,y};
                            }
                        }
                        if(can_go)
                        {
                            int lx = player_x,ly = player_y;
                            int tx = player_x,ty = player_y;
                            while(tx != creature_x || ty != creature_y)
                            {
                                lx = tx;
                                ly = ty;
                                tx = used[ly][lx].first;
                                ty = used[ly][lx].second;
                            }
                            move_creature_on_map(lx,ly);
                        }
                        else
                        {
                            if(creature_x < player_x)
                            {
                                move_creature_on_map(creature_x+1,creature_y);
                            }
                            else if(creature_y > player_y)
                            {
                                move_creature_on_map(creature_x,creature_y-1);
                            }
                            else if(creature_x > player_x)
                            {
                                move_creature_on_map(creature_x-1,creature_y);
                            }
                            else if(creature_y < player_y)
                            {
                                move_creature_on_map(creature_x,creature_y+1);
                            }
                        }
                    }
                }
                else
                {
                    killers.push_back(creature_name);
                    int pq;
                    if(creature_atk <= 0)
                        pq = creature_atk;
                    else
                        pq = std::max(0,creature_atk - player_def);
                    player_hit += pq;
                    message("H" + int_to_string(pq,true) + "b:" + creature_name + "|");
                }
            }
            if(creature_rep == INTELLECT_BOSS_BERSERKER)
            {
                if(std::rand() % 1007 == 0)
                {
                    int rndn = std::rand()%4;
                    if(rndn == 0)
                    {
                        move_creature_on_map(creature_x+1,creature_y);
                    }
                    else if(rndn == 1)
                    {
                        move_creature_on_map(creature_x,creature_y-1);
                    }
                    else if(rndn == 2)
                    {
                        move_creature_on_map(creature_x-1,creature_y);
                    }
                    else if(rndn == 3)
                    {
                        move_creature_on_map(creature_x,creature_y+1);
                    }
                }
                else
                {
                    if(creature_x < player_x)
                    {
                        move_creature_on_map(creature_x+1,creature_y);
                    }
                    else if(creature_y > player_y)
                    {
                        move_creature_on_map(creature_x,creature_y-1);
                    }
                    else if(creature_x > player_x)
                    {
                        move_creature_on_map(creature_x-1,creature_y);
                    }
                    else if(creature_y < player_y)
                    {
                        move_creature_on_map(creature_x,creature_y+1);
                    }
                }
            }
            if(creature_rep == INTELLECT_BOSS_MAGICIAN)
            {
                int ix = abs(player_x - creature_x);
                int iy = abs(player_y - creature_y);
                if(ix + iy <= 1)
                {
                    zap_spell(4,creature_x,creature_y,player_x,player_y);
                }
                else if(ix <= 10 && iy <= 10)
                {
                    zap_spell(10,creature_x,creature_y,player_x,player_y);
                }
                else
                {
                    if(creature_x > player_x)
                    {
                        move_creature_on_map(creature_x+1,creature_y);
                    }
                    else if(creature_y < player_y)
                    {
                        move_creature_on_map(creature_x,creature_y-1);
                    }
                    else if(creature_x < player_x)
                    {
                        move_creature_on_map(creature_x-1,creature_y);
                    }
                    else if(creature_y > player_y)
                    {
                        move_creature_on_map(creature_x,creature_y+1);
                    }
                }
            }
            if(creature_rep == INTELLECT_BOSS_NECROMANCER)
            {
                int ix = abs(player_x - creature_x);
                int iy = abs(player_y - creature_y);
                if(std::max(ix,iy) > 5)
                {
                    int coiny = std::rand() % 100 + 1;
                    if(coiny <= 20)
                    {
                        int sx = 0;
                        int sy = 0;
                        if(creature_x < player_x)
                        {
                            sx = -1;
                        }
                        if(creature_x > player_x)
                        {
                            sx = 1;
                        }
                        if(creature_y < player_y)
                        {
                            sy = -1;
                        }
                        if(creature_y > player_y)
                        {
                            sy = 1;
                        }
                        if(coiny % 5 == 0)
                        {
                            spawn_creature("Evil fork",1,2,1,1,INTELLECT_AGGRO_WEP,creature_x + sx,creature_y + sy,'F');
                        }
                        else if(coiny % 5 == 1)
                        {
                            spawn_creature("Evil spoon",2,1,2,1,INTELLECT_AGGRO_WEP,creature_x + sx,creature_y + sy,'S');
                        }
                        else if(coiny % 5 == 2)
                        {
                            spawn_creature("Evil knife",5,5,0,0,INTELLECT_STUN,creature_x + sx,creature_y + sy,'K');
                        }
                        else if(coiny % 5 == 3)
                        {
                            spawn_creature("Evil teapot",5,5,1,0,INTELLECT_AGGRO_WEP,creature_x + sx,creature_y + sy,'K');
                        }
                        else if(coiny % 5 == 4)
                        {
                            spawn_creature("Evil cup",5,5,2,0,INTELLECT_AGGRO_SCT,creature_x + sx,creature_y + sy,'K');
                        }
                    }
                }
            }
        }
    }
    void change_rep_up()
    {
        creature_rep = intellect_up[creature_rep];
    }
    void change_rep_down()
    {
        creature_rep = intellect_down[creature_rep];
    }
    bool empty()
    {
        return c_empty;
    }
    int get_rep()
    {
        return creature_rep;
    }
    void deal_damage(int damage)
    {
        creature_hp -= damage;
    }
    bool alive()
    {
        return (creature_hp > 0);
    }
    ITEM get_drop()
    {
        return creature_drop;
    }
    std::string get_name()
    {
        return creature_name;
    }
    char get_type()
    {
        return creature_type;
    }
    int get_drop_chance()
    {
        return drop_chance;
    }
    int get_y()
    {
        return creature_y;
    }
    int get_x()
    {
        return creature_x;
    }
};

#endif // CREATURE_LIB_H
