#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
// https://velog.io/@seanlion/btreeimplementation
#define M 5
#define max_children M
#define max_keys max_children-1
#define min_keys (int)(ceil(M/2.0))-1 // 최소 키 개수 구하는 식 

struct BTreeNode* root; //root 노드 기본 설정(포인터로) 
struct BTreeNode{
	bool leaf; // leaf 여부
	int key[max_keys+1]; // key를 담을 배열
	int cnt_key; //키 개수 확인용
	struct BTreeNode* child[max_children+1]; // 자식 포인터 배열 (노드들이 배열로들어감)
	int cnt_child; //자식 개수 확인용
};

int deleteValFromNode(int val, struct BTreeNode* node);

struct BTreeNode* root; // root노드 기본 설정 (포인터로)

//검색
int searchNode(struct BTreeNode* node, int val){
	if (!node){
		printf("Empty node. \n");
		return 0;
	}
	struct BTreeNode* level = node;
	while (true){
		int pos;
		for (pos=0; pos<level->cnt_key; pos++){ // 순차검색
			if (val==level->key[pos]){ //있다면?
				printf("key %d exists!",val);
				return 1;
			}
			else if (val < level->key[pos]){ // 더 큰게 있다면? -> child로 내려가야해
				break;
			}
		}
		if (level->leaf) break;
		level = level->child[pos]; //child 로 level포인터를 바꿔준 다음 while문 새로 시작
	}
} 

struct BTreeNode* createNode(int val){
	struct BTreeNode* newNode; // new node struct 선언
	newNode = (struct BTreeNode*)malloc(sizeof(struct BTreeNode)); // Node에 동적 할당
	newNode->leaf=false; // 리프여부는 초기값 false로
	newNode->key[0]=val; // 새 node의 0번째 key값에 받아온 데이터 넣기
	newNode->cnt_key=1;  // 아직 키가 하나이므로
	newNode->cnt_child=0; // 아직 자식이 없어
	return newNode;
}

// split을 위해 현재노드에 넣은값의 위치값(pos), 현재노드, 부모노드 받기
struct BTreeNode* splitNode(int pos, struct BTreeNode* node, struct BTreeNode* parent){
	int median; //분리를 위해 중앙값 찾아야함
	median = node->cnt_key/2 ; //중앙값은 짝수든 홀수든 'key개수/2'
	struct BTreeNode* right_node; //분리한 값을 새로 넣어줄 오른쪽 노드 만들기 (추후 자식이 됨.)

	right_node=(struct BTreeNode*)malloc(sizeof(struct BTreeNode));
	right_node->leaf = node->leaf; //분리만 한거니까 현재 분리하려는 노드와 리프 여부가 같음 (현재노드가 리프면 right_node도 리프)
	right_node->cnt_key=0;
	right_node->cnt_child=0;

	int num_iter = node->cnt_child;
	//중간부터 끝까지 오른쪽에 담기
	for (int i= median+1; i< num_iter; i++){
		//분리할 노드에 키 담기 (리프든 아니든)
		right_node->key[i-(median+1)] = node->key[i];
		right_node->cnt_key++;
		node->cnt_key--;
	}

