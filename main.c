#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define SHIFT 48

int my_sum(int *total, int *num, int N);
void shift(int *array, int old, int new);
int main(void)
{
    char a;
    int *total = malloc(1*sizeof(int));
    total[0] = 1;
    int max_count = 1;
    int *next = malloc(1*sizeof(int));
    while(1) {
        int flag = 0;
        int count = 0;
        while(1) {
            if(scanf("%c", &a) != 1) {
                flag = 1;
                break;
            }
            if(a == ' ' || a == '\n' || a == '\t') {
                break;
            }
            next = realloc(next, (count+1)*sizeof(int));
            next[count] = a - 48;
            count++;
        }


        if (count > max_count) {
            total = realloc(total, count*sizeof(int));
            for (int i = max_count; i < count; i++) {
                total[i] = 0;
            }
            shift(total, max_count, count);
            max_count = count;
        }
        else if (count < max_count) {
            next = realloc(next, max_count*sizeof(int));
            for (int i = count; i < max_count; i++) {
                total[i] = 0;
            }
            shift(next, count, max_count);
            count = max_count;
        }

        //my_sum(total, next, max_count);
        printf("|");
        for (int i = 0; i < max_count; i++) {
            printf("%d", total[i]);
        }
        printf("|");




        if (flag == 1) {
            break;
        }
    }
}

int my_sum(int *total, int *next, int N) {
    int carry = 0;
    for (int i = N - 1; i > -1; i--) {
        int tmp = total[i] - SHIFT + next[i] - SHIFT + carry;
        carry = (tmp - tmp%10)/10;
        total[i] = tmp - carry;
    }
    int ttmp = carry;
    int count = 0;
    if (ttmp != 0) {
        while (ttmp != 0) {
            ttmp /= 10;
            count ++;
        }
    }
    shift(total, N, N+count);
    for (int i = 0; i<count; i++) {
        total[count - 1 - i] = carry%10;
        carry /=10;
    }
}

void shift(int *array, int old, int new) {
    for (int i = 0; i<new-old; i++) {
        int tmp = array[new-i - 1];
        array[new-i - 1] = array[i];
        array[i] = tmp;
    }
}
