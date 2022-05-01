/*
 * SEAN HOBSON (SH)
 * April 26, 2021
 * Command Line Interpreter
 * CSC139
 *
 */

// Includes for external libraries in program
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
//#include <sys/stat.h>

// Global function declarations
int runCommand(char const *);
void greeting(int);
void printCommands(void);
//int isPath(char *); I could not get this function to work properly, but I am leaving it in here for now
char* concatStrings(const char *, const char *);
char* getLastCharsFromString(const char *, int);
void removeAllInstances(char *,char);

int main(int argc, char *argv[])
{
    // Initializing some variables that will be used throughout the main function of the program
    int numCommands = argc - 1;
    int cmdidx = 1;
    char * cmd;
    char * nextCmd;
    char * fullCommand;

    // Run the greeting function (see below for more details)
    greeting(numCommands);

    // If there is less than or equal to one argument on the command line (that is, calling
    // the .out file), print a notice to the user that no commands were recognized
    if (argc <= 1)
    {
        printf("You have not passed any commands.");
        printCommands();
    }
    // If the sole command of "showcommands" is passed, print out a list
    // of acceptable commands to the user (see below for function)
    else if((strcmp(argv[1],"showcommands") == 0) && (argc == 2))
    {
        printCommands();
        exit(0);
    }

    // So long as the number of commands remaining is greater than zero, stay in the loop
    while (numCommands > 0)
    {
        // Fire the upcoming command into the cmd variable
        cmd = argv[cmdidx];
        // Print a notice to the user what is about to be processed
        printf("argv[%i] = %s\n",cmdidx,cmd);
        
        // If the last character of the cmd variable is a variable, get rid of it
        // to prepare to pass it to the system function
        if(strcasecmp(getLastCharsFromString(cmd, 1), ",") == 0)
        {
            removeAllInstances(cmd, ',');
        }

        // Since the cd and touch commands can work similarly, I grouped them into one
        // if statement where I make sure that is the command being passed, grab the next
        // command in line and append it to the cd/touch command as one string,
        // then pass that to the runCommand function, which does as its name suggests.
        // If it is successful, then I decrement the number of remaining commands by 2
        // and move the index up 2 places.
        // If the touch command is used, I run a follow-up ls -l command to show the
        // last time the files were touched.
        // The part of this if statement where the runCommand function is called is
        // similar in each of the subsequent if-else statements, so I will refrain
        // from mentioning it henceforth.
        if ((strcasecmp(cmd, "cd") == 0) || (strcasecmp(cmd, "touch")) == 0)
        {
            nextCmd = argv[cmdidx + 1];
            printf("Attempting to run \'%s %s\' now...\n",cmd,nextCmd);
            fullCommand = concatStrings(cmd,nextCmd);
            if (runCommand(fullCommand) == 1)
            {
                cmdidx = cmdidx + 2;
                numCommands = numCommands - 2;
            }
            else
            {
                printf("Could not run command. Skipping this command.\n");
                cmdidx++;
                numCommands--;
            }

            if((strcasecmp(cmd, "touch")) == 0)
            {
                runCommand("ls -l");
            }
        }
        
        // If the exit command is passed, then I terminate the program altogether
        else if(strcasecmp(cmd, "exit") == 0)
        {
            printf("Attempting to run \'%s\' now...\n",cmd);
            exit(0);
        }
        
        // Since the exec, man, and which statements can be run in a similar fashion, I grouped them
        // altogether in this if-else and append the command after to them in a string and pass that
        // to the runCommand function.
        else if((strcasecmp(cmd, "exec") == 0) || (strcasecmp(cmd, "man") == 0) || (strcasecmp(cmd,"which") == 0))
        {
            nextCmd = argv[cmdidx + 1];
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
        
        // Since the ls and pwd functions don't require a second parameter, I grouped
        // them together and run them in a similar fashion.
        else if((strcasecmp(cmd, "ls") == 0) || strcasecmp(cmd,"pwd") == 0)
        {
            printf("Attempting to run \'%s\' now...\n",cmd);
            runCommand(cmd);
            cmdidx++;
            numCommands--;
        }
        
        // If the gcc command is called, I use a primitive, yet effective method to make
        // sure the second parameter (file to be gcc'd) is actually a .c or .h file.
        // Everything else after that is pretty much the same
        else if(strcasecmp(cmd, "gcc") == 0)
        {
            nextCmd = argv[cmdidx + 1];
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
            runCommand("ls -l");
        }
        
        // For the more command, I check to see if there is a dash in the case
        // of modifiers to the command, then concatenate that and the third parameter
        // to the more command as one string and pass that to the runCommand function
        else if(strcasecmp(cmd, "more") == 0)
        {
                nextCmd = argv[cmdidx + 1];

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
        
        // If the command being attempted is mv, then I also check for modifiers
        // via the dash operand, then grab the third and fourth parameters,
        // concatenate it altogether and run it through the runCommand function
        else if(strcasecmp(cmd, "mv") == 0)
        {
            nextCmd = argv[cmdidx + 1];

            if(strcasecmp(&nextCmd[0], "-") == 0)
            {
                char *thirdCommand = argv[cmdidx + 2];
                char *fourthCommand = argv[cmdidx + 3];

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
            else
            {
                char *thirdCommand = argv[cmdidx + 2];
                printf("Attempting to run \'%s %s %s\' now...\n", cmd, nextCmd, thirdCommand);
                fullCommand = concatStrings(concatStrings(cmd, nextCmd), thirdCommand);

                if (runCommand(fullCommand) == 1)
                {
                    cmdidx = cmdidx + 3;
                    numCommands = numCommands - 3;
                }
                else
                {
                    printf("Could not successfully run command.\nSkipping this command.\n");
                    cmdidx ++;
                    numCommands --;
                }
            }
        }
        
        // Same as a few of the else-ifs above, I also look for "dash modifiers"
        // for the rm command, concatenate everything together and runCommand it
        else if(strcasecmp(cmd, "rm") == 0)
        {
            if ((cmdidx + 1) >= numCommands)
            {
                printf("\nThere are not sufficient commands/operators passed.\nSkipping this command.\n");
                cmdidx++;
                numCommands--;
//                break;
            }

            else
            {
                nextCmd = argv[cmdidx + 1];
            }

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
            if (runCommand(fullCommand) != 0)
            {
                printf("Could not successfully run command.\nSkipping this command.\n");
            }
                cmdidx++;
                numCommands--;
        }
        
        // If a command is passed to the command line that isn't any of the
        // above options, I still check to see if it is a real command and
        // attempt to run it
        else
        {
            printf("Attempting to run \'%s\' now...\n", cmd);
            if(runCommand(cmd) == 0)
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

// This function takes in a pointer to a string and a specific character to
// remove all instances of from the string
// I used this to remove commas from the commands passed to the CLI
void removeAllInstances(char * st, char c)
{
    char *pr = st, *pw = st;
    while (*pr)
    {
        *pw = *pr++;
        pw += (*pw != c);
    }
    *pw = '\0';
}

// This function takes in a pointer to a string and a specific number, numChars
// What it does is return the last "numChars" from the string that was passed in
// It returns the last "numChars" characters from the string
char* getLastCharsFromString(const char *s1, int numChars)
{
    char *retString = malloc(numChars + 1);
    strncpy(retString, &s1[strlen(s1) - numChars], numChars);
    return retString;
}

// Because I didn't like the built-in strcat function, I built my own primitive
// version that was better suited for my needs.
// Takes in two string pointers, concatenates them, and then returns the pointer
// to the new string
char* concatStrings(const char *s1, const char *s2)
{
    char *final = malloc(strlen(s1) + strlen(s2) + 1);
    strcpy(final, s1);
    strcat(final," ");
    strcat(final, s2);
    return final;
}

// The famous runCommand function!
// This takes in a string/pointer to the command to be run and attempts to run
// it. If it is successful, it returns a 1 to the calling query, but if it is
// unsuccessful, it returns a 0
int runCommand(char const * fullCommand)
{
    if(system(fullCommand))
    {
        printf("%c", '\n');
        return 0;
    }
    else
    {
        printf("%c", '\n');
        return 1;
    }
}

//int isPath(char * path)
//{
//    struct stat s;
//    if(stat(path,&s) == 0)
//    {
//        if((s.st_mode & S_IFDIR) || (s.st_mode & S_IFREG))
//        {
//            return 1;
//        }
//    }
//    else
//    {
//        return 0;
//    }
//    return 0;
//}

// very simple function to print all commands that the program is designed to
// interpret
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
    printf("You may run multiple commands by separating each one with a comma and/or a space.\n\n");
}

// A delightful greeting to the user to let them know whose CLI it is, the date,
// the time, and a reminder that they can run 'showcommands' or leave the
// command line blank after the .out call to see all available commands
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