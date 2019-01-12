//Amr Hammam - 23180137
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <string.h>
//#include "/usr/bin/pythonw"

int main(int argc, char* argv[])
{
	char** args = calloc(sizeof(char*), argc + 1);
	for (int i = 0; i < argc; ++i)
	{
		args[i] = argv[i];
	}
	args[argc] = NULL;
	//printf(args[1]);

	int pid = fork();

	if (pid < 0)
	{
		printf("\nerr: fork FAILED\n");
		return 1;
	}

	else if (pid == 0)
	{
		//execvp("./emu.py", argv+1);
		execlp("python3", "python3", "./emu.py", args[2], NULL);
		printf("\nerr: CPU emulator\n");
		exit(EXIT_FAILURE);
	}

	else 
	{
		pid = fork();
		if (pid < 0)
		{
			printf("\nerr: fork 2 FAILED\n");
		}
		else if (pid == 0)
		{
			sleep(1);
			//execvp("./sched.py", argv+1);
			execlp("python3", "python3", "./sched.py", args[1], NULL);
			printf("\nerr: scheduler\n");
			exit(EXIT_FAILURE);
		}
		else
		{
			wait(NULL);
			printf("\nparent\n");
			return EXIT_SUCCESS;
		}
	}
	return 0;
}