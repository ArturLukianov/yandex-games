#ifndef GAME_FUNCTIONS_H
#define GAME_FUNCTIONS_H

void generate_field()
{
    srand(time(NULL));
    for(int i = 0 ; i < SCREEN_SYMH; i++)
    {
        for(int j = 0 ; j < SCREEN_SYMW; j++)
        {
            if(i == 0 || j == 0 || i == SCREEN_SYMH - 1 || j == SCREEN_SYMW - 1)
            {
                field[i][j] = 1;
            }
            else
            {
                field[i][j] = 0;
            }
            item_field[i][j] = 0;
            npc_field[i][j] = 0;
        }
    }
    npc_field[player_y][player_x] = -1;
    creature_base.clear();
    item_base.clear();
}



void zap_spell(int spell_num,int sx,int sy,int tx,int ty)
{
    script_library[spell_num].exec(sx,sy,tx,ty);
    killers.push_back("Magic");
}

std::pair<int,int> get_nearest_hostile(int creature_x,int creature_y)
{
    int t_x = -1,t_y,mxu = 10000000;
    for(std::map<int,CREATURE>::iterator it = creature_base.begin(); it != creature_base.end(); it++)
    {
        if(it->second.get_rep() != INTELLECT_HELPER)
        {
            int ix = abs(it->second.get_x() - creature_x);
            int iy = abs(it->second.get_y() - creature_y);
            if(mxu >= ix * ix + iy * iy)
            {
                mxu = ix * ix + iy * iy;
                t_x = it->second.get_x();
                t_y = it->second.get_y();
            }
        }
    }
    return {t_x,t_y};
}

void deal_true_damage(int mon_id,int atk)
{
    creature_base[mon_id].deal_damage(atk);
    message("A"+int_to_string(player_atk,true)+"t:"+creature_base[mon_id].get_name()+"|");
    creature_base[mon_id].change_rep_up();
    if(!creature_base[mon_id].alive())
    {
        message("K:"+creature_base[mon_id].get_name()+"|");
        if(creature_base[mon_id].get_name() == "MIAKO")
            miakos_killed++;
        int coiny = std::rand()%100 + 1;
        if(coiny <= creature_base[mon_id].get_drop_chance())
        {
            npc_field[creature_base[mon_id].get_y()][creature_base[mon_id].get_x()] = 0;
            put_item_to_map(creature_base[mon_id].get_drop(),creature_base[mon_id].get_x(),creature_base[mon_id].get_y());
            creature_base.erase(mon_id);
        }
        else
        {
            npc_field[creature_base[mon_id].get_y()][creature_base[mon_id].get_x()] = 0;
            creature_base.erase(mon_id);
        }
    }
}

void apply_effect(int effect,int effect_str,ITEM (*inventory)[inventory_size])
{
    renew_stats();
    std::string msg = "E:";
    if(effect == EFFECT_HEAL)
    {
        player_lp += effect_str;
        msg+="heal"+int_to_string(effect_str,true);
        if(effect_str < 0)
        {
            killers.push_back("Your carelessness");
        }
    }
    if(effect == EFFECT_SPUP)
    {
        player_sp+=effect_str;
        msg+="spup"+int_to_string(effect_str,true);
    }
    if(effect == EFFECT_TPUP)
    {
        player_tp+=effect_str;
        msg+="tpup"+int_to_string(effect_str,true);
    }
    if(effect == EFFECT_UNCURSE)
    {
        player_current_armor.set_cursed(0);
        player_current_weapon.set_cursed(0);
        (*inventory)[using_armor_inventory_index].set_cursed(0);
        (*inventory)[using_weapon_inventory_index].set_cursed(0);
        msg+="uncurse";
    }
    if(effect == EFFECT_CURSE)
    {
        player_current_armor.set_cursed(1);
        player_current_weapon.set_cursed(1);
        (*inventory)[using_armor_inventory_index].set_cursed(1);
        (*inventory)[using_weapon_inventory_index].set_cursed(1);
        msg+="curse";
    }
    if(effect == EFFECT_POLYMORPH)
    {
        symbol_code[2] = alphabet[std::rand()%alphabet_size];
        for(std::map<int,CREATURE>::iterator it = creature_base.begin(); it != creature_base.end(); it++)
        {
            if(effect_str > 0)
                it->second.change_rep_down();
            else
                it->second.change_rep_up();
        }
        msg+="poly"+int_to_string(effect_str,true);
    }
    if(effect == EFFECT_SPAWN)
    {
        put_creature_to_map(CREATURE(creature_stamps[std::rand() % effect_str + 1][std::rand() % creature_stamps[effect_str].size()],player_x + 1,player_y + 1,ITEM()),player_x + 1,player_y+1);
        put_creature_to_map(CREATURE(creature_stamps[std::rand() % effect_str + 1][std::rand() % creature_stamps[effect_str].size()],player_x + 1,player_y - 1,ITEM()),player_x + 1,player_y-1);
        put_creature_to_map(CREATURE(creature_stamps[std::rand() % effect_str + 1][std::rand() % creature_stamps[effect_str].size()],player_x - 1,player_y - 1,ITEM()),player_x - 1,player_y-1);
        put_creature_to_map(CREATURE(creature_stamps[std::rand() % effect_str + 1][std::rand() % creature_stamps[effect_str].size()],player_x - 1,player_y + 1,ITEM()),player_x - 1,player_y+1);
        msg+="spawn"+int_to_string(effect_str,true);
    }
    if(effect == EFFECT_BLAST)
    {
        int blast_radius = std::abs(effect_str);
        for(int i = player_x - blast_radius; i < player_x + blast_radius; i++)
        {
            for(int j = player_y - blast_radius; j < player_y + blast_radius; j++)
            {
                if(item_field[j][i] != 0)
                {
                    item_base.erase(item_field[j][i]);
                    item_field[j][i] = 0;
                }
                if(npc_field[j][i] != 0)
                {
                    if(npc_field[j][i] == -1)
                    {
                        int pq;
                        if(-effect_str <= 0)
                            pq = -effect_str;
                        else
                            pq = std::max(0,- effect_str - player_def);
                        player_hit += pq;
                    }
                    else
                    {
                        creature_base[npc_field[j][i]].deal_damage(effect_str);
                        message("B"+int_to_string(effect_str,true)+"t:"+creature_base[npc_field[j][i]].get_name()+"|");
                        creature_base[npc_field[j][i]].change_rep_up();
                        if(!creature_base[npc_field[j][i]].alive())
                        {
                            message("K:"+creature_base[npc_field[j][i]].get_name()+"|");
                            creature_base.erase(npc_field[j][i]);
                            npc_field[j][i] = 0;
                        }
                    }
                }
            }
        }
        msg+="blast"+int_to_string(effect_str,true);
    }
    msg+="|";
    renew_stats();
    message(msg);
}

