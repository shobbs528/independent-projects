#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include <sys/stat.h>

int runCommand(char const *);
void greeting(int);
void printCommands(void);
int isPath(char *);
char* concatStrings(const char *, const char *);
char* getLastCharsFromString(const char *, int);

int main(int argc, char *argv[])
{
    int numCommands = argc - 1;
    int cmdidx = 1;
    char cmd[64];
    char nextCmd[64];
    char * fullCommand;

    greeting(numCommands);

    if (argc <= 1)
    {
        printf("You have not passed any commands.");
        printCommands();
    }
    else if((strcmp(argv[1],"showcommands") == 0) && (argc == 2))
    {
        printCommands();
    }

    while (numCommands > 0)
    {
        strncpy(cmd,argv[cmdidx],64);
        cmd[63] = '\0';
        printf("argv[%i] = %s\n",cmdidx,cmd);

        if ((strcasecmp(cmd, "cd") == 0) || (strcasecmp(cmd, "touch")) == 0)
        {
            strncpy(nextCmd,argv[cmdidx+1],64);
            nextCmd[63] = '\0';
            printf("Attempting to run \'%s %s\' now...\n",cmd,nextCmd);
            fullCommand = concatStrings(cmd,nextCmd);
            if (isPath(nextCmd) == 1 && runCommand(fullCommand) == 1)
            {
                cmdidx = cmdidx + 2;
                numCommands = numCommands - 2;
            }
            else if (isPath(nextCmd) == 0)
            {
                printf("%s is not a valid directory or directory does not exist. Skipping this command.\n", nextCmd);
                cmdidx++;
                numCommands--;
            }
            else
            {
                printf("Could not run command. Skipping this command.\n");
                cmdidx++;
                numCommands--;
            }
        }
        else if(strcasecmp(cmd, "exit") == 0)
        {
            printf("Attempting to run \'%s\' now...\n",cmd);
            exit(0);
        }
        else if((strcasecmp(cmd, "exec") == 0) || (strcasecmp(cmd, "man") == 0) || (strcasecmp(cmd,"which") == 0))
        {
            strncpy(nextCmd,argv[cmdidx+1],64);
            nextCmd[63] = '\0';
            printf("Attempting to run \'%s %s\' now...\n",cmd,nextCmd);

            fullCommand = concatStrings(cmd,nextCmd);
            if (runCommand(fullCommand) == 1)
            {
                cmdidx = cmdidx + 2;
                numCommands = numCommands - 2;
            }
            else
            {
                printf("Could not successfully run command.\nSkipping this command.\n");
                cmdidx++;
                numCommands--;
            }
        }
        else if((strcasecmp(cmd, "ls") == 0) || strcasecmp(cmd,"pwd") == 0)
        {
            printf("Attempting to run \'%s\' now...\n",cmd);
            runCommand(cmd);
        }
        else if(strcasecmp(cmd, "gcc") == 0)
        {
            strncpy(nextCmd,argv[cmdidx+1],64);
            nextCmd[63] = '\0';
            printf("Attempting to run \'%s %s\' now...\n",cmd,nextCmd);
            char *lastChar = getLastCharsFromString(nextCmd, 1);
            if ((strcasecmp(&lastChar[strlen(lastChar) - 1], "c") == 0) || (strcasecmp(&lastChar[strlen(lastChar) - 1], "h") == 0))
            {
                fullCommand = concatStrings(cmd, nextCmd);
                if (runCommand(fullCommand) == 1)
                {
                    cmdidx = cmdidx + 2;
                    numCommands = numCommands - 2;
                }
                else
                {
                    printf("Could not successfully run %s for file %s. Skipping this command.\n", cmd, nextCmd);
                    cmdidx = cmdidx + 2;
                    numCommands = numCommands - 2;
                }
            }
            else
            {
                printf("This is not a supported file type for %s.\nSkipping this command.\n", cmd);
                cmdidx++;
                numCommands--;
            }
        }
        else if(strcasecmp(cmd, "more") == 0)
        {
            strncpy(nextCmd,argv[cmdidx+1],64);
            nextCmd[63] = '\0';

            if(strcasecmp(&nextCmd[0], "-") == 0)
            {
                char *thirdCommand = argv[cmdidx+2];
                printf("Attempting to run \'%s %s %s\' now...\n",cmd,nextCmd,thirdCommand);
                char *lastChars = getLastCharsFromString(thirdCommand, 3);
                if(strcasecmp(lastChars, "txt") == 0)
                {
                    fullCommand = concatStrings(concatStrings(cmd, nextCmd),thirdCommand);
                    if (runCommand(fullCommand) == 1)
                    {
                        cmdidx = cmdidx + 3;
                        numCommands = numCommands - 3;
                    }
                    else
                    {
                        printf("Could not successfully run %s %s %s.\nSkipping this command\n", cmd, nextCmd, thirdCommand);
                        cmdidx = cmdidx + 3;
                        numCommands = numCommands - 3;
                    }
                }
                else
                {
                    printf("This is potentially not a filetype supported by the %s command.\nSkipping this command.\n", cmd);
                    cmdidx = cmdidx + 2;
                    numCommands = numCommands - 2;
                }
            }
            else
            {
                printf("Attempting to run \'%s %s\' now...\n",cmd,nextCmd);

                char *lastChars = getLastCharsFromString(nextCmd, 3);
                if(strcasecmp(lastChars, "txt") == 0)
                {
                    fullCommand = concatStrings(cmd,nextCmd);
                    if (runCommand(fullCommand) == 1)
                    {
                        cmdidx = cmdidx + 2;
                        numCommands = numCommands - 2;
                    }
                    else
                    {
                        printf("Could not successfully run command.\nSkipping this command.\n");
                        cmdidx++;
                        numCommands--;
                    }
                }
                else
                {
                    printf("This is potentially not a filetype supported by the %s command.\nSkipping this command.\n", cmd);
                    cmdidx++;
                    numCommands--;
                }
            }
        }
        else if(strcasecmp(cmd, "mv") == 0)
        {
            strncpy(nextCmd,argv[cmdidx+1],64);
            nextCmd[63] = '\0';

            if(strcasecmp(&nextCmd[0], "-") == 0)
            {
                char *thirdCommand = argv[cmdidx + 2];
                char *fourthCommand = argv[cmdidx + 3];

                if((isPath(thirdCommand) != 0))
                {
                    printf("Your first directory, %s, was determined to not be valid.\nSkipping this command.\n", thirdCommand);
                    cmdidx = cmdidx + 2;
                    numCommands = numCommands - 2;
                }
                else if((isPath(fourthCommand) != 0))
                {
                    printf("Your first directory, %s, was determined to not be valid.\nSkipping this command.\n", fourthCommand);
                    cmdidx = cmdidx + 3;
                    numCommands = numCommands - 3;
                }
                else
                {
                    printf("Attempting to run \'%s %s %s %s\' now...\n",cmd,nextCmd,thirdCommand, fourthCommand);
                    fullCommand = concatStrings(concatStrings(concatStrings(cmd, nextCmd),thirdCommand),fourthCommand);

                    if (runCommand(fullCommand) == 1)
                    {
                        cmdidx = cmdidx + 4;
                        numCommands = numCommands - 4;
                    }
                    else
                    {
                        printf("Could not successfully run command.\nSkipping this command.\n");
                        cmdidx = cmdidx + 2;
                        numCommands = numCommands - 2;
                    }
                }
            }
            else
            {
                char *thirdCommand = argv[cmdidx + 2];
                if((isPath(nextCmd) != 0))
                {
                    printf("Your first directory, %s, was determined to not be valid.\nSkipping this command.\n", nextCmd);
                    cmdidx = cmdidx + 2;
                    numCommands = numCommands - 2;
                }
                else if((isPath(thirdCommand) != 0))
                {
                    printf("Your first directory, %s, was determined to not be valid.\nSkipping this command.\n", thirdCommand);
                    cmdidx = cmdidx + 3;
                    numCommands = numCommands - 3;
                }
                else
                {
                    printf("Attempting to run \'%s %s %s\' now...\n",cmd,nextCmd,thirdCommand);
                    fullCommand = concatStrings(concatStrings(cmd, nextCmd),thirdCommand);

                    if (runCommand(fullCommand) == 1)
                    {
                        cmdidx = cmdidx + 3;
                        numCommands = numCommands - 3;
                    }
                    else
                    {
                        printf("Could not successfully run command.\nSkipping this command.\n");
                        cmdidx++;
                        numCommands--;
                    }
                }
            }
        }
        else if(strcasecmp(cmd, "rm") == 0)
        {
            strncpy(nextCmd,argv[cmdidx+1],64);
            nextCmd[63] = '\0';

            if(strcasecmp(&nextCmd[0], "-") == 0)
            {
                char *thirdCommand = argv[cmdidx+2];
                printf("Attempting to run \'%s %s %s\' now...\n",cmd,nextCmd,thirdCommand);
                fullCommand = concatStrings(concatStrings(cmd, nextCmd),thirdCommand);

                if (runCommand(fullCommand) == 1)
                {
                    cmdidx = cmdidx + 3;
                    numCommands = numCommands - 3;
                }
                else
                {
                    printf("Could not successfully run command.\nSkipping this command.\n");
                    cmdidx++;
                    numCommands--;
                }
            }
            else
            {
                fullCommand = concatStrings(cmd, nextCmd);
                if (runCommand(fullCommand) == 1)
                {
                    cmdidx = cmdidx + 2;
                    numCommands = numCommands - 2;
                }
                else
                {
                    printf("Could not successfully run command.\nSkipping this command.\n");
                    cmdidx++;
                    numCommands--;
                }
            }
        }
        else if(strcasecmp(cmd, "sh") == 0)
        {
            printf("\nNow converting to dash (sh) shell...\n");
        }
        else if(strcasecmp(cmd,"$PATH") == 0)
        {
            printf("Now showing $PATH filepaths...\n");
            fullCommand = concatStrings("echo",cmd);
            if (runCommand(fullCommand) != 1)
            {
                printf("Could not successfully run command.\nSkipping this command.\n");
            }
                cmdidx++;
                numCommands--;
        }
        else
        {
            printf("Attempting to run \'%s\' now...\n", cmd);
            if(runCommand(cmd) == 1)
            {
                cmdidx++;
                numCommands--;
            }
            else
            {
                printf("Could not successfully run command. Skipping this command.\n");
                cmdidx++;
                numCommands--;
            }
        }
    }

    exit(0);
}

