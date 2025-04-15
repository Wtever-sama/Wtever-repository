#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIZE 100
#define INF_MIN -1000
#define INF_MAX 1000
int main(){
    char input[MAX_SIZE];
    char bt[MAX_SIZE];
    fgets(input, MAX_SIZE, stdin) != NULL);

    input[strcspn(input, "\n")] = '\0';//strcspn 是 C 标准库中的一个函数，用于计算字符串中不包含指定字符集的最长前缀长度。

    char *token = strtok(input, " ");
    int i = 0;
    while(token != NULL){
        if(token[0]== 'n')
            bt[i++] = 'n';
        else bt[i++] = token[0];
        token = strtok(NULL, " ");
    }
    bt[i] = '\0';
}
/*还原树，然后计算所有不直接相连的节点的数据之和的最大值
除了直接前驱和直接后继其他都是不直接相连的
如何判断是否是直接前驱和直接后继？
是直接前驱后后继就跳过进行下一个子树的遍历*/