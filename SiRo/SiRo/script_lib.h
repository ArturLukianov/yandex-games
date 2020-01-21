#ifndef SCRIPT_LIB_H
#define SCRIPT_LIB_H

class ANIMATION
{
    int anim_num;
    DWORD anim_col;
public:
    ANIMATION()
    {

    }
    ANIMATION(int num,DWORD color)
    {
        anim_num = num;
        anim_col = color;
    }
    void play(int tx,int ty)
    {
        for(std::map<int,CREATURE>::iterator it = creature_base.begin(); it != creature_base.end(); it++)
        {
            DWORD ste = FOREGROUND_BLUE * (std::rand() % 2) | FOREGROUND_RED * (std::rand() % 2) | FOREGROUND_GREEN * (std::rand() % 2) | BACKGROUND_BLUE * (std::rand() % 2) | BACKGROUND_RED * (std::rand() % 2) | BACKGROUND_GREEN * (std::rand() % 2) | FOREGROUND_INTENSITY | BACKGROUND_INTENSITY;
            int x = it->second.get_x();
            int y = it->second.get_y();
            while(x != tx || y != ty)
            {
                int sx = 0;
                int sy = 0;
                if(x < tx)
                {
                    x++;
                    sx = 1;
                }
                else if(x > tx)
                {
                    x--;
                    sx = -1;
                }
                if(y < ty)
                {
                    y++;
                    sy = 1;
                }
                else if(y > ty)
                {
                    y--;
                    sy = -1;
                }
                std::string arr_sym;
                if(sx == 0 && sy == 0)
                {
                    arr_sym = "&";
                }
                else if(sx == 1 && sy == 1)
                {
                    arr_sym = "\\";
                }
                else if(sx == -1 && sy == -1)
                {
                    arr_sym = "\\";
                }
                else if(sx == 1 && sy == -1)
                {
                    arr_sym = "/";
                }
                else if(sx == -1 && sy == 1)
                {
                    arr_sym = "/";
                }
                else if(sx == 0)
                {
                    arr_sym = "|";
                }
                else if(sy == 0)
                {
                    arr_sym = "-";
                }
                write_line_attr(arr_sym,x,y,ste);
                Sleep(sl_tm / 100);
            }
        }
    }
    void play(int x,int y,int tx, int ty)
    {
        int sh = 0;
        switch(anim_num)
        {
        case ANIMATION_ARROW:
            while(x != tx || y != ty)
            {
                int sx = 0;
                int sy = 0;
                if(x < tx)
                {
                    x++;
                    sx = 1;
                }
                else if(x > tx)
                {
                    x--;
                    sx = -1;
                }
                if(y < ty)
                {
                    y++;
                    sy = 1;
                }
                else if(y > ty)
                {
                    y--;
                    sy = -1;
                }
                std::string arr_sym;
                if(npc_field[y][x] != 0)
                {
                    arr_sym = "%";
                    break;
                }
                if(field[y][x] != 0)
                {
                    arr_sym = "%";
                    break;
                }
                if(sx == 0 && sy == 0)
                {
                    arr_sym = "%";
                }
                else if(sx == 1 && sy == 1)
                {
                    arr_sym = "\\";
                }
                else if(sx == -1 && sy == -1)
                {
                    arr_sym = "\\";
                }
                else if(sx == 1 && sy == -1)
                {
                    arr_sym = "/";
                }
                else if(sx == -1 && sy == 1)
                {
                    arr_sym = "/";
                }
                else if(sx == 0)
                {
                    arr_sym = "|";
                }
                else if(sy == 0)
                {
                    arr_sym = "-";
                }
                if(sh++ % dl_sh == 0)
                {
                    redraw_screen();
                }
                write_line_attr(arr_sym,x,y,anim_col);
            }
            break;
        case ANIMATION_BEAM:
            while(x != tx || y != ty)
            {
                int sx = 0;
                int sy = 0;
                if(x < tx)
                {
                    x++;
                    sx = 1;
                }
                else if(x > tx)
                {
                    x--;
                    sx = -1;
                }
                if(y < ty)
                {
                    y++;
                    sy = 1;
                }
                else if(y > ty)
                {
                    y--;
                    sy = -1;
                }
                std::string arr_sym;
                if(field[y][x] != 0)
                {
                    arr_sym = "%";
                    break;
                }
                if(item_field[y][x] != 0)
                {
                    arr_sym = "@";
                }
                else if(npc_field[y][x] != 0)
                {
                    arr_sym = "@";
                }
                else if(sx == 0 && sy == 0)
                {
                    arr_sym = "^";
                }
                else if(sx == 1 && sy == 1)
                {
                    arr_sym = "\\";
                }
                else if(sx == -1 && sy == -1)
                {
                    arr_sym = "\\";
                }
                else if(sx == 1 && sy == -1)
                {
                    arr_sym = "/";
                }
                else if(sx == -1 && sy == 1)
                {
                    arr_sym = "/";
                }
                else if(sx == 0)
                {
                    arr_sym = "|";
                }
                else if(sy == 0)
                {
                    arr_sym = "-";
                }
                write_line_attr(arr_sym,x,y,anim_col);
            }
            Sleep(sl_tm);
            redraw_screen();
            break;
        default:
            break;
        }
    }
    void play(int x,int y,int ran)
    {
        int sh = 0 ;
        switch(anim_num)
        {
        case ANIMATION_WAVE:
            for(int i = 1 ; i <= ran; i++)
            {
                for(int j = std::max(0,x - i); j <= std::min(SCREEN_SYMW-1,x + i); j++)
                    write_line_attr("w",j,std::max(0,y-i),anim_col);
                for(int j = std::max(0,x - i); j <= std::min(SCREEN_SYMW-1,x + i); j++)
                    write_line_attr("w",j,std::min(SCREEN_SYMH-1,y+i),anim_col);
                for(int j = std::max(0,y - i); j <= std::min(SCREEN_SYMH-1,y + i); j++)
                    write_line_attr("w",std::max(0,x-i),j,anim_col);
                for(int j = std::max(0,y - i); j <= std::min(SCREEN_SYMH-1,y + i); j++)
                    write_line_attr("w",std::min(SCREEN_SYMW-1,x+i),j,anim_col);
                if(sh++ % dl_sh == 0)
                    Sleep(sl_tm / 100);
                redraw_screen();
            }
            break;
        case ANIMATION_AURA:
            write_line_attr("O",x-1,y-1,anim_col);
            write_line_attr("O",x-1,y+1,anim_col);
            write_line_attr("O",x+1,y-1,anim_col);
            write_line_attr("O",x+1,y+1,anim_col);
            write_line_attr("O",x,y-1,anim_col);
            write_line_attr("O",x,y+1,anim_col);
            write_line_attr("O",x-1,y,anim_col);
            write_line_attr("O",x+1,y,anim_col);
            Sleep(sl_tm / 10);
            redraw_screen();
            break;
        case ANIMATION_SPAWN:ANIMATION_SPAWN:
            for(int i = 0; i < spawnanim_size; i++){
                write_line_attr(spawnanim[i], x, y, anim_col);
                Sleep(sl_tm / 100);
            }
        default:
            break;
        }
    }
};

