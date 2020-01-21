#include <iostream>
#include <windows.h>
#include <conio.h>
#include <string>
#include <map>
#include <random>
#include <time.h>
#include <algorithm>
#include <queue>

#include "declarations.h"

#include "basic_lib.h"
#include "item_lib.h"
#include "main_functions.h"
#include "creature_lib.h"
#include "menus.h"
#include "item_resourses.h"
#include "creature_resourses.h"
#include "player_lib.h"
#include "item_functions.h"
#include "creature_functions.h"
#include "script_lib.h"
#include "script_resourses.h"
#include "skills.h"
#include "game_functions.h"

#include "splash_screens.h"

int main(void)
{
    try
    {
        srand(time(NULL));
        prepare();
        prepare_items_library();
        prepare_creature_library();
        loading_start_screen();
        welcome();
        main_menu();
    }
    catch(int e)
    {
        std::cout<<"Some unexp3ct3d behavioru. Reprot 1t";
    }
    return EXIT_SUCCESS;
}