bool use_item(ITEM item,ITEM (*inventory)[inventory_size],int inventory_current_size,int index)
{
    if(item.is_using() == 0)
    {
        if(item.get_type() == TYPE_WEAPON || item.get_type() == TYPE_THROWABLE)
        {
            if(weapon_on && (*inventory)[using_weapon_inventory_index].get_cursed())
            {
                return false;
            }
            if(weapon_on)
            {
                (*inventory)[using_weapon_inventory_index].deselect();
            }
            player_current_weapon = item;
            weapon_on = true;
            using_weapon_inventory_index = index;
            renew_stats();
            return true;
        }
        if(item.get_type() == TYPE_ARMOR)
        {
            if(armor_on && (*inventory)[using_armor_inventory_index].get_cursed())
            {
                return false;
            }
            if(armor_on)
            {
                (*inventory)[using_armor_inventory_index].deselect();
            }
            player_current_armor = item;
            using_armor_inventory_index = index;
            armor_on = true;
            renew_stats();
            return true;
        }
        if(item.get_type() == TYPE_POTION)
        {
            apply_effect(item.get_effect(),item.get_effect_str(),inventory);
            renew_stats();
            return true;
        }
        if(item.get_type() == TYPE_BOOK)
        {
            player_script = script_library[item.get_learn()];
            renew_stats();
            message("LEARNED|");
            return true;
        }
    }
    else
    {
        if(item.get_type() == TYPE_WEAPON || item.get_type() == TYPE_THROWABLE)
        {
            weapon_on = false;
            renew_stats();
            return true;
        }
        if(item.get_type() == TYPE_ARMOR)
        {
            armor_on = false;
            renew_stats();
            return true;
        }
    }
    return false;
}

void redraw_screen()
{
    COORD topLeft  = { 0, 0 };
    SetConsoleCursorPosition(hConsole, topLeft);
    TCHAR rfield[(SCREEN_SYMW + 1) * SCREEN_SYMH];
    int rfield_pos = 0;
    int symc=0;
    int lattr = -1;
    DWORD dwBuff;
    for(int i = 0 ; i < SCREEN_SYMH; i++)
    {
        for(int j = 0 ; j < SCREEN_SYMW; j++)
        {
            int tattr;
            char nsym;
            if(npc_field[i][j] != 0)
            {
                if(npc_field[i][j] == -1)
                {
                    nsym = symbol_code[2];
                    tattr = symbol_attr[2];
                }
                else
                {
                    nsym = creature_base[npc_field[i][j]].get_type();
                    tattr = symbol_attr[4];
                }
            }
            else if(item_field[i][j] != 0)
            {
                nsym = symbol_code[3];
                tattr = symbol_attr[3];
            }
            else
            {
                nsym = symbol_code[field[i][j]];
                tattr = symbol_attr[field[i][j]];
            }
            if(tattr != lattr && lattr != -1)
            {
                SetConsoleTextAttribute(hConsole,lattr);
                WriteConsole(hConsole,&rfield,symc,&dwBuff,NULL);
                rfield_pos = 0;
                symc = 0;
            }
            lattr = tattr;
            rfield[rfield_pos++] = nsym;
            symc++;
        }
        rfield[rfield_pos++] = '\n';
        symc++;
    }
    SetConsoleTextAttribute(hConsole,lattr);
    WriteConsole(hConsole,&rfield,symc,&dwBuff,NULL);
    SetConsoleTextAttribute(hConsole,15);
    message_out();
    hide_cursor();
}


