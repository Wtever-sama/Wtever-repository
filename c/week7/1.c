#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define MAX_SIZE 100

struct btnode {
    char data;
    struct btnode *left;
    struct btnode *right;
};
//新节点
struct btnode *newNode(int data){
    struct btnode *node = (struct btnode *)malloc(sizeof(struct btnode));
    node->data = data;
    node->left = NULL;
    node->right = NULL;
    return node;
}

//创建队列节点
typedef struct QueueNode{
    struct btnode *treenode;
    struct QueueNode *next;
}QueueNode;
//创建队列
typedef struct{
    QueueNode *front;
    QueueNode *rear;
}Queue;
//入队
void enqueue(Queue *q, struct btnode *node){
    //先分配内存，这里新节点是队列节点类型
    QueueNode *new_node = (QueueNode *)malloc(sizeof(QueueNode));
    //赋值
    new_node->treenode = node;
    new_node->next = NULL;
    //如果队列不空则将新节点添加到队尾
    if(q->rear)q->rear->next = new_node;
    //否则将新节点作为队首，同时队尾指向新节点
    else q->front = new_node;
    q->rear = new_node;
}

struct btnode *dequeue(Queue *q){
    //如果队列队首为空则返回空
    if(!q->front)return NULL;
    //创建临时队列节点储存队首元素
    QueueNode *temp = q->front;
    struct btnode *node = temp->treenode;
    //队首向后面移动一位
    q->front = q->front->next;
    //如果移动后队首为空就将队尾设置成空
    if(!q->front)q->rear = NULL;
    free(temp);
    return node;
}

int isEmpty(Queue *q){
    return q->front == NULL;
}
//还原一颗二叉树
struct btnode *create_bt(char *bt){
    int size = strlen(bt);
    int inf_min = -1000;
    int inf_max = 1000;
    if(size == 0 || bt[0] == '\0')return NULL;

    struct btnode *root = newNode(bt[0]);
    Queue q = {NULL, NULL};//初始化空队列
    enqueue(&q, root);//根节点先入队

    int i = 1;
    while(i < size){
        struct btnode *current = dequeue(&q);//先取出一个队首节点作为当期节点，下一个左右子树的parent
        if(current->data != 'n'){
            if(bt[i] != 'n'){//如果数组元素不是null，有左节点
                current->left = newNode(bt[i]);
                enqueue(&q, current->left);
            }
            i++;
            if(i < size && bt[i] != 'n'){//如果还有剩余元素，并且不是 null，则构造右子节点
                current->right = newNode(bt[i]);
                enqueue(&q, current->right);
            }
            i++;
        }else{
            i++;
            continue;
        }        
    }

    return root;
}

char find_common_parent(char *bt, int idx_node1, int idx_node2);
int get_level(int index_node);
int index_find_where_is_node(char *bt, char node);//根节点从 1 开始

int is_ordered_bt(struct btnode *root, int min, int max);
int main(){
    //初始化数组和数据
    char input[MAX_SIZE];
    char bt[MAX_SIZE];
    char node1, node2;
    int index = 0;
    int node_num = 0;

    int num = 0;

    //输入数据
    while(fgets(input, MAX_SIZE, stdin) != NULL){
        input[strcspn(input, "\n")] = '\0';
        char *token = strtok(input, " ");
        if(index == 0){
            while(token != NULL){
                bt[node_num] = token[0];//取字符串首字符;这里赋值的是token就是指针，是不对的 
                node_num++;
                token = strtok(NULL, " ");//?
            }
        }else{
            node1 = token[0]; // char node1
            token = strtok(NULL, " ");
            node2 = token[0]; // 取第二个token的首字符
        }
        index++;
        bt[node_num] = '\0';
    }

    int idx_node1 = index_find_where_is_node(bt, node1);
    int idx_node2 = index_find_where_is_node(bt, node2);

    //处理函数
    struct btnode *root = create_bt(bt);
    int min= -1000;
    int max= 1000;
    if(is_ordered_bt(root, min, max)){
        char parent = find_common_parent(bt, idx_node1, idx_node2);
        printf("%c\n", parent);
    }else{
        printf("null\n");
    }

    //free(bt);
    return 0;
}

