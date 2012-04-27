#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

struct node {
  int val;
  struct node *left;
  struct node *right;
};

int max(int a, int b) {
  if (a >= b) return a;
  return b;
}

int depth(struct node* root) {
  if (root == NULL) return 0;
  if (root->left == NULL && root->right == NULL) {
    return 0;
  } else {
    return 1 + max(depth(root->left), depth(root->right));
  }
}


void print_level(struct node *root, int level) {
  int d = depth(root);
  char space[2*d];
  if (level == 0) printf( "%s%d\n", memset(space, ' ', 2*d), root->val);
  else {
    
  }
}

int **twodarray(int w, int h) {
  printf("width: %d\theight: %d\n", w, h);
  int i, j;
  int **array = malloc(sizeof(int*) * h);
  for (i = 0; i < h; i++) {
    array[i] = malloc(sizeof(int*) * w);
    for (j = 0; j < w; j++) {
      array[i][j] = -1;
    }
  }
  return array;
}

void fill_box(int **box, struct node* item, int level, int offset) {
  if (item == NULL) return;
  else {
    box[level][offset] = item->val;
    box[level+1][offset+1] = -3;
    box[level+1][offset-1] = -2;
    fill_box(box, item->left, level + 2, offset - 2);
    fill_box(box, item->right, level + 2, offset + 2);
  }
}

void print_tree(struct node* root) {
  int i, j, w, h, d;
  d = depth(root);
  w = (exp2(d) + 1) * 2;
  h = (d + 1) * 2;
  printf("depth: %d\n", d);
  int **box = twodarray(w, h);
  fill_box(box, root, 0, w/2);
  for (i = 0; i < h; i++){
    for (j = 0; j < w; j++) {
      switch(box[i][j]) {
          case (-1): 
            printf("  ");
            break;
          case (-2):
            printf(" /");
            break;
          case (-3):
            printf("\\ ");
            break;
          default:
            printf("%d ", box[i][j]);
            break;
      }
    }
    printf("\n");
  }
}

void insert(struct node* item, struct node* root) {
  if (item->val < root->val) {
    if (root->left == NULL) root->left = item;
    else insert(item, root->left);
  } else {
    if (root->right == NULL) root->right = item;
    else insert(item, root->right);
  }
}

struct node *newNode(int val) {
  struct node* node = (struct node*) malloc(sizeof(struct node));
  node->val = val;
  node->left = NULL;
  node->right = NULL;
  return node;
}



int main(){
  struct node *root = newNode(10);
  struct node *left = newNode(5);
  struct node *a1 = newNode(7);
  struct node *a2 = newNode(15);
  struct node *a3 = newNode(20);
  struct node *a4 = newNode(25);
  insert(left, root);
  insert(a1, root);
  insert(a2, root);
  insert(a3, root);
  insert(a4, root);
  print_tree(root);
}
