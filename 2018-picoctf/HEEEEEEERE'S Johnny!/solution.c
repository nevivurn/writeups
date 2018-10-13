#include <stdio.h>
#include <crypt.h>
#include <stdlib.h>
#include <string.h>

char *target = "$6$q7xpw/2.$la4KiUz87ohdszbOVoIopy2VTwm/5jEXvWSdWynh0CnP5T.MnJfVNCzp3IfJMHUNuBhr1ewcYd8PyeKHqHQoe.";
char *salt = "$6$q7xpw/2.$";

int main(void) {
	FILE *rockyou = fopen("rockyou.txt", "r");
	if (!rockyou) {
		perror("fopen");
		return 1;
	}

	char buf[64], *result = NULL;
	while (fgets(buf, 64, rockyou)) {
		for (int i = 0; buf[i] != '\0'; i++) {
			if (buf[i] == '\n') {
				buf[i] = '\0';
				break;
			}
		}

		result = crypt(buf, salt);
		if (!strcmp(result, target)) {
			puts(buf);
			break;
		}
	}

	free(result);
	fclose(rockyou);
}
