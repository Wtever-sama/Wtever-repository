#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIZE 100

int get_sum(char *bt, int i);
int find_max_sum(char *bt);
int main(){
    char input[MAX_SIZE];
    char bt[MAX_SIZE];
    fgets(input, MAX_SIZE, stdin);

    input[strcspn(input, "\n")] = '\0';//strcspn 是 C 标准库中的一个函数，用于计算字符串中不包含指定字符集的最长前缀长度。

    char *token = strtok(input, " ");
    int i = 0;
    while(token != NULL){
        if(token[0]== 'n')
            bt[i++] = '0';
        else bt[i++] = token[0];
        token = strtok(NULL, " ");
    }
    bt[i] = '\0';

    int max_sum = find_max_sum(bt);
    printf("%d\n", max_sum);
    return 0;
}
/*还原树，然后计算所有不直接相连的节点的数据之和的最大值
除了直接前驱和直接后继其他都是不直接相连的
如何判断是否是直接前驱和直接后继？
是直接前驱后后继就跳过进行下一个子树的遍历*/
/*可以由节点的编号确定它的直接前驱和后继*/

    //i是节点的标号，从 1
    //对于标号为i的节点，其前驱为 i/2，后继为 2i 2i+1
    //实际的下标等于编号减 1
    //遍历当当前元素的后面元素的编号不等于当前元素的下标的 2 倍或者 2 倍加一，
    //则当前元素为非相邻节点
    //假设从编号为 i 的节点开始， i = 1,2...size
    //那么标号为 2^k*i,(2i+1)*2^(k-1),k=1,2...,节点都要删除，只考虑剩下的节点求和,其中(2i+1)*2^k<=size,2^k<=size

    //这样需要求size个sum，并选出最大的；对于每个sum，时间复杂度为 O(size);最后的时间复杂度为 O(size^2)

int find_max_sum(char *bt){
    int size = strlen(bt);
    int sum[size];//储存每种可能的 sum
    for(int i = 1; i <= size; i++){
        sum[i-1] = get_sum(bt, i);
    }
    int max = sum[0];
    for(int i = 1; i<size; i++){
        if(sum[i] > max)
            max = sum[i];
    }
    return max;
}

int get_sum(char *bt, int i){
    int ini_idx = i;
    if (strlen(bt) == 0)return 0;
    int find_idx[strlen(bt)];//储存所有满足条件的下角标；注意，不是编号
    int index_find_idx = 0;
    //从起始节点往后面找
    for (int k = 1; 
    (k *(2*i + 1) <= strlen(bt)) 
    && (k*i <= strlen(bt)) 
    && (ini_idx <= strlen(bt)); 
    k *= 2){
        printf("k: %d\n",k);
        printf("ini_idx: %d\n",ini_idx);
        if(ini_idx-1 < strlen(bt)
            && bt[ini_idx-1] != 'n' 
            && ini_idx != k*i 
            && ini_idx != k*(2*i + 1)
            && ini_idx-1 < strlen(bt)){
                printf("k: %d\n",k);
                printf("k*i: %d\n",k*i);
                printf("forward ini_idx: %d\n",ini_idx);
                find_idx[index_find_idx] = ini_idx - 1;
        } 
        ini_idx++;
        index_find_idx++;
    }
    //往前面找
    ini_idx = i;
    for(int j = 2; (i/j >= 1) && (ini_idx>=1); j *= 2){
        if(bt[ini_idx-1] != 'n' && ini_idx != i/j && ini_idx-1<strlen(bt)){
            find_idx[index_find_idx] = ini_idx-1;
            printf("back ini_idx: %d\n",ini_idx);
        }
        ini_idx--;
        index_find_idx++;
    }
    int sum=0;
    for (int m = 0; m < index_find_idx; m++){
        sum += bt[find_idx[m]] - '0';
    }
    return sum;
}
/*input:
3 2 3 null 3 null 1
*/