#include <stdio.h>
#include <stdlib.h>

#define SHELLSCRIPT "\
#/bin/bash \n\
echo \"Playing GIF:\" \n\
xdg-open 2.gif \n\
"

int main()
{
    puts("Run the Shellscript:");
    system(SHELLSCRIPT);
    return 0;
}
