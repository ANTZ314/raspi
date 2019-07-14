#include <stdio.h>
#include <stdlib.h>

#define SHELLSCRIPT "\
#/bin/bash \n\
cd /home/pi/Videos \n\
omxplayer vid1.h264\n\
"

int main()
{
    puts("Will execute sh with the following script :");
    system(SHELLSCRIPT);
    return 0;
}