char* getLastCharsFromString(const char *s1, int numChars)
{
    char *retString = malloc(numChars + 1);
    strncpy(retString, &s1[strlen(s1) - numChars], numChars);
    return retString;
}

char* concatStrings(const char *s1, const char *s2)
{
    char *final = malloc(strlen(s1) + strlen(s2) + 1);
    strcpy(final, s1);
    strcat(final," ");
    strcat(final, s2);
    return final;

}

int runCommand(char const * fullCommand)
{
    if(system(fullCommand))
    {
        printf("%c", '\n');
        return 1;
    }
    else
    {
        printf("%c", '\n');
        return 0;
    }
}

int isPath(char * path)
{
    struct stat s;
    if(stat(path,&s) == 0)
    {
        if((s.st_mode & S_IFDIR) || (s.st_mode & S_IFREG))
        {
            return 1;
        }
    }
    else
    {
        return 0;
    }
    return 0;
}

void printCommands(void)
{
    printf("\nHere are a list of the available commands to run from the CLI:\n");
    printf("- cd\n");
    printf("- exec\n");
    printf("- exit\n");
    printf("- gcc\n");
    printf("- ls\n");
    printf("- man\n");
    printf("- more\n");
    printf("- mv\n");
    printf("- rm\n");
    printf("- pwd\n");
    printf("- sh\n");
    printf("- touch\n");
    printf("- which\n");
    printf("- $path\n");
    printf("\nTo see how any of these commands work, please run \"man <command>\"\n");
    printf("You may run multiple commands by separating each one with a space.\n\n");
}

void greeting(int x)
{
    printf("\nWelcome to SH's CLI\n");
    struct tm *tm;
    time_t t;
    char sTime[100];
    char sDate[100];
    t = time(NULL);
    tm = localtime(&t);
    strftime(sDate, sizeof(sDate), "%B %d %Y", tm);
    strftime(sTime, sizeof(sTime), "%I:%M:%S %p", tm);
    printf("The date is: %s\n", sDate);
    printf("The time is: %s\n\n", sTime);

    if(x <= 1)
    {
        printf("<><><>To show a full list of commands available, either re-run the program with no arguments or run "
               "the program with the \"showcommands\" argument.<><><>\n\n");
    }
}