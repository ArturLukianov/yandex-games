#ifndef ITEM_FUNCTIONS
#define ITEM_FUNCTIONS


std::map<int,ITEM>item_base;
int l_base_id = 1;
int put_item_to_map(ITEM item, int x, int y)
{
    if(x > 0 && y > 0 && x < SCREEN_SYMW && y < SCREEN_SYMH && item_field[y][x] == 0 && field[y][x] != 1 && !item.empty())
    {
        item_field[y][x] = l_base_id;
        item_base[l_base_id] = item;
        return l_base_id++;
    }
    return -1;
}

ITEM get_item_from_base(int id)
{
    return item_base[id];
}

bool put_item_to_inventory(ITEM (*inventory)[inventory_size],ITEM item,int inventory_current_size)
{
    (*inventory)[inventory_current_size] = ITEM(item);
    return true;
}

bool pick_up(ITEM (*inventory)[inventory_size],int inventory_current_size,int x,int y)
{
    if(item_field[y][x] != 0 && inventory_current_size < inventory_size)
    {
        put_item_to_inventory(inventory,get_item_from_base(item_field[y][x]),inventory_current_size);
        item_base.erase(item_field[y][x]);
        item_field[y][x] = 0;
        message("P:" + (*inventory)[inventory_current_size].get_name() + "t:" + type_to_string((*inventory)[inventory_current_size].get_type()) + "|");
        return true;
    }
    return false;
}

int inventory_select_item(std::string title,ITEM (*inventory)[inventory_size], int current_inventory_size)
{
    bool selecting_item = 1;
    int cursor_pos = 0;
    while(selecting_item)
    {
        draw_frame();
        for(int i = 0; i < current_inventory_size; i ++)
        {
            std::string s_inventory_item = int_to_string(i+1,false);
            int y = (i+1);
            while(y < 1000)
            {
                s_inventory_item+=" ";
                y*=10;
            }
            s_inventory_item += " : ";
            s_inventory_item += (*inventory)[i].get_name();
            s_inventory_item += " : ";
            s_inventory_item += type_to_string((*inventory)[i].get_type());
            if((*inventory)[i].get_type() != TYPE_POTION && (*inventory)[i].get_type() != TYPE_COLLECTIBLE)
            {
                s_inventory_item += " : ";
                if((*inventory)[i].is_hidden())
                {
                    s_inventory_item+="???";
                }
                else
                {
                    s_inventory_item += (*inventory)[i].get_stat_name();
                    s_inventory_item += int_to_string((*inventory)[i].get_stat(),true);
                    if((*inventory)[i].get_cursed())
                    {
                        s_inventory_item += " : CURSED";
                    }
                }
                if((*inventory)[i].is_using())
                {
                    s_inventory_item += " : USING";
                }
            }
            if(cursor_pos == i)
                write_line_attr(s_inventory_item,1,2+i, FOREGROUND_BLUE|FOREGROUND_RED|FOREGROUND_INTENSITY);
            else
                write_line(s_inventory_item,1,2+i);
        }
        write_line_attr(title,1,1,FOREGROUND_BLUE|FOREGROUND_INTENSITY);
        if(cursor_pos == current_inventory_size)
            write_line_attr("CANCEL",1,2 + current_inventory_size,FOREGROUND_BLUE|FOREGROUND_RED|FOREGROUND_INTENSITY);
        else
            write_line("CANCEL",1,2 + current_inventory_size);
        std::string cursor = "<--- [";
        if(cursor_pos < current_inventory_size)
        {
            cursor += int_to_string(cursor_pos+1,false);
            cursor += "]";
        }
        else
        {
            cursor += "CANCEL]";
        }
        write_line_attr(cursor,100,2 + cursor_pos,FOREGROUND_RED | FOREGROUND_GREEN|FOREGROUND_INTENSITY);
        message_out();
        hide_cursor();
        int key = tgetch();
        if(key == K_UP)
        {
            cursor_pos--;
        }
        if(key == K_DOWN)
        {
            cursor_pos++;
        }
        if(key == K_ENTER)
        {
            selecting_item = 0;
        }
        if(cursor_pos < 0)
        {
            cursor_pos = current_inventory_size;
        }
        if(cursor_pos > current_inventory_size)
        {
            cursor_pos = 0;
        }
    }
    if(cursor_pos == current_inventory_size)
    {
        return -1;
    }
    else
    {
        return cursor_pos;
    }
}

void show_inventory(ITEM (*inventory)[inventory_size], int current_inventory_size)
{
    draw_frame();
    for(int i = 0; i < current_inventory_size; i ++)
    {
        std::string s_inventory_item = int_to_string(i+1,false);
        int y = (i+1);
        while(y < 1000)
        {
            s_inventory_item+=" ";
            y*=10;
        }
        s_inventory_item += " : ";
        s_inventory_item += (*inventory)[i].get_name();
        s_inventory_item += " : ";
        s_inventory_item += type_to_string((*inventory)[i].get_type());
        DWORD item_col = 15;
        if((*inventory)[i].get_type() != TYPE_POTION && (*inventory)[i].get_type() != TYPE_COLLECTIBLE)
        {
            s_inventory_item += " : ";
            if((*inventory)[i].is_hidden())
            {
                s_inventory_item+="???";
            }
            else
            {
                s_inventory_item += (*inventory)[i].get_stat_name();
                s_inventory_item += int_to_string((*inventory)[i].get_stat(),true);
                if((*inventory)[i].get_cursed())
                {
                    s_inventory_item += " : CURSED";
                    item_col = FOREGROUND_RED | 15 |  FOREGROUND_INTENSITY;
                }
            }
            if((*inventory)[i].is_using())
            {
                s_inventory_item += " : USING";
                if((*inventory)[i].get_cursed())
                {
                    item_col = FOREGROUND_GREEN | FOREGROUND_RED;
                }
                else
                {
                    item_col = FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY;
                }
            }
        }
        write_line_attr(s_inventory_item,1,1+i,item_col);
    }
    if(current_inventory_size == 0)
    {
        write_line_attr("EMPTY",1,1,15 | FOREGROUND_INTENSITY);
    }
    message_out();
    hide_cursor();
}

#endif // ITEM_FUNCTIONS