	if (!node->leaf){// 현재노드가 leaf가 아니면 -> 자식담기
	    num_iter=node->cnt_child;
		for (int i=median+1; i<num_iter; i++){
			right_node->child[i-(median+1)] = node -> child[i];
			right_node->cnt_key++;
			node->cnt_child--;
		}
	}
	//분리할 때 위로 올릴 부모노드 처리
	if (node==root){// 루트면 새 부모노드 만들어야함.
		struct BTreeNode* new_parent_node;
		new_parent_node=createNode(node->key[median]); // 중앙값 갖고 새 부모노드 만들기
		node -> cnt_key--;
		new_parent_node->child[0]=node;// 새 부모노드의 왼쪽자식은 현재노드
		new_parent_node->child[1]=right_node;// 오른쪽 자식을 새로만들어진 오른쪽노드
		new_parent_node->cnt_child=2;
		return new_parent_node;
	}else{ //root가 아니면, 원래있던 부모노드 활용
		for (int i=parent->cnt_key; i>pos; i--){
			// 부모노드에 넣어야하니까 거기있던 키 배치 다시하기(뒤로밀기)
			parent->key[i]=parent->key[i-1];
			parent->child[i+1]=parent->child[i]
		}
		parent->key[pos]=node->key[median];//부모노드에 넣어야할 자리에 값 넣기
		parent->cnt_key++; //부모노드 키 개수 증가
		node->cnt_key--;   //원래노드 키 개수 감속
		parent->child[pos+1]=right_node; //왼쪽노드는 원래 연결되어있으니, 오른쪽만 부모노드에 연결.
		parent->cnt_child++;
	}
	return node;
}
//노드에 값을 삽입하는 함수구조체 제작. (split을 위해 부모노드(parent), 현재노드(node)를 같이 듦),
//부모노드에서 특정 키의 위치를 갖고있음.
struct BTreeNode* insertNode(int parent_pos, int val, struct BTreeNode* node, struct BTreeNode* parent){
	int pos;//현재 노드에서 키의 위치를 갖고있어야함. 왜냐면 넣으려고 하는 값의 위치를 찾아야하기에
	for (pos=0; pos< node->cnt_key; pos++){
		//pos의 위치는 0부터시작, 현재노드의 키 개수만큼 탐색
		if (val==node->key[pos]){
			//node의 pos번째 키와 val이 같다면
			printf("Duplicates are not Permitted! \n");
			return node;
		//val이 현재pos보다 작다면, 그 pos에서 멈춘다. 
		}else if(val < node->key[pos]){break;}
		//만약 val이 그 node에 있는 값보다 크다면 마지막 pos가 나올 것임.
	}
	if (!node->leaf){
		//node leaf 여부가 false이면, (leaf가 아니라면)
		//node의 pos번째 자식노드에 insertNode값을 담는다. -> 재귀로 자식을 탐색하러 또들어감
		node->child[pos] = insertNode(pos,val,node->child[pos], node);
		if (node->cnt_key==max_keys+1){
			//현재 노드 키 개수가 규칙에서 벗어날 것 같으면 -> 스플릿
			node = splitNode(parent_pos, node, parent);//윗방향으로 분리
		}
	}else{
		//leaf일 경우 삽입로직
		for (int i=node->cnt_key; i>pos; i--){
			//끝에서부터 val을 삽입해야하는 위치에 있는 노드까지의 노드들을 뒤로 땡기는 작업
			node->key[i]=node->key[i-1];//key가 한칸씩 뒤로감
			node->child[i+1]=node->child[i];//child도 마찬가지
		}
		node->key[pos]=val;//val을 삽입해야하는 위치에 val삽입.
		node->cnt_key++; //key count중가
		if(node->cnt_key == max_keys+1){ // leaf 노드가 꽉 찼으면 분리작업수행
			node=splitNode(parent_pos node, parent);
		}
	}
	return node;//node에 값을 넣어주니까 그 node를 반환. 그래야 재귀가 종료
}

//삽입함수 제작(val : 받아야하는값)
void insert(int val){
	if (!root){//root가 없으면 새로 생성 , 해당 노드는 루트이자 리프노드
		root=createNode(val);
		root->leaf=true;
		return;
	}else{//처음에는 root가 부모이자 리프노드.
		root=insertNode(0,val,root,root);
	}
}

//못빌릴때 합치는 함수
void mergeNode(struct BTreeNode* par_node, int node_pos, int mer_node_pos){
// 왼쪽 노드를 지웠을 때엔 최종 merge되는 주체가 왼쪽노드가 되도록 강제로 만듦(편의성)
// node_pos가 삭제된 키를 갖고있는 노드가 될 수도있고 안될 수도 있음
	int merge_idx = par_node->child[mer_node_pos]->cnt_key;
	
	//부모노드의 key를 merge함.
	par_node->child[mer_node_pos]->key[merge_idx] = par_node->key[mer_node_pos];
	par_node->child[mer_node_pos]->cnt_key++;

	for (int i=0; i<par_node->child[node_pos]->cnt_key; i++){
// 지우는 노드에서 그 키를 지워서 최소 키 개수 유지가 안될 수 있음. 
// 남은 키 들은 merge한 노드로 옮겨야함.. 남은키가 없으면 for문이 돌지않음.
		par_node->child[mer_node_pos]->key[merge_idx+1+i] = par_node->child[node_pos]->key[i]; // 키개수가 2개 -> i가 0, merge idx 오른쪽 키/키개수가 늘어나면 하나씩 더 늘어남.
		par_node->child[mer_node_pos]->cnt_key++;
	}

//merge한 노드 끝 부분으로 옮겨가야 하니 끝 부분 idx 지정.
	int merge_child_idx=par_node->child[mer_node_pos]->cnt_child;
	for (int i=0; i<par_node->child[node_pos]->cnt_child; i++){
//지우는 노드에서 키를 지우고 남은 자식이 있으니, 자식들을 merge한 노드로 옮겨야함.
		par_node->child[mer_node_pos]->child[merge_child_idx+i] = par_node->child[node_pos]->child[i];
		par_node->child[mer_node_pos]->cnt_child++;
	}
	free(par_node->child[node_pos]);//merge 되고나서 반대편 노드는 필요없으니 메모리에서날리기
	for(int i=mer_node_pos; i<(par_node->cnt_key)-1; i++){
		//부모노드의 키 하나는 이미 자식노드와 병합되었으니 재정비
		par_node->key[i]=par_node->key[i+1];
	}
	par_node->cnt_key--;

	for(int i=mer_node_pos+1; i<(par_node->cnt_child)-1; i++){
		//부모노드에는 병합한거 말고, 그 뒤 자식도 있을 수 있으니, 재배열
		// merge한 노드 뒷노드부터 대상이됨.
		par_node->child[i] = par_node->child[i+1];
	}
	par_node->cnt_child--;
}

