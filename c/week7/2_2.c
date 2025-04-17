#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIZE 1000

// 定义二叉树节点结构
typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

// 辅助函数，用于创建新的二叉树节点
TreeNode* createTreeNode(int val) {
    TreeNode* node = (TreeNode*)malloc(sizeof(TreeNode));
    node->val = val;
    node->left = NULL;
    node->right = NULL;
    return node;
}

// 从层次遍历字符串构建二叉树
TreeNode* buildTree(char* bt) {
    if (bt[0] == '0') return NULL;
    TreeNode* root = createTreeNode(bt[0] - '0');
    TreeNode* queue[MAX_SIZE];
    int front = 0, rear = 0;
    queue[rear++] = root;//将当前节点的左子节点加入队列，以便后续继续处理它的子节点
    int i = 1;
    while (front < rear && bt[i] != '\0') {
        //取出当前节点
        TreeNode* current = queue[front++];
        // 处理左子节点
        if (bt[i] != '0') {
            current->left = createTreeNode(bt[i] - '0');
            queue[rear++] = current->left;//将新创建的左子节点加入队列（queue[rear++]）
        }
        i++;
        if (bt[i] != '0') {
            current->right = createTreeNode(bt[i] - '0');
            queue[rear++] = current->right;
        }
        i++;
    }
    return root;
}

// 主函数，计算在不触发警报情况下能盗取的最大金额
int* robTree(TreeNode* root) {
    if (root == NULL) {
        int* result = (int*)malloc(2 * sizeof(int));
        result[0] = 0;
        result[1] = 0;
        return result;
    }
    int* left = robTree(root->left);//递归调用左右子树，分别得到左右子树能盗取的最大金额；
    int* right = robTree(root->right);//其中[0]表示不选择当前节点，[1]表示选择当前节点的最大金额

    int* result = (int*)malloc(2 * sizeof(int));
    // 选择偷当前节点，那么不能偷其左右子节点
    result[1] = root->val + left[0] + right[0];
    // 不选择偷当前节点，则可以选择偷或不偷左右子节点，取最优解
    result[0] = left[0] > left[1]? left[0] : left[1] + (right[0] > right[1]? right[0] : right[1]);

    free(left);
    free(right);
    return result;
}

int find_max_sum(char* bt) {
    TreeNode* root = buildTree(bt);
    int* result = robTree(root);
    int max = result[0] > result[1]? result[0] : result[1];
    free(result);
    return max;
}

// 辅助函数，用于释放二叉树内存
void freeTree(TreeNode* root) {
    if (root == NULL) return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}
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
/*
condition ? value_if_true : value_if_false;
condition：一个布尔表达式，结果为真（非零）或假（零）。
value_if_true：当 condition 为真时返回的值。
value_if_false：当 condition 为假时返回的值。

*/