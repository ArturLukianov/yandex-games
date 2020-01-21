#ifndef SPLASH_SCREENS_H
#define SPLASH_SCREENS

char cursor_loading[] = "/|\\-";

int load_line_sl_tm = 10;

void loading_start_screen1(){
    clear_console();
    draw_frame();
    write_line_attr("SiRo2018 Loading...",1,1,FOREGROUND_RED | FOREGROUND_INTENSITY);
    write_line_attr("[                  ] Splashing screens...",1,2,FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    for(int i = 0 ; i <  18; i++){
        write_line_attr(">",2 + i,2,FOREGROUND_BLUE | FOREGROUND_INTENSITY);
        Sleep(load_line_sl_tm);
    }
    write_line_attr("[                  ] Making visibility of work...",1,3,FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    for(int i = 0 ; i <  18; i++){
        write_line_attr(">",2 + i,3,FOREGROUND_BLUE | FOREGROUND_INTENSITY);
        Sleep(load_line_sl_tm);
    }
    write_line_attr("[                  ] Waiting for loading NULL to nullptr...",1,4,FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    for(int i = 0 ; i <  18; i++){
        write_line_attr(">",2 + i,4,FOREGROUND_BLUE | FOREGROUND_INTENSITY);
        Sleep(load_line_sl_tm);
    }
    write_line_attr("[                  ] Welcoming you...",1,5,FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    for(int i = 0 ; i <  18; i++){
        write_line_attr(">",2 + i,5,FOREGROUND_BLUE | FOREGROUND_INTENSITY);
        Sleep(load_line_sl_tm);
    }
    write_line_attr("[ANY KEY TO CONTINUE]",50,19,FOREGROUND_RED | FOREGROUND_INTENSITY);

    int sx = 5;
    int sy = 10;

    write_line_attr(" SSS ",sx,sy,FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    write_line_attr("S    ",sx,sy + 1,FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    write_line_attr(" SS  ",sx,sy + 2,FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    write_line_attr("   S ",sx,sy + 3,FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    write_line_attr("SSS  ",sx,sy + 4,FOREGROUND_GREEN | FOREGROUND_INTENSITY);

    write_line_attr("  ",sx + 5,sy,FOREGROUND_RED | FOREGROUND_INTENSITY);
    write_line_attr("i ",sx + 5,sy + 1,FOREGROUND_RED | FOREGROUND_INTENSITY);
    write_line_attr("  ",sx + 5,sy + 2,FOREGROUND_RED | FOREGROUND_INTENSITY);
    write_line_attr("i ",sx + 5,sy + 3,FOREGROUND_RED | FOREGROUND_INTENSITY);
    write_line_attr("i ",sx + 5,sy + 4,FOREGROUND_RED | FOREGROUND_INTENSITY);

    write_line_attr("RRR  ",sx + 8,sy,FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY);
    write_line_attr("R  R ",sx + 8,sy + 1,FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY);
    write_line_attr("RRR  ",sx + 8,sy + 2,FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY);
    write_line_attr("R R  ",sx + 8,sy + 3,FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY);
    write_line_attr("R  R ",sx + 8,sy + 4,FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY);

    write_line_attr("    ",sx + 13,sy,FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    write_line_attr("    ",sx + 13,sy + 1,FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    write_line_attr(" oo ",sx + 13,sy + 2,FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    write_line_attr("o  o",sx + 13,sy + 3,FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    write_line_attr(" oo ",sx + 13,sy + 4,FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
    hide_cursor();
    tgetch();
}

void loading_start_screen2(){
    clear_console();
    draw_frame();
    write_line_attr("SiRo2018 Loading...",1,1,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("Error...",1,2,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr(".Error..",1,2,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("..Error.",1,2,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("...Error",1,2,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("in was sl",1,1,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("0x0ff04003a",5,5,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("kmp",10,3,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("so1ve it",10,20,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("evil live",14,20,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("and somebody came",51,14,FOREGROUND_RED | FOREGROUND_INTENSITY);
    Sleep(load_line_sl_tm * 10);
    write_line_attr("{>I~.*V",18,18,FOREGROUND_RED | FOREGROUND_INTENSITY);
    tgetch();
}


void loading_start_screen(){
    if(rand() % 100 > 10){
        loading_start_screen1();
    }else{
        loading_start_screen2();
    }
}
#endif // SPLASH_SCREENS_H
