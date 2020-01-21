#ifndef MENUS_H
#define MENUS_H

void credits_out()
{
    draw_frame();
    for(int i = 0; i < credits_length; i++)
    {
        write_line(credits[i] + "\n",1,1+i);
    }
    hide_cursor();
    tgetch();
    main_menu();
}

void help_out()
{
    draw_frame();
    for(int i = 0; i < help_length; i++)
    {
        write_line(help[i] + "\n",1,1+i);
    }
    hide_cursor();
    tgetch();
    main_menu();
}

void game_over()
{
    draw_frame();
    for(int i = 0; i < game_over_text_length; i++)
    {
        write_line(game_over_text[i] + "\n",1,1+i);
    }
    write_line("Killed by: ",1,game_over_text_length + 2);
    for(int i = 0; i < killers.size(); i++)
    {
        std::string comma = ",";
        if(i == killers.size()-1)
            comma="";
        write_line(" " + killers[i] + comma,1,game_over_text_length + 3 + i);
    }
    write_line(tips[std::rand()%tips_length],1,SCREEN_SYMH - 2);
    hide_cursor();
    while(tgetch()!=K_ENTER) {}
    main_menu();
}

void quit()
{
    draw_frame();
    for(int i = 0; i < quit_info_length; i++)
    {
        write_line(quit_info[i] + "\n",1,1+i);
    }
    hide_cursor();
    int quit_key = tgetch();
    if(quit_key == K_y)
        exit(EXIT_SUCCESS);
    else if(quit_key == K_n)
        return;
    else
        quit();
}

void quit_to_main_menu()
{
    draw_frame();
    for(int i = 0; i < quit_info_length; i++)
    {
        write_line(quit_info[i] + "\n",1,1+i);
    }
    hide_cursor();
    int quit_key = tgetch();
    if(quit_key == K_y)
        main_menu();
    else if(quit_key == K_n)
        return;
    else
        quit();
}

void welcome()
{
    draw_frame();

    write_line("WELLCOME TO SiRo - Simple Rogue!",1,1);
    write_line("<ETC>",1,2);
    write_line(tips[std::rand()%tips_length],1,SCREEN_SYMH - 2);
    hide_cursor();

    while(tgetch() != K_ENTER)
    {

    }
}

void main_menu()
{
    int cursor_position = 0;
    bool main_menu_running = 1;
    int last_key = 0;
    int r_tip = std::rand()%tips_length;
    while(main_menu_running)
    {
        draw_frame();
        write_line(tips[r_tip],1,SCREEN_SYMH - 2);
        for(int i = 0; i < main_menu_options_length; i++)
        {
            if(i == cursor_position)
                write_line_attr(main_menu_options[i],1,1+i, FOREGROUND_GREEN|FOREGROUND_INTENSITY);
            else
                write_line(main_menu_options[i],1,1+i);
        }

        write_line_attr("<---",10,1+cursor_position, FOREGROUND_RED | FOREGROUND_GREEN|FOREGROUND_INTENSITY);
        hide_cursor();
        last_key = tgetch();
        if(last_key == K_UP)
        {
            cursor_position--;
        }
        if(last_key == K_DOWN)
        {
            cursor_position++;
        }
        if(last_key == K_ENTER)
        {
            main_menu_running = 0;
        }
        if(cursor_position < 0)
            cursor_position = main_menu_options_length - 1;
        if(cursor_position >= main_menu_options_length)
            cursor_position = 0;
    }
    if(cursor_position == 0)
    {
        start_game();
    }
    else  if(cursor_position == 1)
    {
        help_out();
    }
    else if(cursor_position == 2)
    {
        credits_out();
    }
    else if(cursor_position == 3)
    {
        quit();
        main_menu();
    }
}


#endif // MENUS_H
