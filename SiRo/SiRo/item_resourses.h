#ifndef ITEM_RESOURSES_H
#define ITEM_RESOURSES_H

std::map<int,std::vector<ITEM> >item_stamps;

std::pair<int,ITEM> item_library[] =
{
    {1,ITEM("Paper folded excalibur",TYPE_WEAPON,1,0,1)},
    {1,ITEM("Qq clothes",TYPE_ARMOR,0,3,1)},
    {1,ITEM("Not great kitchen knife",TYPE_WEAPON,3,0,1)},
    {1,ITEM("Net armor",TYPE_ARMOR,0,2,1)},
    {1,ITEM("Armor of nothihg",TYPE_ARMOR,0,0,1)},
    {1,ITEM("Old hatword",TYPE_WEAPON,10,0,1)},
    {1,ITEM("Armor of dirt",TYPE_ARMOR,0,1,1)},
    {1,ITEM("Mystery of coiny",TYPE_WEAPON,-5,0,1)},
    {1,ITEM("Coiny's mystery",TYPE_ARMOR,0,-5,1)},
    {1,ITEM("Sunny day",TYPE_ARMOR,0,10,1)},
    {1,ITEM("Saint cookie",TYPE_POTION,1,true,EFFECT_HEAL,10)},
    {1,ITEM("Dark elefish bone",TYPE_POTION,1,true,EFFECT_SPUP,1)},
    {1,ITEM("Coiny's bronze muscle",TYPE_POTION,1,true,EFFECT_TPUP,1)},
    {1,ITEM("Coiny's coin",TYPE_COLLECTIBLE,0,0,1)},
    {1,ITEM("ReveR SeS",TYPE_WEAPON,30,0,10)},
    {1,ITEM("Armor of armor",TYPE_ARMOR,0,40,10)},
    {1,ITEM("Desruc eye",TYPE_POTION,1,true,EFFECT_UNCURSE,1)},
    {1,ITEM("Old eggrave",TYPE_POTION,1,true,EFFECT_SPUP,-1)},
    {1,ITEM("Cheap choco",TYPE_POTION,1,true,EFFECT_TPUP,-1)},
    {1,ITEM("Clown's hatrat",TYPE_POTION,1,true,EFFECT_HEAL,-10)},
    {1,ITEM("Desruc eye",TYPE_POTION,1,true,EFFECT_CURSE,1)},
    {1,ITEM("P?O?T?O?N",TYPE_POTION,1,true,EFFECT_HEAL,2)},
    {1,ITEM("P?O?T?O?N",TYPE_POTION,1,true,EFFECT_SPUP,2)},
    {1,ITEM("P?O?T?O?N",TYPE_POTION,1,true,EFFECT_TPUP,2)},
    {1,ITEM("P?O?T?O?N",TYPE_POTION,1,true,EFFECT_UNCURSE,2)},
    {1,ITEM("P?O?T?O?N",TYPE_POTION,1,true,EFFECT_HEAL,-2)},
    {1,ITEM("P?O?T?O?N",TYPE_POTION,1,true,EFFECT_SPUP,-2)},
    {1,ITEM("P?O?T?O?N",TYPE_POTION,1,true,EFFECT_TPUP,-2)},
    {1,ITEM("P?O?T?O?N",TYPE_POTION,1,true,EFFECT_CURSE,-2)},
    {1,ITEM("P?O?T?O?N",TYPE_POTION,1,true,EFFECT_POLYMORPH,2)},
    {1,ITEM("Challenge down",TYPE_POTION,1,true,EFFECT_SPAWN,2)},
    {1,ITEM("beta oxygen myphril booster",TYPE_POTION,1,true,EFFECT_BLAST,2)},
    {1,ITEM("hyper beta oxygen myphril booster",TYPE_POTION,1,true,EFFECT_BLAST,-5)},
    {1,ITEM("myphrill oxygen rust pyro hallow",TYPE_POTION,1,true,EFFECT_POLYMORPH,10)},
    {1,ITEM("Why?",TYPE_POTION,1,false,std::rand()%9,std::rand()%10 - 5)},
    {1,ITEM("Ethink",TYPE_THROWABLE,3,0,3,1,3)},
    {1,ITEM("MAEB?RESAL!",TYPE_THROWABLE,10,0,100,1,1)},
    {1,ITEM("CUBE00",TYPE_BOOK,0)},
    {1,ITEM("CUBE01",TYPE_BOOK,1)},
    {1,ITEM("CUBE02",TYPE_BOOK,2)},
    {1,ITEM("CUBE03",TYPE_BOOK,3)},
    {1,ITEM("CUBEST",TYPE_COLLECTIBLE,3)},
    {1,ITEM("CUBE04",TYPE_BOOK,4)},
    {1,ITEM("CUBE05",TYPE_BOOK,5)},
    {1,ITEM("CUBE06",TYPE_BOOK,6)},
    {1,ITEM("CUBE07",TYPE_BOOK,7)},
    {1,ITEM("CUBE08",TYPE_BOOK,8)},
    {1,ITEM("Int cookie",TYPE_POTION,1,true,EFFECT_HEAL,10000)},
    {1,ITEM("¶",TYPE_ARMOR,1,1,1)},
    {1,ITEM("~",TYPE_WEAPON,-100,-100,100)},
    {1,ITEM("mint",TYPE_BOOK,9)},
};

int item_library_size = 51;

void prepare_items_library()
{
    for(int i = 0; i < item_library_size; i ++)
    {
        item_stamps[item_library[i].first].push_back(item_library[i].second);
    }
}

#endif // ITEM_RESOURSES