//왼쪽에서 빌리는 함수
//부모노드 par_node 와, 현재노드 pos위치를 인자로 받음. 이미 현재 노드의 키는 지워졌음
//cnt_key는 최소상태 혹은 미만일 것임.
void borrowFromLeft(struct BTreeNode* par_node, int cur_node_pos){
	int tenant_idx=0 ; //빌리는 주체노드에 빌려주는 키가 들어가야할 위치

	//빌리는 자리를 마련해야하기에 기존것을 한칸씩 뒤로 미뤄줌 (남아있는게 없어도 적용). borrowFromRight와 달리 먼저 자리정리를 해야함
	for(int i=0; i<par_node->child[cur_node_pos]->cnt_key; i++){
		par_node->child[cur_node_pos]->key[i+1] = par_node->child[cur_node_pos]->key[i];
	}
	
	//빌리는 키는 오름차순 상 부모에게서 빌려옴. 여기서는 왼쪽에서 빌려오니까, cur_node_pos(오른쪽 자식 가르키는위치)에서 1을 뺴야 부모키의 위치가됨. 
	//그리고, 형제노드의 키가 위로 올라가는 꼴.
	par_node->child[cur_node_pos]->key[tenant_idx] = par_node->key[cur_node_pos-1]; 
	par_node->child[cur_node_pos]->cnt_key--;

	//형제노드를 빌려줬으니, 자식도 정리해야함. 자식위치 정리도 진행 (한칸씩 앞으로 떙김)
	if (par_node->child[cur_node_pos-1]->cnt_child > 0){
// 형제노드 자식이 있는 경우에만
		int tenant_child_idx=(par_node->child[cur_node_pos-1]->cnt_child)-1; // tenant 노드에 형제노드의 가장 뒷 자식 위치를 줘야하기에 그 인덱스 지정
		
		// 자식위치 정리. borrowFromRight와 달리 미리 세팅해야함.
		for(int i = par_node->child[cur_node_pos]->cnt_child ; i>0; i--){
			//뒤에서부터 시작
			par_node->child[cur_node_pos]->child[i] = par_node->child[cur_node_pos]->child[i-1];
		}
		
		//형제노드 자식 빌려옴. 빌려온 자식 놓는 위치는 현재노드의 첫번째 위치
		par_node->child[cur_node_pos]->child[0] = par_node->child[cur_node_pos-1]->child[tenant_child_idx];
		par_node->child[cur_node_pos]->cnt_child++;
		
		par_node->child[cur_node_pos-1]->cnt_child--;
	}
}
// 왼쪽자식의 맨 오른쪽에서, 오른쪽이웃의 맨왼쪽값을 빌려오는것. 
// 왼쪽자식의 맨 오른쪽값은, 부모노드의 해당위치값이 내려가게되고, 
// 부모노드의 해당위치값으로 오른쪽자식의 맨 왼쪽값이 올라온다. (회전느낌)
void borrowFromRight(struct BTreeNode* par_node, int cur_node_pos){
	//부모노드(par_node)와 현재노드위치(cur_node_pos)를 인자로받음. 이미 현재노드의 키는 지워졌음. cnt_key는 최소상태 혹은 미만임.
	int tenant_idx = par_node->child[cur_node_pos]->cnt_key;//빌리는 주체노드에 빌려주는 키가 들어가야할 위치 (맨 오른쪽)
	
	par_node->child[cur_node_pos]->key[tenant_idx]=par_node->key[cur_node_pos]; // 빌리는 키는 오름차순 상 부모에게서 빌려온다. 그리고 형제노드의 키가 위로 올라간다.
	par_node->child[cur_node_pos]->cnt_key++;

	int idx_from_sib_topar=0;
	//부모노드는 빌려준 형제노드의 키를 가져옴
	par_node->key[cur_node_pos]=par_node->child[cur_node_pos+1]->key[idx_from_sib_topar]; // 부모노드는 빌려준 형제의 키를 들고온다. 

	//오른쪽형제노드의 0번짜 키를 빌려줬으므로, 인덱스 재정렬
	for (int i=0; (par_node->child[cur_node_pos+1]->cnt_key)-1;i++){
		par_node->child[cur_node_pos+1]->key[i]=par_node->child[cur_node_pos+1]->key[i+1];
	}
	par_node->child[cur_node_pos+1]->cnt_key--;

	//오른쪾형제노드 child받아오고, 오른쪽형제노드의 child도 정리(앞으로한칸씩당김)
	int idx_from_sib=0;
	if(par_node->child[cur_node_pos+1]->cnt_child>0){
		int tenant_child_idx=par_node->child[cur_node_pos+1]->cnt_child;
		//빌려받은녀석의 오른쪽자식으로, 오른쪽형제의 0번째 child붙여줘
		par_node->child[cur_node_pos]->child[tenant_idx] = par_node->child[cur_node_pos]->child[idx_from_sib];
		par_node->child[cur_node_pos]->cnt_child++;

		//오른쪽 형제노드의 child 한칸씩 당기고 cnt_child--;
		for (int i=0; (par_node->child[cur_node_pos+1]->cnt_key)-1; i++){
			par_node->child[cur_node_pos+1]->key[i] = par_node->child[cur_node_pos+1]->key[i+1];
		}
		par_node->child[cur_node_pos+1]->cnt_child--;
	}
}