char find_common_parent(char *bt, int idx_node1, int idx_node2){

    int level_node1 = get_level(idx_node1);
    int level_node2 = get_level(idx_node2);
    
    //printf("level_node1: %d\n", level_node1);
    //printf("level_node2: %d\n", level_node2);

    //找到深层是哪一层,处理到同一层
    while(level_node1 > level_node2){
        idx_node1 /= 2;
        level_node1 -= 1;
    }
    while (level_node2 > level_node1){
        idx_node2 /= 2;
        level_node2 -= 1;
    }
    
    //处于同一层，同时向上直到找到最近的双亲节点
    while(idx_node1 != idx_node2){
        idx_node1 /= 2;
        idx_node2 /= 2;
    }

    return bt[idx_node1-1];
}
int get_level(int index_node){
    return (int)floor(log2(index_node)) + 1;
}
int index_find_where_is_node(char *bt, char node){
    //读到终止符为止
    for(int i = 0; bt[i] != '\0'; i++){
        if(bt[i] == node){
            return i + 1;
        }else{
            continue;//第一次匹配不顺利要继续不能退出
        }
    }
    return -1;
}
/*还原出这颗树再用中序遍历或者递归验证*/
int is_ordered_bt(struct btnode *root,int min, int max) {
    // 空节点是合法的
    if (!root || root->data == 'n') return 1;
    // 将字符转换为整数
    int data_value = root->data - '0'; // 假设数据是 '0'-'9' 的字符
    // 检查当前节点是否在合法范围内
    if (data_value < min || data_value > max) {
        return 0; // 不满足二叉排序树性质
    }
    // 递归检查左子树和右子树
    return is_ordered_bt(root->left, min, data_value - 1) &&
           is_ordered_bt(root->right, data_value + 1, max);
}

/*output
6 2 8 0 4 7 9 null null 3 5
2 8
input array:
6280479nn35
node1: 2
node2: 8
closest parent: 
c*/

/*printf("idx_node1: %d\n",idx_node1);
    printf("idx_node2: %d\n",idx_node2);

    //检查是否正确输入：
    printf("input array:\n");
    printf("%s\n", bt);
    printf("node1: %c\n", node1);
    printf("node2: %c\n", node2);*/

/*
采用数组进行处理

如果将 null 也算进节点的话，树就是完全二叉树
由数组下标确定编号，
编号从 1 开始
第i编号的节点的parent为i/2
左子树的编号为2i，右子树为2i+1

·若2i>n,则编号为i 的结点无左子树;若2i£n,则编号
为i 的结点的左孩子的编号为2i；
·若2i+1>n,则编号为i 的结点无右子树;若2i+1£n,
则编号为i 的结点的右孩子的编号为2i+1。

对于第i层，有2^（i-1）个节点，从左边到右边依次是存储的数据
有x个几点，包括null
2^i-1<x<=2^i，有 i+1层
这样就可以构建一颗层次遍历的二叉树

对于给定的俩个节点，
先找到在输入的列表的位置，确定其所在的层次，*/

/*
先用 max size 存储输入列表，为第一行
第二行是两个数字，找到在列表中的位置，如果在同一层，就直接除以二直到彼此的值相等为止；

***如果是二叉排序树就继续下面的程序否则就终止；

***如果在不同的层，深的那一层先处理到和浅的一样，然后从浅层开始处理，直到相等为止；
关键是确定所在层次和处理到同一层次
后者：until pow(2,浅层序号-2)<处理后的节点编号<=pow(2,浅层序号-1)
若是两者相同了就输出 数组[找到的下标]；
如果在深层往浅层走的过程中父节点就是浅层，那么输出浅层
*/
/*//返回的是指向根结点的指针
    struct btnode *root = NULL;

    struct btnode *root_node = (struct btnode *)malloc(sizeof(struct btnode));
    if(root_node == NULL){
        printf("Memory Allocation Error\n");
        exit(1);
    }
    root_node->data = bt[0];
    root_node->left = NULL;
    root_node->right = NULL;
    
    root->left = root_node;

    struct btnode *current = root_node;//从头遍历

    for(int i = 0; i < strlen(bt); i++){

        struct btnode *new_node = (struct btnode *)malloc(sizeof(struct btnode));
        if(new_node == NULL){
            printf("Memory Allocation Error\n");
            exit(1);
        }
        new_node->data = bt[i];
        new_node->left = NULL;
        new_node->right = NULL;

        // 判断插入位置
        int flag = 0;
        while(current != NULL){
            while(current->data >= new_node->data){
                current = current->left;
                flag = 0;
            }
            while(current->data < new_node->data){
                current = current->right;
                flag = 1;
            }
        }
        if (flag == 0){
            current->left = new_node;
        }else{
            current->right = new_node;
        }
        current = new_node;
    }//for循环结束
    return root;*/