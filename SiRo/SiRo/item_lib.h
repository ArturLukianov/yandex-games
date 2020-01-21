#ifndef ITEM_LIB_H
#define ITEM_LIB_H

class ITEM
{

    std::string item_name;
    int item_type;
    int item_atk,item_def;
    bool in_use;
    bool hidden;
    int item_lvl;
    bool item_oneusable;
    int item_effect;
    int item_effect_str;
    bool item_cursed;
    bool item_empty;
    int item_range;
    int item_usecount = 0;
    int item_learn;
public:
    ITEM(std::string name, int type, int lvl, bool oneuseable,int effect,int effect_str)
    {
        item_name = name;
        item_type = type;
        item_lvl = lvl;
        in_use = false;
        hidden = true;
        item_usecount = -1;
        item_oneusable = oneuseable;
        item_effect = effect;
        item_effect_str = effect_str;
        item_empty = false;
    }
    ITEM(std::string name, int type, int atk, int def,int lvl)
    {
        item_name = name;
        item_type = type;
        item_atk = atk;
        item_def = def;
        item_lvl = lvl;
        in_use = false;
        hidden = true;
        item_usecount = -1;
        item_oneusable = false;
        item_cursed = ((std::rand()%100+1)>=60?true:false);
        item_empty = false;
    }
    ITEM(std::string name, int type, int atk, int def,int range,int lvl,int usecount)
    {
        item_name = name;
        item_type = type;
        item_atk = atk;
        item_def = def;
        item_lvl = lvl;
        in_use = false;
        hidden = true;
        item_usecount = usecount;
        item_range = range;
        item_oneusable = false;
        item_cursed = ((std::rand()%100+1)>=60?true:false);
        item_empty = false;
    }
    ITEM(std::string name, int type, int script_learn)
    {
        item_name = name;
        item_type = type;
        in_use = false;
        item_usecount = -1;
        hidden = true;
        item_oneusable = true;
        item_learn = script_learn;
        item_cursed = ((std::rand()%100+1)>=60?true:false);
        item_empty = false;
    }
    ITEM()
    {
        item_empty = true;
    }
    std::string get_name()
    {
        return item_name;;
    }
    int get_learn(){
        return item_learn;
    }
    void rcurse(){
        item_cursed = ((std::rand()%100+1)>=60?true:false);
    }
    int get_type()
    {
        return item_type;
    }
    int get_effect_str()
    {
        return item_effect_str;
    }
    bool get_cursed()
    {
        return item_cursed;
    }
    void set_cursed(bool zn)
    {
        item_cursed = zn;
    }
    int get_stat()
    {
        if(item_type == TYPE_THROWABLE){
            return item_usecount;
        }
        if(item_type == TYPE_WEAPON)
        {
            return item_atk;
        }
        if(item_type == TYPE_ARMOR)
        {
            return item_def;
        }
        if(item_type == TYPE_BOOK)
        {
            return item_learn;
        }
        return 0;
    }
    bool get_oneusable()
    {
        if(item_usecount == -1)
            return item_oneusable;
        else if(item_usecount == 0)
            return true;
        else{
            return false;
        }
    }
    int get_effect()
    {
        return item_effect;
    }
    void prouse(){
        if(item_usecount != -1)item_usecount--;
    }
    bool is_hidden()
    {
        return hidden;
    }
    bool empty(){
        return item_empty;
    }
    void unhide()
    {
        hidden = false;
    }
    std::string get_stat_name()
    {
        if(item_type == TYPE_THROWABLE)
        {
            return "UCN";
        }
        if(item_type == TYPE_WEAPON)
        {
            return "ATK";
        }
        if(item_type == TYPE_ARMOR)
        {
            return "DEF";
        }
        if(item_type == TYPE_BOOK)
        {
            return "LRN";
        }
        return "";
    }
    void set_type(int type){
        item_type = type;
    }
    bool is_using()
    {
        return in_use;
    }
    void use()
    {
        if(item_type == TYPE_WEAPON || item_type == TYPE_ARMOR || item_type == TYPE_THROWABLE)
            in_use = !in_use;
        unhide();
    }
    int get_atk()
    {
        return item_atk;
    }
    int get_rng()
    {
        return item_range;
    }
    int get_def()
    {
        return item_def;
    }
    void deselect()
    {
        in_use = false;
    }
    void set_atk(int atk)
    {
        item_atk -= atk;
    }
    void set_true_atk(int atk)
    {
        item_atk=atk;
    }
    void set_true_def(int def)
    {
        item_def=def;
    }
    void set_def(int def)
    {
        item_def -= def;
    }
    int get_level()
    {
        return item_lvl;
    }
};

#endif // ITEM_LIB_H
