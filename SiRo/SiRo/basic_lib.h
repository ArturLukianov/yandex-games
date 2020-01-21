#ifndef BASIC_LIB_H
#define BASIC_LIB_H

#define STRLEN(x) (sizeof(x)/sizeof(TCHAR) - 1)

const int BACKGROUND_WHITE = (15<<4);

const int SCREEN_WIDTH = 400;
const int SCREEN_HEIGHT = 400;
const int SCREEN_SYMH = 29;
const int SCREEN_SYMW = 119;

const int TYPE_COLLECTIBLE = 1;
const int TYPE_WEAPON = 2;
const int TYPE_ARMOR = 3;
const int TYPE_POTION = 4;
const int TYPE_THROWABLE = 5;
const int TYPE_BOOK = 6;
const int TYPE_VOLUME = 7;
const int TYPE_SCROLL = 8;
const int TYPE_ARTIFACT = 9;
const int TYPE_MATERIAL = 10;

const int EFFECT_NONE = 0;
const int EFFECT_HEAL = 1;
const int EFFECT_SPUP = 2;
const int EFFECT_TPUP = 3;
const int EFFECT_UNCURSE = 4;
const int EFFECT_CURSE = 5;
const int EFFECT_SPAWN = 6;
const int EFFECT_BLAST = 7;
const int EFFECT_POLYMORPH = 8;

const int inventory_size = 10;

const int K_UP = 72;
const int K_DOWN = 80;
const int K_LEFT = 77;
const int K_RIGHT = 75;
const int K_ENTER = 13;
const int K_KDOWN = 224;
const int K_y = 'y';
const int K_n = 'n';
const int K_q = 'q';
const int K_p = 'p';
const int K_i = 'i';
const int K_s = 's';
const int K_d = 'd';
const int K_c = 'c';
const int K_u = 'u';
const int K_t = 't';
const int K_e = 'e';
const int K_r = 'r';
const int K_z = 'z';

const int boss_multiply_interval = 2;

const int max_level = 5;

const int ANIMATION_ARROW = 1;
const int ANIMATION_WAVE = 2;
const int ANIMATION_AURA = 3;
const int ANIMATION_BEAM = 4;
const int ANIMATION_BOSS = 5;
const int ANIMATION_SPAWN = 6;

const int SCRIPT_ARROW = 1;
const int SCRIPT_WAVE = 2;
const int SCRIPT_BEAM = 3;
const int SCRIPT_SPAWN = 4;

const int EVENT_deviloper = 0;
const int EVENT_coinyrush = 1;

int events_cnt = 2;

const int SCRIPT_TYPE_TARGET = 1;
const int SCRIPT_TYPE_WAVE = 2;

const int INTELLECT_STAY = 1;
const int INTELLECT_STUN = 2;
const int INTELLECT_RANDOM_WEP = 3;
const int INTELLECT_AGGRO_WEP = 4;
const int INTELLECT_HELPER = 5;
const int INTELLECT_RANDOM_SCT = 6;
const int INTELLECT_AGGRO_SCT = 7;
const int INTELLECT_THR = 8;
const int INTELLECT_STUN_SCT = 9;
const int INTELLECT_STUN_THR = 10;
const int INTELLECT_BOSS_BERSERKER = 11;
const int INTELLECT_BOSS_MAGICIAN = 12;
const int INTELLECT_BOSS_NECROMANCER = 13;

const int BOSS_BERSERKER = 0;
const int BOSS_MAGICIAN = 1;
const int BOSS_NECROMANCER = 2;

int intellect_up[] =
{
    0, // none
    INTELLECT_STAY, // stay straight
    INTELLECT_RANDOM_WEP, // stun
    INTELLECT_AGGRO_WEP, // random
    INTELLECT_AGGRO_WEP, // aggro
    INTELLECT_HELPER, // helper
    INTELLECT_AGGRO_SCT, // random scripter
    INTELLECT_AGGRO_SCT, // aggro scripter
    INTELLECT_THR, // thrower
    INTELLECT_RANDOM_SCT, // stun scripter
    INTELLECT_THR, // stun thrower
    INTELLECT_BOSS_BERSERKER,
    INTELLECT_BOSS_MAGICIAN,
    INTELLECT_BOSS_NECROMANCER,
};

int intellect_down[] =
{
    0, // none
    INTELLECT_STAY, // stay straight
    INTELLECT_STUN, // stun
    INTELLECT_STUN, // random
    INTELLECT_STUN, // aggro
    INTELLECT_STUN, // helper
    INTELLECT_STUN_SCT, // random scripter
    INTELLECT_STUN_SCT, // aggro scripter
    INTELLECT_STUN_THR, // thrower
    INTELLECT_STUN_SCT, // stun scripter
    INTELLECT_STUN_THR, // stun thrower
    INTELLECT_BOSS_BERSERKER,
    INTELLECT_BOSS_MAGICIAN,
    INTELLECT_BOSS_NECROMANCER,
};