// 현재노드와 자식노드에서의 위치를 인자로 받는 함수 -> 빌리기 , 병합을 진행
void balanceNode(struct BTreeNode* node, int child_pos){
// 자식노드 키 위치가 맨 왼쪽일 때는 오른쪽 부모, 형제를 봐야함
	if (child_pos==0){
	//if 자식노드 기준에서 형제의 키 개수가 최소 숫자 범위 안부서질때
	//else 부서지면 부모(현재노드)와 지우는 노드랑 병합대상 노드 위치를 같이 넘겨줌
		if(node->child[child_pos]->cnt_key > min_keys){borrowFromLeft(node, child_pos);}
		else{mergeNode(node,child_pos, child_pos-1);}
		return ;
	}else{
//맨 왼쪽, 맨 오른쪽 말고 그 외의 위치일 때	
        if(node->child[child_pos-1]->cnt_key > min_keys){borrowFromLeft(node,child_pos);}
		else if(node->child[child_pos+1]->cnt_key > min_keys){borrowFromRight(node, child_pos);}
		else{mergeNode(node,child_pos,child_pos-1);}//양끝이 아닌 중간에 
		return ;	
	}
}
//내부노드 기준으로 자식들을 merge 해야하는 케이스
int mergeChildNode(struct BTreeNode* par_node, int cur_node_pos){
//merge는 왼쪽 기준으로 하는데, 자식노드에서 합쳐질 위치 지정. 
	int mergeidx=par_node->child[cur_node_pos]->cnt_key;
// 바로 지우지 않고, 합치려고 하는 노드에 지우려고 하는 부모노드(내부노드)의 값을 합침.
// 왜냐? -> 바로비우고 자식노드만 합치면, 합치려고 하는 노드 밑에 또 자식노드가 있을 경우, 자식 1개가 낙동강오리알됨
	int val_par_node = par_node->key[cur_node_pos]; //지우려는 부모노드 값 기억
	par_node->child[cur_node_pos]->key[mergeidx] = par_node->key[cur_node_pos];
	par_node->child[cur_node_pos]->cnt_key++;

	//합치려는 노드에 형제노드 값을 가져옴 (원래함수목적)
	for(int i=0;i<par_node->child[cur_node_pos+1]->cnt_key ; i++){
		par_node->child[cur_node_pos]->key[mergeidx+1+i] = par_node->child[cur_node_pos+1]->key[i];
		par_node->child[cur_node_pos]->cnt_key++;
	}
	//형제노드 자식들도 가져와야함
	for (int i=0; i< par_node->child[cur_node_pos+1]->cnt_child; i++){
		par_node->child[cur_node_pos]->child[mergeidx+1+i] = par_node->child[cur_node_pos+1]->child[i];
		par_node->child[cur_node_pos]->cnt_child++;
	}
	//부모노드(내부노드)의 키를 젔으니 재배열 & 자식도 재배열
	for (int i=cur_node_pos; i<par_node->cnt_key;i++){
		par_node->key[i]=par_node->key[i+1];
		par_node->cnt_key--;
	}
	for (int i=cur_node_pos+1; i< par_node->cnt_child;i++){
		par_node->child[i]=par_node->child[i+1];
		par_node->cnt_child--;
	}
	//부모노드에서 내린 값을 지우기 위해 일단 리턴, 값을 삭제하는 함수에서 지워질 예정
	return val_par_node;
}