void redraw_screen_no_message()
{
    COORD topLeft  = { 0, 0 };
    SetConsoleCursorPosition(hConsole, topLeft);
    TCHAR rfield[(SCREEN_SYMW + 1) * SCREEN_SYMH];
    int rfield_pos = 0;
    int symc=0;
    int lattr = -1;
    DWORD dwBuff;
    for(int i = 0 ; i < SCREEN_SYMH; i++)
    {
        for(int j = 0 ; j < SCREEN_SYMW; j++)
        {
            int tattr;
            char nsym;
            if(npc_field[i][j] != 0)
            {
                if(npc_field[i][j] == -1)
                {
                    nsym = symbol_code[2];
                    tattr = symbol_attr[2];
                }
                else
                {
                    nsym = creature_base[npc_field[i][j]].get_type();
                    tattr = symbol_attr[4];
                }
            }
            else if(item_field[i][j] != 0)
            {
                nsym = symbol_code[3];
                tattr = symbol_attr[3];
            }
            else
            {
                nsym = symbol_code[field[i][j]];
                tattr = symbol_attr[field[i][j]];
            }
            if(tattr != lattr && lattr != -1)
            {
                SetConsoleTextAttribute(hConsole,lattr);
                WriteConsole(hConsole,&rfield,symc,&dwBuff,NULL);
                rfield_pos = 0;
                symc = 0;
            }
            lattr = tattr;
            rfield[rfield_pos++] = nsym;
            symc++;
        }
        rfield[rfield_pos++] = '\n';
        symc++;
    }
    SetConsoleTextAttribute(hConsole,lattr);
    WriteConsole(hConsole,&rfield,symc,&dwBuff,NULL);
    SetConsoleTextAttribute(hConsole,15);
    hide_cursor();
}

void turn()
{
    redraw_screen_no_message();
    wave_timer++;
    std::vector<std::pair<int,int> >need_delete;
    for(std::map<int,CREATURE>::iterator it = creature_base.begin(); it != creature_base.end(); it++)
    {
        if(!it->second.alive())
        {
            need_delete.push_back({it->second.get_y(),it->second.get_x()});
        }
        else
        {
            it->second.move_creature();
        }
    }
    for(int i = 0 ; i < need_delete.size(); i++)
    {
        int ny = need_delete[i].first;
        int nx = need_delete[i].second;
        int coiny = std::rand()%100 + 1;
        if(coiny <= creature_base[npc_field[ny][nx]].get_drop_chance())
        {
            put_item_to_map(creature_base[npc_field[ny][nx]].get_drop(),nx,ny);
            creature_base.erase(npc_field[ny][nx]);
            npc_field[ny][nx] = 0;
        }
        else
        {
            creature_base.erase(npc_field[ny][nx]);
            npc_field[ny][nx] = 0;
        }
    }
}

void inventory_menu(ITEM (*inventory)[inventory_size], int *current_inventory_size,int x,int y)
{
    bool inventory_running  = 1;
    do
    {
        show_inventory(inventory,*current_inventory_size);
        int i_key = tgetch();
        if(i_key == K_d)
        {
            int selected_el = inventory_select_item("DROP",inventory,*current_inventory_size);
            if(selected_el != -1)
            {
                if(!((*inventory)[selected_el].is_using() && (*inventory)[selected_el].get_cursed()))
                {
                    (*inventory)[selected_el].deselect();
                    if(put_item_to_map((*inventory)[selected_el],x,y) != -1)
                    {
                        if((*inventory)[selected_el].is_using())
                        {
                            if(use_item((*inventory)[selected_el],inventory,*current_inventory_size,selected_el))
                            {
                                (*inventory)[selected_el].deselect();
                            }
                        }
                        if(using_armor_inventory_index > selected_el)
                        {
                            using_armor_inventory_index--;
                        }
                        if(using_weapon_inventory_index > selected_el)
                        {
                            using_weapon_inventory_index--;
                        }
                        if((*inventory)[selected_el].get_name() == "Coiny's coin")
                            coin_count--;
                        for(int q = selected_el; q < *current_inventory_size - 1; q++)
                        {
                            (*inventory)[q] = (*inventory)[q+1];
                        }
                        (*current_inventory_size)--;
                    }
                }
            }
        }
        else if(i_key == K_u)
        {
            int selected_el = inventory_select_item("USE",inventory,*current_inventory_size);
            if(selected_el != -1)
            {
                if(!((*inventory)[selected_el].is_using() && (*inventory)[selected_el].get_cursed()))
                {
                    if(use_item((*inventory)[selected_el],inventory,(*current_inventory_size),selected_el))
                    {
                        (*inventory)[selected_el].use();
                        if((*inventory)[selected_el].get_oneusable() && (*inventory)[selected_el].get_type() != TYPE_THROWABLE)
                        {
                            for(int q = selected_el; q < *current_inventory_size - 1; q++)
                            {
                                (*inventory)[q] = (*inventory)[q+1];
                            }
                            (*current_inventory_size)--;
                        }
                    }
                }
            }
        }
        else if(i_key == K_q)
        {
            inventory_running = 0;
        }
    }
    while(inventory_running);
}

