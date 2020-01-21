#ifndef SKILLS_H
#define SKILLS_H

class SKILL
{
    int lvl;
    int type;
    std::string name;
    std::string description;
public:
    SKILL() {}
    SKILL(int nlvl, int ntype, std::string nname, std::string ndescription)
    {
        lvl = nlvl;
        type = ntype;
        name = nname;
        description = ndescription;
    }
    std::string get_name()
    {
        return name;
    }
    std::string get_description()
    {
        return description;
    }
    int get_lvl()
    {
        return lvl;
    }
    int get_type()
    {
        return type;
    }
};

SKILL player_skills[100];
int player_skills_count = 0;

SKILL skill_library[] = {
    SKILL(1,1,"Tport", "Ports you somewhere. Beware of shadows!")
};

void add_skill(SKILL sk)
{
    if(player_skills_count < 100)
    {
        player_skills[player_skills_count] = sk;
        player_skills_count++;
    }
}

void player_use_skill(SKILL sk)
{
    int tp = sk.get_type();
    int eff = sk.get_lvl();
    message("USK|");
    switch(tp)
    {
    case 1:{
        int npx = rand() % (SCREEN_SYMW - 1) + 1;
        int npy = rand() % (SCREEN_SYMH - 1) + 1;
        if(npc_field[npy][npx] != 0 && npc_field[npy][npx] != -1){
            creature_base[npc_field[npy][npx]].deal_damage(1000);
            if(!creature_base[npc_field[npy][npx]].alive())
            {
                message("K:"+creature_base[npc_field[npy][npx]].get_name()+"|");
                int coiny = std::rand()%100 + 1;
                if(coiny <= creature_base[npc_field[npy][npx]].get_drop_chance())
                {
                    put_item_to_map(creature_base[npc_field[npy][npx]].get_drop(),npx,npy);
                    creature_base.erase(npc_field[npy][npx]);
                    npc_field[npy][npx] = 0;
                }
                else
                {
                    creature_base.erase(npc_field[npy][npx]);
                    npc_field[npy][npx] = 0;
                }
                int rpx = player_x;
                int rpy = player_y;
                move_player(npx, npy);
                coiny = std::rand() % 100 + 1;
                if(coiny > eff){
                    put_creature_to_map(CREATURE("Shadow", 1, player_atk, 10, 1, INTELLECT_AGGRO_WEP, rpx, rpy, {}, '?', 0), rpx, rpy);
                }
            }
        }else{
            int rpx = player_x;
            int rpy = player_y;
            move_player(npx, npy);
            int coiny = std::rand() % 100 + 1;
            if(coiny > eff){
                put_creature_to_map(CREATURE("Shadow", 1, player_atk, 10, 1, INTELLECT_AGGRO_WEP, rpx, rpy, {}, '?', 0), rpx, rpy);
            }
        }
    }
        break;
    default:
        break;
    }
}

#endif //SKILLS_H