//Predecessor 찾는 함수 (지금값 바로 전의값 찾기)
int findPredecessor(struct BTreeNode* cur_node){
	// int predecessor;
//현재 탐색노드가 리프이면, 찾을 수 있음 -> 현재노드에서 가장 큰 키 주면됨.
	if (cur_node->leaf){return cur_node->key[cur_node->cnt_key-1];}
	return findPredecessor(cur_node->child[(cur_node->cnt_child)-1]);
//탐색할 때마다 큰쪽 자식으로 탐색해야함.
}
// predecessor 찾아서 내부노드에 덮어씌우는 함수
int overrideWithPred(struct BTreeNode* par_node, int pos_std_search){
//predecessor를 재귀로 쭉 내려가서 찾는 함수 호출, 부모노드랑 타고 내려갈 위치를 인자로 받음
	int predecessor=findPredecessor(par_node->child[pos_std_search]);
	par_node->key[pos_std_search]=predecessor;
	return predecessor;
}

int findSuccessor(struct BTreeNode* cur_node){
	// int successor;
// 현재 탐색노드가 리프이면,찾을 수 있음 -> 현재노드의 0번인덱스를 주면됨.
	if (cur_node->leaf){return cur_node->key[0];}
	return findSuccessor(cur_node->child[0]);
//탐색할 때마다 작은쪽 자식으로 탐색해야함.
}

//successor 찾아서 내부노드에 덮어씌우는 함수
int overrideWithSucc(struct BTreeNode* par_node, int pos_std_search){
// Successor를 재귀로 쭉 내려가서 찾는 함수 호출. 부모노드랑 내려갈 위치 인자로받음
	int succcessor=findSuccessor(par_node);
	par_node->key[pos_std_search]=succcessor;//변경수행
	return succcessor;
}
 
 // 내부노드에서 값을 지우는 함수
 void deleteInnerNode(struct BTreeNode* cur_node, int cur_node_pos){
	 int cessor=0; //pred 혹은 succ가 있을경우 || merge할 경우의 찾은 값을 담은 변수
	 int deletion_for_merge=0;
	 //왼쪽 오른쪽 중 어느쪽 자식이 더 많은지 확인, pred 혹은 succ를 찾아야하기 때문. 
	 //만약 같으면 무조건 왼쪽을 보도록 강제함.
	 if (cur_node->child[cur_node_pos]->cnt_key >= cur_node->child[cur_node_pos+1]->cnt_key){ // 왼쪽이 더 많거나 같다면
		 if (cur_node->child[cur_node_pos]->cnt_key > min_keys){
			 //자식 키 개수가 최소범위보다 작지 않으면 predessor찾기 가능
			 cessor=overrideWithPred(cur_node, cur_node_pos);
			 
			 //찾은 pred를 위로 올려야함. 근데 이 과정이 결국 해당 리프노드에서 값을 지우는게 효과라서 삭제하는 함수 호출
			 deleteValFromNode(cessor, cur_node->child[cur_node_pos]);
		 }else{//키개수가 부족? -> Merge
			 deletion_for_merge=mergeChildNode(cur_node, cur_node_pos);
			 deleteValFromNode(deletion_for_merge, cur_node->child[cur_node_pos]);
		 }
	 }else{
		 if (cur_node->child[cur_node_pos+1]->cnt_key > min_keys){
			 cessor = overrideWithSucc(cur_node, cur_node_pos);
			 deleteValFromNode(cessor, cur_node->child[cur_node_pos+1]);
			 //successor 찾으면 이것도 리프노드에서 지우는 효과를 내야함.
		 }else{
			 deletion_for_merge=mergeChildNode(cur_node,cur_node_pos);
			 deleteValFromNode(deletion_for_merge, cur_node->child[cur_node_pos]);
		 }
	 }
 }


int main(int argc, char** argv) {
	return 0;
}