void spawn_wave(int level)
{
    if(level > max_level)
        level = max_level;
    message("SWl:"+int_to_string(level,false)+"|");
    for(int i = 0; i < wave_spawn_coords_size; i++)
    {
        CREATURE_STAMP spawn_creature_stamp = creature_stamps[std::rand() % level + 1][std::rand() % creature_stamps[level].size()];
        ITEM spawn_drop = item_library[spawn_creature_stamp.creature_drop[std::rand()%spawn_creature_stamp.creature_drop.size()]].second;
        if(spawn_drop.get_type() != TYPE_POTION && spawn_drop.get_type() != TYPE_COLLECTIBLE && spawn_drop.get_type() != TYPE_BOOK)
        {
            spawn_drop.set_atk(std::rand() % (spawn_drop.get_level()*2));
            spawn_drop.set_def(std::rand() % (spawn_drop.get_level()*2));
        }
        spawn_drop.rcurse();
        CREATURE spawn_creature = CREATURE(spawn_creature_stamp,wave_spawn_coords[i][0],wave_spawn_coords[i][1],spawn_drop);
        put_creature_to_map(spawn_creature,wave_spawn_coords[i][0],wave_spawn_coords[i][1]);
    }
}

void move_player(int nx, int ny)
{
    if(npc_field[ny][nx] == 0 && field[ny][nx] != 1 && ny >= 0 && nx >= 0 && nx <= SCREEN_SYMW - 1 && ny <= SCREEN_SYMH - 1)
    {
        npc_field[player_y][player_x] = 0;
        player_lx = player_x;
        player_ly = player_y;
        player_x = nx;
        player_y = ny;
        npc_field[player_y][player_x] = -1;
        if(item_field[player_y][player_x] != 0)
        {
            message("S:"+item_base[item_field[player_y][player_x]].get_name()+"|");
        }
    }
    else if(npc_field[ny][nx] != 0)
    {
        creature_base[npc_field[ny][nx]].deal_damage(player_atk);
        message("A"+int_to_string(player_atk,true)+"t:"+creature_base[npc_field[ny][nx]].get_name()+"|");
        creature_base[npc_field[ny][nx]].change_rep_up();
        if(!creature_base[npc_field[ny][nx]].alive())
        {
            message("K:"+creature_base[npc_field[ny][nx]].get_name()+"|");
            if(creature_base[npc_field[ny][nx]].get_name() == "MIAKO")
                miakos_killed++;
            int coiny = std::rand()%100 + 1;
            if(coiny <= creature_base[npc_field[ny][nx]].get_drop_chance())
            {
                put_item_to_map(creature_base[npc_field[ny][nx]].get_drop(),nx,ny);
                creature_base.erase(npc_field[ny][nx]);
                npc_field[ny][nx] = 0;
            }
            else
            {
                creature_base.erase(npc_field[ny][nx]);
                npc_field[ny][nx] = 0;
            }
        }
    }
}

void show_stats(int atk,int def,int lp,int sp,int tp,int max_lp,int ep,int max_ep,std::string script_name)
{
    draw_frame();
    std::string stat_line = "ATK : " + int_to_string(atk,false);
    write_line_attr(stat_line,1,1,FOREGROUND_RED|FOREGROUND_INTENSITY);
    stat_line = "DEF : " + int_to_string(def,false);
    write_line_attr(stat_line,1,2,FOREGROUND_BLUE|FOREGROUND_INTENSITY);
    stat_line = "LP  : " + int_to_string(lp,false) + "/" + int_to_string(max_lp,false);
    write_line_attr(stat_line,1,3,FOREGROUND_GREEN|FOREGROUND_INTENSITY);
    stat_line = "EP  : " + int_to_string(ep,false) + "/" + int_to_string(max_ep,false);
    write_line_attr(stat_line,1,4,FOREGROUND_RED|FOREGROUND_GREEN|FOREGROUND_INTENSITY);
    stat_line = "SP  : " + int_to_string(sp,false);
    write_line_attr(stat_line,1,5,FOREGROUND_BLUE|FOREGROUND_GREEN|FOREGROUND_INTENSITY);
    stat_line = "TP  : " + int_to_string(tp,false);
    write_line_attr(stat_line,1,6,FOREGROUND_RED|FOREGROUND_BLUE|FOREGROUND_INTENSITY);
    stat_line = "WEP  : ";
    if(weapon_on)
    {
        stat_line+=player_current_weapon.get_name();
        stat_line+=" : ATK";
        stat_line+=int_to_string(player_current_weapon.get_atk(),true);
    }
    else
    {
        stat_line+=" NONE";
    }
    write_line_attr(stat_line,1,8,FOREGROUND_RED | BACKGROUND_WHITE|FOREGROUND_INTENSITY);
    stat_line = "ARM  : ";
    if(armor_on)
    {
        stat_line+=player_current_armor.get_name();
        stat_line+=" : DEF";
        stat_line+=int_to_string(player_current_armor.get_def(),true);
    }
    else
    {
        stat_line+=" NONE";
    }
    write_line_attr(stat_line,1,9,FOREGROUND_BLUE | BACKGROUND_WHITE|FOREGROUND_INTENSITY);
    stat_line = "SPT  :  " + script_name;
    write_line_attr(stat_line,1,10,FOREGROUND_GREEN|BACKGROUND_WHITE | FOREGROUND_INTENSITY);
    message_out();
    hide_cursor();
}