class SCRIPT
{
    ANIMATION s_anim;
    int s_num;
    int s_str;
    int s_eff;
    int s_type;
    int s_eq;
    int s_cnt;
    int s_rng;
    std::string s_name;
    CREATURE_STAMP spawning_c;
public:
    SCRIPT()
    {
    }
    SCRIPT(std::string name,int anim_num,DWORD anim_col,int num,int eq,CREATURE_STAMP spawning_cc){
        s_anim = ANIMATION(anim_num,anim_col);
        s_num = num;
        s_eq = eq;
        s_name = name;
        s_type = SCRIPT_TYPE_TARGET;
        spawning_c = spawning_cc;
    }
    SCRIPT(std::string name,int anim_num,DWORD anim_col,int num,int str,int eff,int eq,int cnt,int rng)
    {
        s_anim = ANIMATION(anim_num,anim_col);
        s_num = num;
        s_eq = eq;
        s_str = str;
        s_eff = eff;
        s_cnt = cnt;
        s_name = name;
        s_rng = rng;
        if(s_num == SCRIPT_ARROW || s_num == SCRIPT_BEAM)
        {
            s_type = SCRIPT_TYPE_TARGET;
        }
        else
        {
            s_type = SCRIPT_TYPE_WAVE;
        }
    }
    std::string get_name()
    {
        return s_name;
    }
    int get_type()
    {
        return s_type;
    }
    int get_rng()
    {
        return s_rng;
    }
    void exec(int x,int y,int tx,int ty)
    {
        if(s_num == SCRIPT_SPAWN){
            CREATURE spawn_creat = CREATURE(spawning_c,tx,ty,ITEM());
            put_creature_to_map(spawn_creat,tx,ty);
            return;
        }
        for(int i = 0 ; i < s_cnt; i++)
        {
            int sh = 0;
            s_anim.play(x,y,tx,ty);
            switch(s_num)
            {
            case SCRIPT_ARROW:
                while(x != tx || y != ty)
                {
                    if(x < tx)
                    {
                        x++;
                    }
                    else if(x > tx)
                    {
                        x--;
                    }
                    if(y < ty)
                    {
                        y++;
                    }
                    else if(y > ty)
                    {
                        y--;
                    }
                    if(field[y][x] != 0)
                    {
                        break;
                    }
                    if(npc_field[y][x] != 0)
                    {
                        if(sh != 0 && npc_field[y][x] == -1)
                        {
                            player_hit += s_str;
                        }
                        else
                        {
                            creature_base[npc_field[y][x]].deal_damage(s_str);
                        }
                        redraw_screen();
                        break;
                    }
                    sh++;
                }
                break;
            case SCRIPT_BEAM:
                while(x != tx || y != ty)
                {
                    int sx = 0;
                    int sy = 0;
                    if(x < tx)
                    {
                        x++;
                        sx = 1;
                    }
                    else if(x > tx)
                    {
                        x--;
                        sx = -1;
                    }
                    if(y < ty)
                    {
                        y++;
                        sy = 1;
                    }
                    else if(y > ty)
                    {
                        y--;
                        sy = -1;
                    }
                    if(field[y][x] != 0)
                    {
                        break;
                    }
                    if(npc_field[y][x] != 0)
                    {
                        if(sh != 0 && npc_field[y][x] == -1)
                        {
                            player_hit += s_str;
                        }
                        else
                        {
                            creature_base[npc_field[y][x]].deal_damage(s_str);
                        }
                    }
                    sh ++;
                }
                break;
            default:
                exec(x,y);
            }
        }
    }
    int get_eq()
    {
        return s_eq;
    }
    void exec(int x,int y)
    {
        int ran = s_rng;
        for(int i = 0 ; i < s_cnt; i++)
        {
            s_anim.play(x,y,ran);
            switch(s_num)
            {
            case SCRIPT_WAVE:
                for(int i = 1 ; i <= ran; i++)
                {
                    for(int j = std::max(0,x - i); j <= std::min(SCREEN_SYMW-1,x + i); j++)
                    {
                        int nm = npc_field[std::max(0,y-i)][j];
                        if(nm > 0)
                        {
                            creature_base[nm].deal_damage(s_str);
                        }
                        if(nm == -1)
                        {
                            player_hit += s_str;
                        }
                    }

                    for(int j = std::max(0,x - i); j <= std::min(SCREEN_SYMW-1,x + i); j++)
                    {
                        int nm = npc_field[std::min(SCREEN_SYMH-1,y+i)][j];
                        if(nm > 0)
                        {
                            creature_base[nm].deal_damage(s_str);
                        }
                        if(nm == -1)
                        {
                            player_hit += s_str;
                        }
                    }
                    for(int j = std::max(0,y - i); j <= std::min(SCREEN_SYMH-1,y + i); j++)
                    {
                        int nm = npc_field[j][std::max(0,x-i)];
                        if(nm > 0)
                        {
                            creature_base[nm].deal_damage(s_str);
                        }
                        if(nm == -1)
                        {
                            player_hit += s_str;
                        }
                    }
                    for(int j = std::max(0,y - i); j <= std::min(SCREEN_SYMH-1,y + i); j++)
                    {
                        int nm = npc_field[j][std::min(SCREEN_SYMW-1,x+i)];
                        if(nm > 0)
                        {
                            creature_base[nm].deal_damage(s_str);
                        }
                        if(nm == -1)
                        {
                            player_hit += s_str;
                        }
                    }
                }
                break;
            default:
                break;
            }
        }
    }
    int get_spec(){
        return s_num;
    }
};

SCRIPT player_script;

#endif // SCRIPT_LIB_H
