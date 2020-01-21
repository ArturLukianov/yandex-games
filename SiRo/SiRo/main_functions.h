#ifndef MAIN_FUNCTIONS_H
#define MAIN_FUNCTIONS_H

void prepare()
{
    SetConsoleTextAttribute(hConsole,15);
    SMALL_RECT windowSize = {0, 0, SCREEN_HEIGHT, SCREEN_WIDTH};

    SetConsoleWindowInfo(hConsole, TRUE, &windowSize);

    SetConsoleTitle(TITLE);
}

void message(std::string msg)
{
    if(system_message.length() < SCREEN_SYMW){
        system_message += msg;
        new_message = true;
        renew_message = true;
    }
}

void message_out()
{
    if (renew_message)
    {
        std::string filler = "";
        for(int i = 0 ; i < SCREEN_SYMW; i++)
        {
            filler+=" ";
        }
        write_line(filler,0,SCREEN_SYMH);
    }
    if(new_message)
    {
        write_line(system_message,0,SCREEN_SYMH);
        system_message = "|";
        new_message = false;
        renew_message = true;
        hide_cursor();
    }
}

#endif // MAIN_FUNCTIONS_H