bool throw_weapon(int x,int y,ITEM weapon)
{
    if(npc_field[y][x] != 0 && npc_field[y][x] != -1)
    {
        creature_base[npc_field[y][x]].deal_damage(player_atk);
        message("A"+int_to_string(player_atk,true)+"t:"+creature_base[npc_field[y][x]].get_name()+"|");
        creature_base[npc_field[y][x]].change_rep_up();
        if(!creature_base[npc_field[y][x]].alive())
        {
            message("K:"+creature_base[npc_field[y][x]].get_name()+"|");
            int coiny = std::rand()%100 + 1;
            if(coiny <= creature_base[npc_field[y][x]].get_drop_chance())
            {
                put_item_to_map(creature_base[npc_field[y][x]].get_drop(),x,y);
                creature_base.erase(npc_field[y][x]);
                npc_field[y][x] = 0;
            }
            else
            {
                creature_base.erase(npc_field[y][x]);
                npc_field[y][x] = 0;
            }
        }
        message("THROWED|");
        return true;
    }
    return false;
}

bool throw_menu(ITEM weapon)
{
    bool throwing = true;
    int x = player_x;
    int y = player_y;
    while(throwing)
    {
        redraw_screen();
        int rx = x;
        int ry = y;
        while(rx != player_x || player_y != ry)
        {
            write_line_attr(",",rx,ry,BACKGROUND_GREEN);
            if(player_y < ry)
            {
                ry--;
            }
            else if(player_y > ry)
            {
                ry++;
            }
            if(player_x < rx)
            {
                rx--;
            }
            else if(player_x > rx)
            {
                rx++;
            }

        }
        write_line_attr("X",x,y,BACKGROUND_GREEN);
        int key = tgetch();
        if(key == K_ENTER)
        {
            if(throw_weapon(x,y,weapon))
            {
                return true;
            }
        }
        if(key == K_q)
        {
            return false;
        }
        if(key == K_DOWN)
        {
            if(abs(player_x - x)*abs(player_x - x) + abs(player_y - (y+1))*abs(player_y - (y+1)) <= weapon.get_rng()*weapon.get_rng())
                y++;
        }
        if(key == K_UP)
        {
            if(abs(player_x - x)*abs(player_x - x) + abs(player_y - (y-1))*abs(player_y - (y-1)) <= weapon.get_rng()*weapon.get_rng())
                y--;
        }
        if(key == K_RIGHT)
        {
            if(abs(player_x - (x-1))*abs(player_x - (x-1)) + abs(player_y - y)*abs(player_y - y) <= weapon.get_rng()*weapon.get_rng())
                x--;
        }
        if(key == K_LEFT)
        {
            if(abs(player_x - (x+1))*abs(player_x - (x+1)) + abs(player_y - y)*abs(player_y - y) <= weapon.get_rng()*weapon.get_rng())
                x++;
        }
        if(x < 0)
            x = 0;
        if(x > SCREEN_SYMW - 1)
            x = SCREEN_SYMW - 1;
        if(y < 0)
            y = 0;
        if(y > SCREEN_SYMH - 1)
            y = SCREEN_SYMH - 1;
    }
}

void spawn_creature(std::string name,int hp,int atk,int spd,int lvl,int rep,int x,int y,char sym)
{
    put_creature_to_map(CREATURE(name,hp,atk,spd,lvl,rep,x,y,ITEM(),sym,0),x,y);
}

void quest_menu()
{
    draw_frame();
    write_line_attr("QUESTS:",1,1,FOREGROUND_BLUE | FOREGROUND_INTENSITY);
    for(int i = 0 ; i < quest_cnt; i++)
    {
        write_line_attr(quest_name[i],1,2+i,quest[i]?(FOREGROUND_GREEN):(FOREGROUND_GREEN | FOREGROUND_RED | FOREGROUND_INTENSITY));
        if(quest[i])
        {
            write_line_attr("COMPLETED",50,2+i,(FOREGROUND_GREEN | FOREGROUND_INTENSITY));
        }
    }
    hide_cursor();
    tgetch();
}

