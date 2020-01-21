#ifndef DECLARATIONS_H
#define DECLARATIONS_H

void prepare();
void welcome();
void main_menu();
void start_game();
void game_over();
void end_menu();
void help_out();
void credits_out();
void quit();
void quit_to_main_menu();
void clear_console();
void hide_cursor();
void message_out();
void message(std::string msg);
void draw_frame();
void show_stats(int atk,int def,int lp,int sp,int tp);
void redraw_screen();
void deal_true_damage(int mon_id,int atk);
void zap_spell(int spell_num,int sx,int sy,int tx,int ty);
std::pair<int,int> get_nearest_hostile(int creature_x,int creature_y);
void spawn_creature(std::string name,int hp,int atk,int spd,int lvl,int rep,int x,int y,char sym);
void move_player(int nx, int ny);

#endif // DECLARATIONS_H