int script_library_size = 10;

char alphabet[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(){}.></?*;:'[]~`";
int alphabet_size = STRLEN(alphabet);

int field[SCREEN_SYMH][SCREEN_SYMW];
int npc_field[SCREEN_SYMH][SCREEN_SYMW];
int item_field[SCREEN_SYMH][SCREEN_SYMW];
char symbol_code_bk[] = {'.','#','&','*'};
char symbol_code[] = {};
std::string spawnanim[] = {"@", "!", "@", "!", "@", "#"};
int spawnanim_size = 6;

int boss_spawn_turn = 200;

int wave_spawn_coords[][2] = {{1,1},
    {1,SCREEN_SYMH - 2},
    {SCREEN_SYMW - 2,1},
    {SCREEN_SYMW - 2,SCREEN_SYMH - 2}
};
int wave_spawn_coords_size = 4;

int symbol_attr[] = {FOREGROUND_BLUE,
                     FOREGROUND_GREEN,
                     BACKGROUND_WHITE|FOREGROUND_INTENSITY,
                     FOREGROUND_RED | FOREGROUND_BLUE|FOREGROUND_INTENSITY,
                     FOREGROUND_RED | FOREGROUND_INTENSITY
                    };
int creature_type_count = 9;
int wave_timer = 0;
int wave_interval = 100;
int next_wave = 0;
int wave_level = 0;
int wave_count = 0;
int wave_level_up_interval = 8;
int wave_next_level_up = 0;

int dl_sh = 1;
int sl_tm = 100;

int player_lp = 10;
int player_tp = 0;
int player_sp = 1;
int player_def = 0;
int player_atk = 1;
int coin_count = 0;
int player_ep = 10;
int player_max_ep = 10;
int player_max_lp = player_tp * 2 + 10;
bool weapon_on = false;
bool armor_on = false;
int player_x = SCREEN_SYMW / 2;
int player_y = SCREEN_SYMH / 2;
int player_lx = player_x;
int player_ly = player_y;
int player_hit = 0;
int using_weapon_inventory_index = 0;
int using_armor_inventory_index = 0;

std::vector<std::string>killers;

std::string system_message = "|";

bool new_message = false;
bool renew_message = false;
bool quest[100];
int quest_cnt = 13;
std::string quest_name[] = {"Double bill?",
                            "Golden paladin$",
                            "Kill or be killed!",
                            "You are not Prepared!",
                            "Killing miakoes is cruel.",
                            "I is your best helper!",
                            "I feel icky.",
                            "PROJECTGR$DE1",
                            "Glut you!",
                            "Will your lips taste the kiss of death?",
                            "But why?",
                            "Fun guy!!!",
                            "I will hurt you down!"
                           };

std::string main_menu_options[] = {"Start",
                                   "Help",
                                   "Credits",
                                   "Quit"
                                  };

std::string help[] = {  "This is help file",
                        "AKTC - Any Key To Continue",
                        "DFS - Deep-First Search",
                        "LP - Life Points",
                        "SP - Strength Points",
                        "TP - Toughtness Points",
                        "EO* - End Of *",
                        "DLSA - Developer Loves Stupid Abbrevations",
                        "ETC - Enter To Continue",
                        "------EOH------",
                        "<AKTC>"
                     };

std::string quit_info[] = {  "DO YOU REALLY WANT TO QUIT???",
                             "<y> - to continue",
                             "<n> - to decline"
                          };
std::string credits[] = {   "SiRo(SImple ROgue) 2018-2019",
                            "Music by B@GCAT",
                            "Gameplay by B@GCAT",
                            "Humour by B@GCAT",
                            "Developer - B@GCAT",
                            "Quests - Vertig1, B@GCAT",
                            "",
                            "[::]",
                            "<AKTC>"
                        };
std::string game_over_text[] = {   "GAME OVER",
                                   "<ETC>"
                               };

std::string tips[] = {"Why coiny?",
                      "Is I strong?",
                      "Don't cheat! Bigcat is watching you!",
                      "Can you solve the mystery?",
                      "Ok, Qooqle, how to hack SiRo?",
                      "There is no easter eggs, I think",
                      "GUI or not GUI?",
                      "Deviloper is always near.",
                      "gelgbpngpuzr",
                      "13 is number of knowledge"
                     };

int main_menu_options_length = 4;
int help_length = 11;
int quit_info_length = 3;
int credits_length = 9;
int game_over_text_length = 2;
int tips_length = 10;

int miakos_killed = 0;

HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
LPCSTR TITLE = "SiRo 2018-2019";


std::string name_slogs[] =
{
    "LO",
    "PO",
    "TO",
    "TA",
    "KU",
    "KO",
    "R"
};

int name_slogs_size = 7;


void clear_console()
{
    COORD topLeft  = { 0, 0 };
    CONSOLE_SCREEN_BUFFER_INFO screen;
    DWORD written;

    GetConsoleScreenBufferInfo(hConsole, &screen);
    FillConsoleOutputCharacterA(
        hConsole, ' ', screen.dwSize.X * screen.dwSize.Y, topLeft, &written
    );
    FillConsoleOutputAttribute(
        hConsole, FOREGROUND_GREEN | FOREGROUND_RED | FOREGROUND_BLUE,
        screen.dwSize.X * screen.dwSize.Y, topLeft, &written
    );
    SetConsoleCursorPosition(hConsole, topLeft);
}

void hide_cursor()
{
    COORD topLeft  = { SCREEN_SYMW, SCREEN_SYMH };
    SetConsoleCursorPosition(hConsole, topLeft);
}

void draw_frame()
{
    clear_console();
    TCHAR frame[SCREEN_SYMH * (SCREEN_SYMW+1)];
    int last_char = 0;
    for(int i = 0; i < SCREEN_SYMH; i++)
    {
        for(int j = 0 ; j < SCREEN_SYMW ; j ++)
        {
            if(i == 0 && j == 0)
            {
                frame[last_char++] = 'O';
            }
            else if(i == SCREEN_SYMH - 1 && j == 0)
            {
                frame[last_char++] = 'O';
            }
            else if(i == 0 && j == SCREEN_SYMW- 1)
            {
                frame[last_char++] = 'O';
            }
            else if(i == SCREEN_SYMH - 1 && j == SCREEN_SYMW- 1)
            {
                frame[last_char++] = 'O';
            }
            else if(j == 0 || j == SCREEN_SYMW-1)
            {
                frame[last_char++] = '|';
            }
            else if(i == 0 || i == SCREEN_SYMH-1)
            {
                frame[last_char++] = '=';
            }
            else
            {
                frame[last_char++] = ' ';
            }
        }
        frame[last_char++] = '\n';
    }
    DWORD dwBuff;
    WriteConsole(hConsole,&frame,STRLEN(frame),&dwBuff,NULL);
    hide_cursor();
}

void write_line(std::string line, int x, int y)
{
    DWORD dwBuff;
    COORD topLeft  = { x, y };
    SetConsoleCursorPosition(hConsole, topLeft);
    TCHAR item_line[line.size()+1];
    for(int j = 0 ; j <= line.size(); j++)
    {
        item_line[j] = line[j];
    }
    WriteConsole(hConsole,&item_line,STRLEN(item_line),&dwBuff,NULL);
}

void write_line_attr(std::string line, int x, int y,DWORD attr)
{
    DWORD dwBuff;
    COORD topLeft  = { x, y };
    SetConsoleCursorPosition(hConsole, topLeft);
    TCHAR item_line[line.size()+1];
    for(int j = 0 ; j <= line.size(); j++)
    {
        item_line[j] = line[j];
    }
    SetConsoleTextAttribute(hConsole,attr);
    WriteConsole(hConsole,&item_line,STRLEN(item_line),&dwBuff,NULL);
    SetConsoleTextAttribute(hConsole,15);
}

int tgetch()
{
    int key = getch();
    if(key == K_KDOWN)
    {
        key = getch();
    }
    return key;
}

std::string int_to_string(int n,bool zn)
{
    std::string result = "";
    std::string minusr = "+";
    if(n < 0)
        minusr="-";
    n = std::abs(n);
    while(n > 0)
    {
        result+=(n%10)+'0';
        n/=10;
    }
    std::reverse(result.begin(),result.end());
    if(zn)
    {
        minusr+=result;
        if(minusr != "+")
            return minusr;
        return "+0";
    }
    else
    {
        if(minusr == "-")
            result = minusr + result;
        if(result != "")
            return result;
        return "0";
    }
}

std::string type_to_string(int type)
{
    if(type == TYPE_WEAPON)
    {
        return "WEP";
    }
    if(type == TYPE_ARMOR)
    {
        return "ARM";
    }
    if(type == TYPE_COLLECTIBLE)
    {
        return "COL";
    }
    if(type == TYPE_POTION)
    {
        return "POT";
    }
    if(type == TYPE_THROWABLE)
    {
        return "THR";
    }
    if(type == TYPE_BOOK)
    {
        return "BOK";
    }
    if(type == TYPE_VOLUME)
    {
        return "VOL";
    }
    return "NON";
}


#endif // BASIC_LIB_H