void skills_menu()
{
    int cursor_pos = 0;
    bool loop = 1;
    while(loop){
        draw_frame();
        write_line_attr("SKILLS:",1,1,FOREGROUND_BLUE | FOREGROUND_INTENSITY);
        for(int i = 0; i < player_skills_count; i ++)
        {
            write_line_attr(player_skills[i].get_name(),1,2 + i, FOREGROUND_RED | FOREGROUND_INTENSITY);
            write_line_attr(player_skills[i].get_description(),10,2 + i, FOREGROUND_GREEN | FOREGROUND_INTENSITY);
        }
        if(player_skills_count == 0)
        {
            write_line_attr("None",1,2, FOREGROUND_RED | FOREGROUND_INTENSITY);
        }else{
            write_line_attr("<--",50,2+cursor_pos, FOREGROUND_BLUE | FOREGROUND_RED);
        }
        hide_cursor();
        int key = tgetch();
        if(key == K_q){
            loop = 0;
            break;
        }
        if(key == K_DOWN){
            cursor_pos++;
        }
        if(key == K_UP){
            cursor_pos--;
        }
        if(cursor_pos < 0 && player_skills_count != 0){
            cursor_pos = player_skills_count - 1;
        }
        if(cursor_pos >= player_skills_count && player_skills_count != 0){
            cursor_pos = 0;
        }
        if(key == K_ENTER && player_skills_count != 0){
            player_use_skill(player_skills[cursor_pos]);
            loop = 0;
            break;
        }
    }
}

std::string gen_name()
{
    int w_cnt = std::rand() % 5 + 2;
    std::string res = "";
    for(int i = 0 ; i < w_cnt; i++)
    {
        res += name_slogs[std::rand() % name_slogs_size];
    }
    return res;
}

void spawn_boss()
{
    message("BOSS|");
    int boss_x = std::rand() % (SCREEN_SYMW - 2) + 1;
    int boss_y = std::rand() % (SCREEN_SYMH - 2) + 1;
    ANIMATION an = ANIMATION(ANIMATION_BOSS,0);
    an.play(boss_x,boss_y);
    int sum_atk = 0;
    int sum_hp = 0;
    for(std::map<int,CREATURE>::iterator it = creature_base.begin(); it != creature_base.end(); it++)
    {
        sum_atk += it->second.get_atk();
        sum_hp += it->second.get_hp();
        it->second.deal_damage(it->second.get_hp());
    }
    turn();
    int boss_type = std::rand() % 3;
    std::string namae = gen_name();
    switch(boss_type)
    {
    case BOSS_BERSERKER:
        put_creature_to_map(
            CREATURE(namae,sum_hp / 4,sum_atk,2,10,INTELLECT_BOSS_BERSERKER,
                     boss_x,boss_y,ITEM(namae + "'s memory",TYPE_WEAPON,wave_level * 2,0,1),'&',100),
            boss_x,
            boss_y
        );
        break;
    case BOSS_MAGICIAN:
        put_creature_to_map(
            CREATURE(namae,sum_hp / 4,sum_atk / 4,1,10,INTELLECT_BOSS_MAGICIAN,
                     boss_x,boss_y,ITEM(namae + "'s memory",TYPE_BOOK,9),'&',100),
            boss_x,
            boss_y
        );
        break;
    case BOSS_NECROMANCER:
        put_creature_to_map(
            CREATURE(namae,sum_atk + sum_hp,0,1,10,INTELLECT_BOSS_NECROMANCER,
                     boss_x,boss_y,ITEM(namae + "'s memory",TYPE_BOOK,11 + std::rand() % 2),'&',100),
            boss_x,
            boss_y
        );
        break;
    default:
        break;
    }
}

void spawn_event(int event)
{
    switch(event)
    {
    case EVENT_deviloper:
        put_creature_to_map(CREATURE(creature_library[31].second,2,1,ITEM("ebon" + int_to_string(std::rand(),false),TYPE_ARMOR,1,12,1)),2,1);
        put_creature_to_map(CREATURE(creature_library[33].second,3,1,ITEM("ebon" + int_to_string(std::rand(),false),TYPE_WEAPON,1,1,1)),3,1);
        put_creature_to_map(CREATURE(creature_library[27].second,4,1,ITEM("ebon" + int_to_string(std::rand(),false),TYPE_WEAPON,1,1,1)),4,1);
        put_creature_to_map(CREATURE(creature_library[13].second,5,1,ITEM("ebon" + int_to_string(std::rand(),false),TYPE_COLLECTIBLE,1,1,1,2,1)),5,1);
        put_creature_to_map(CREATURE(creature_library[34].second,6,1,ITEM("ebon" + int_to_string(std::rand(),false),TYPE_WEAPON,1,1,1)),6,1);
        put_creature_to_map(CREATURE(creature_library[35].second,7,1,ITEM("ebon" + int_to_string(std::rand(),false),TYPE_ARMOR,1,1,1)),7,1);
        put_creature_to_map(CREATURE(creature_library[36].second,8,1,ITEM("ebon" + int_to_string(std::rand(),false),TYPE_ARMOR,1,1,1)),8,1);
        put_creature_to_map(CREATURE(creature_library[33].second,9,1,ITEM("ebon" + int_to_string(std::rand(),false),TYPE_WEAPON,1,1,1)),9,1);
        put_creature_to_map(CREATURE(creature_library[37].second,10,1,ITEM("ebon" + int_to_string(std::rand(),false),TYPE_COLLECTIBLE,1,1,1)),10,1);
        break;
    case EVENT_coinyrush:
        for(int i = 1; i < SCREEN_SYMW; i++){
            for(int j = 1; j < SCREEN_SYMH; j++){
                if(rand() % 100 + 1 == 1)
                    put_creature_to_map(CREATURE("coiny",1,1,1,1,INTELLECT_AGGRO_WEP,i,j,{},'~',0),i , j);
            }
        }
        break;
    }
}

void start_game()
{
    bool main_game_running = 1;
    int last_key = 0;
    for(int i = 0 ; i < quest_cnt; i++)
    {
        quest[i] = false;
    }
    ITEM inventory[inventory_size];
    int inventory_current_size = 0;
    strcpy(symbol_code, symbol_code_bk);
    player_skills_count = 0;
    player_lp = 10;
    boss_spawn_turn = 200;
    player_tp = 0;
    player_sp = 1;
    player_def = 0;
    player_atk = 1;
    coin_count = 0;
    player_max_lp = 10 + player_lp;
    renew_stats();
    wave_timer = 0;
    wave_interval = 100;
    next_wave = 0;
    miakos_killed = 0;
    wave_level = 0;
    wave_count = 0;
    wave_level_up_interval = 3;
    wave_next_level_up = 0;
    player_script = script_library[0];
    weapon_on = false;
    armor_on = false;
    player_x = SCREEN_SYMW / 2;
    player_y = SCREEN_SYMH / 2;
    player_max_ep = 10;
    player_ep = player_max_ep;
    renew_stats();
    player_hit = 0;
    add_skill(skill_library[0]);
    message("STARTED NEW GAME|");
    bool gameOver = false;
    generate_field();
    while(main_game_running)
    {
        killers.clear();
        if(wave_timer >= next_wave)
        {
            if(std::rand()%100 < 90)
            {
                try
                {
                    if(wave_count >= wave_next_level_up)
                    {
                        wave_level++;
                        wave_next_level_up = wave_count + wave_level_up_interval;
                        wave_level_up_interval += wave_level_up_interval / 4;
                    }
                    next_wave = wave_timer + wave_interval;
                    wave_interval += wave_level * 10;
                    message("HEH|");
                    spawn_wave(wave_level);
                    message("OKGI|");
                    wave_count++;
                }
                catch(int e)
                {
                    message("BOKRTD|");
                }
            }
            else
            {
                try
                {
                    spawn_event(std::rand() % events_cnt);
                }
                catch(int e)
                {
                    message("BOKRTD|");
                }
                next_wave = wave_timer + wave_interval;
            }
        }
        if(boss_spawn_turn <= wave_timer)
        {
            try
            {
                spawn_boss();
            }
            catch(int e)
            {
                message("BOKRTD|");
            }
            boss_spawn_turn += boss_spawn_turn * boss_multiply_interval;
        }
        redraw_screen();
        last_key = tgetch();
        if(last_key == K_UP)
        {
            move_player(player_x,player_y - 1);
            turn();
        }
        if(last_key == K_DOWN)
        {
            move_player(player_x,player_y + 1);
            turn();
        }
        if(last_key == K_LEFT)
        {
            move_player(player_x + 1,player_y);
            turn();
        }
        if(last_key == K_RIGHT)
        {
            move_player(player_x - 1,player_y);
            turn();
        }
        if(last_key == K_ENTER)
        {
            turn();
        }
        if(last_key == K_q)
        {
            quit_to_main_menu();
        }
        if(last_key == K_r)
        {
            quest_menu();
        }
        if(last_key == K_z)
        {
            skills_menu();
            turn();
        }
        if(last_key == K_p)
        {
            if(inventory_current_size < 10)
            {
                if(pick_up(&inventory, inventory_current_size,player_x,player_y))
                {
                    if(inventory[inventory_current_size].get_name() == "Coiny's coin")
                        coin_count++;
                    inventory_current_size++;
                }
            }
            else
            {
                if(!quest[7])
                {
                    message("DWYWBPIF AD|");
                    inventory_current_size = 0;
                    weapon_on = false;
                    armor_on = false;
                    quest[7] = true;
                }
            }
        }
        if(last_key == K_i)
        {
            inventory_menu(&inventory,&inventory_current_size,player_x,player_y);
        }
        if(last_key == K_s)
        {
            show_stats(player_atk,player_def,player_lp,player_sp,player_tp,player_max_lp,player_ep,player_max_ep,player_script.get_name());
            tgetch();
        }
        if(last_key == K_t)
        {
            if(weapon_on && player_current_weapon.get_type() == TYPE_THROWABLE)
            {
                if(!player_current_weapon.get_oneusable() && throw_menu(player_current_weapon))
                {
                    player_current_weapon.prouse();
                    inventory[using_weapon_inventory_index].prouse();
                    renew_stats();
                    turn();
                }
            }
        }
        if(last_key == K_e)
        {
            if(player_ep - player_script.get_eq() >= 0)
            {
                if(player_script.get_spec() == SCRIPT_SPAWN)
                {
                    int sx = std::rand() % 3 - 1;
                    int sy = std::rand() % 3 - 1;
                    if(sx == player_x && sy == player_y)
                        sx = -1;
                    player_script.exec(player_x,player_y,player_x + sx,player_y + sy);
                }
                else
                {
                    if(creature_base.size() > 0)
                    {
                        player_script.exec(player_x,player_y,creature_base.begin()->second.get_x(),creature_base.begin()->second.get_y());
                    }
                    else
                        player_script.exec(player_x,player_y,player_x + 10 * (std::rand()%3 - 1) + std::rand() % 13,player_y + 10* (std::rand()%3 - 1) + std::rand() % 13);

                    //system("pause");
                }
                message("SCRIPT EXEC|");
                player_ep -= player_script.get_eq();
                turn();
            }
        }
        if(wave_timer % 10 == 0 && player_ep + 1 <= player_max_ep)
            player_ep++;
        player_lp -= player_hit;
        player_ep += player_hit;
        if(player_ep < 0)
            player_ep = 0;
        if(player_ep > player_max_ep)
            player_ep = player_max_ep;
        player_hit = 0;
        if(player_lp <= 0)
        {
            main_game_running = false;
            gameOver = true;
        }
        if(!quest[4] && miakos_killed >= 5)
        {
            message("KIMICUR AD|");
            put_creature_to_map(CREATURE(creature_stamps[1][5],player_x + 1,player_y + 1,ITEM()),player_x + 1,player_y+1);
            put_creature_to_map(CREATURE(creature_stamps[1][5],player_x - 1,player_y + 1,ITEM()),player_x - 1,player_y+1);
            put_creature_to_map(CREATURE(creature_stamps[1][5],player_x - 1,player_y - 1,ITEM()),player_x - 1,player_y-1);
            put_creature_to_map(CREATURE(creature_stamps[1][5],player_x + 1,player_y - 1,ITEM()),player_x + 1,player_y-1);
            quest[4] = true;
        }
        if(!quest[1] && weapon_on && armor_on && player_current_armor.get_name() == "Coiny's mystery" && player_current_weapon.get_name() == "Mystery of coiny" && coin_count > 0)
        {
            message("GOPA AD|");
            player_current_weapon.set_cursed(true);
            player_current_armor.set_cursed(true);
            player_current_weapon.set_true_atk(6);
            player_current_armor.set_true_def(6);
            weapon_on = true;
            armor_on = true;
            inventory[using_weapon_inventory_index].set_cursed(true);
            inventory[using_weapon_inventory_index].set_true_atk(6);
            inventory[using_armor_inventory_index].set_cursed(true);
            inventory[using_armor_inventory_index].set_true_def(6);
            for(int i = 0 ; i < inventory_current_size; i++)
            {
                if(inventory[i].get_name() == "Coiny's coin")
                {
                    for(int q = i; q < inventory_current_size - 1; q++)
                    {
                        inventory[q] = inventory[q+1];
                    }
                    inventory_current_size--;
                    coin_count--;
                    break;
                }
            }
            quest[1] = true;
            renew_stats();
            /*use_item(inventory[0],&inventory,inventory_current_size,0);
            use_item(inventory[1],&inventory,inventory_current_size,1);*/
        }
        if(!quest[0] && coin_count == 2)
        {
            message("DOUBIL AD|");
            int coin = std::rand() % 100 + 1;
            inventory[0] = inventory[coin % inventory_current_size];
            inventory[0].set_true_atk((inventory[0].get_atk() * (coin % 3)) % 50);
            inventory[0].set_true_def((inventory[0].get_def() * (coin % 3)) % 50);
            weapon_on = false;
            armor_on = false;
            if(coin % 2 == 0)
            {
                inventory[0].set_type(TYPE_ARMOR);
            }
            else
            {
                inventory[0].set_type(TYPE_WEAPON);
            }
            inventory_current_size = 1;
            coin_count = 0;
            quest[0] = true;
        }
        if(!quest[6] && creature_base.size() >= 50)
        {
            message("IFI AD|");
            killers.push_back("sindrom of human's catless");
            apply_effect(EFFECT_HEAL,-100000,&inventory);
            quest[6] = true;
        }
        if(!quest[8] && true);

        renew_stats();
    }
    if(gameOver)
    {
        game_over();
    }
}

#endif // GAME_FUNCTIONS_H
