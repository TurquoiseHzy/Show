/*
作者：黄子懿，刘子威，许骏洲
KDTree.h:
定义了Data、KDTree

*/
#ifndef KDTREE_H
#define KDTREE_H
#define NEWFANGFA     //是否使用数据库文件名作为分类依据

using namespace std;
#include<iostream>
#include<vector>
#include<algorithm>
#include<string>
extern int TYPENUM;

/*
Data:
存储数据
m_fileName：数据文件名
type：数据所在累
code：数据编码
feature：数据特征向量
*/
template<int KD>
class Data{
public:
	string m_fileName;
	int type;
	int code;
	vector<double> feature;

public:
	Data(){ 
		feature.resize(KD);
	};
	~Data(){ 
		vector <double>().swap(feature);
	};

};

/*
KD树节点
存储:
father、rightchild、leftchild：指针，指向其他节点
isLeaf：是否为叶节点
ptData：指针，指向数据
split：以该节点为根的子树的分割域
*/
template<int KD>
class KDNode{
public:
	bool isLeaf;
	KDNode *father,*rightchild,*leftchild;
	Data<KD>* ptData;
	int split;
public:
	KDNode():
		isLeaf(false),
		ptData(NULL),
		father(NULL),
		rightchild(NULL),
		leftchild(NULL)
	{};
	~KDNode() {
		delete ptData;
	};
public:
#ifdef OUT_DEBUG
	void output()
	{
		cout<<"Code:"<<ptData->code<<endl;
		if(leftchild!= NULL)
			cout<<"		LCode:"<<leftchild->ptData->code<<endl;
		if(rightchild != NULL)
			cout<<"		RCode:"<<rightchild->ptData->code<<endl;
	}
#endif
};


/*
KDTree类
支持build和search接口


*/

template<int KD>
class KDTree{

public:

	KDNode<KD> *Root;
	int treeSize;

public:
	KDTree():
		Root(NULL),
		treeSize(0){};
	~KDTree(){};

public:
	/*
	bulid(data,datacount)
	data:数据集头指针
	datacount:数据个数
		*/
	void build(Data<KD>* data,int dataCount){
		treeSize = dataCount ;
		Root = new KDNode < KD > ;
		buildSubtree(data ,dataCount ,Root );
	};

private://build用私有函数

	void qs(int l,int r,int split,Data <KD>* data){
		if( l >= r)
			return ;
		int lp=l,rp =r;
		Data <KD> key = data [l];
		while(lp < rp)
		{
			while(lp < rp && data[rp].feature[split] >= key.feature[split])
			{
				--rp;
			}
 
			data[lp] = data[rp];
 
			while(lp < rp && data[lp].feature[split] <= key.feature[split])
			{
				++lp;
			}
         
			data[rp] = data[lp];    
		}
		data[lp] = key;
		qs(l,lp-1,split,data);
		qs(lp+1,r,split,data);
	}

	void buildSubtree(Data<KD>* data,int dataCount,KDNode <KD> * root){
		
		if(dataCount == 1){
			root->ptData = data ;
			root->isLeaf = true ;
			return ;
		}

		int split = root->father == NULL ? 6 : (( root -> father->split + 1 ) %  KD);
		
		Data <KD>* copy = new Data<KD> [ dataCount ];
		Data <KD> temp ;
		for ( int i = 0 ; i < dataCount ; i ++ )
		{
			copy [ i ] = data [ i ];
		}
		int k = 0;
		qs(0,dataCount  - 1,split,copy);

		int leftCount = dataCount / 2 , rightCount = dataCount - leftCount - 1;
		int midCode = copy [ leftCount ].code;

		for ( int i = 0 ; i < dataCount ; i ++)
		{
			if(data[ i ].code == midCode)
			{
				root->ptData = data + i ;
				break;
			}
		}
		KDNode < KD >*leftchild,*rightchild;
		root->split = split ;
		if(leftCount > 0)
		{
			leftchild = new KDNode < KD >;
			root->leftchild = leftchild;
			leftchild->father = root;
			buildSubtree( copy , leftCount , leftchild);
		}
		if(rightCount > 0)
		{
			rightchild = new KDNode < KD >;
			rightchild->father = root;
			root->rightchild = rightchild;
			buildSubtree( copy + leftCount + 1, rightCount, rightchild );
		}
	} 

private://search用跨成员函数私有量
	KDNode<KD> **priorQ;
	double *PQdis;
	int priorQsize;
	double *resultDis;
	Data<KD>* result;
	int resGet;

public:
	/*
	Data<KD>* search*search(resNum,target,dis):搜索target在dis意义下的resNum近邻
	返回：指向搜索结果的头指针，NULL表示空树
	resNum:返回近邻数
	target:目标向量
	dis:两个vector<double>之间的距离函数
	*/
	Data<KD>* search(int resNum, vector<double> target,double (*dis)(vector<double> & n,vector<double> & t)){
#ifdef NEWFANGFA
		int resNeed=resNum;
		resNum =5*resNeed;
#endif
		if(Root == NULL){
			return NULL;
		}
		resGet = 0;
		priorQ = new KDNode <KD> *[treeSize];
		PQdis = new double [treeSize];
		priorQ[0]=Root;
		priorQsize = 1;
		result = new Data<KD>[resNum];
		resultDis = new double [resNum];
		while ( priorQsize > 0)
		{
			priorQsize --;
#ifdef OUT_DEBUG
			cout<<"get "<<priorQ[priorQsize]->ptData->code<<" out of PQ"<<endl;
			cout<<"after that PQsize="<<priorQsize<<endl;
#endif
			search_point(resNum,target,dis,priorQ[priorQsize]);
		}
#ifdef NEWFANGFA
		
		int maxtype,maxcount = -1;
		int *typecount = new int [TYPENUM+1];
		for(int i = 1 ; i<=TYPENUM;i++)
			typecount [i] = 0;
		for(int i = 0 ; i<resNeed;i++)
			typecount [result[i].type] ++;
		typecount[result[0].type] +=5;
		for(int i = 1 ; i<=TYPENUM;i++)
			if(typecount [i] > maxcount )
			{
				maxcount = typecount [i] ;
				maxtype = i;
			}
		if(result[0].type==maxtype)
        {
		Data<KD> tmp;
		for(int i = 0 ;i< resNeed ;i++)
			for(int j = resNeed;j<resNum ;j++)
				if(result[i].type!=maxtype &&result[j].type== maxtype)
				{
					tmp = result [i];
					result[i]=result [j];
					result[j]=tmp;
					break;
				}
		}
				
#endif
				
		delete []priorQ;
		delete []PQdis;
		delete []resultDis;
		return result ;
	};
	
private:
	// KDtree.search用私有函数
	void search_point(int resNum, vector<double> target,double (*dis)(vector<double> & n,vector<double> & t),KDNode <KD> * now)
	{
		
#ifdef OUT_DEBUG
		cout<<"is searching"<<now->ptData->code<<endl;
#endif
		tryputIntoresult(now->ptData,dis(now->ptData->feature,target),resNum);
		if( now->isLeaf == true )
		{
			return ;
		}
		
		int s = now->split;
		if( target[s] < now->ptData->feature[s])
		{
			if(now->rightchild != NULL)
			{
				putIntoPQ(now->rightchild,abs(now->ptData->feature[s] - target[s]));
			}

			if(now->leftchild != NULL)
			search_point(resNum,target,dis,now->leftchild);

		}
		else
		{
			if(now->leftchild != NULL)
			{
				putIntoPQ(now->leftchild,abs(now->ptData->feature[s] - target[s]));
			}
			if(now->rightchild != NULL)
			search_point(resNum,target,dis,now->rightchild);
		}
		
#ifdef OUT_DEBUG
		cout<<"search "<<now->ptData->code<<"over"<<endl;
#endif
	}

	void putIntoPQ(KDNode <KD> *node,double nodeDis){
		
#ifdef OUT_DEBUG
		cout<<"is trying to put"<<node->ptData->code<<"into PQ"<<endl;
#endif
		if(nodeDis > resultDis[resGet - 1])
			return ;
		int pos=-1;
		if(priorQsize==0 || nodeDis>PQdis[0])
			pos = 0;
		else
			for(int i = 0 ; i<priorQsize;i++)
			{
				if(PQdis[i] < nodeDis)
					pos = i;
			}
		if ( pos ==-1)
			pos = priorQsize;
		for(int i = priorQsize ; i >pos ;i --)
		{
			priorQ[i]= priorQ[i-1];
			PQdis[i]=PQdis[i-1];
		}
		priorQ[pos] = node;
		PQdis[pos] = nodeDis;
		priorQsize ++ ;
		
		
#ifdef OUT_DEBUG
		cout<<"after that PQ is:"<<endl;
		for(int i = 0 ;i <priorQsize;i++)
			cout<<"    "<<priorQ[i]->ptData->code<<endl;
		
#endif
		return ;
	}

	void tryputIntoresult(Data<KD>* now,double nowDis,int resNum){
#ifdef OUT_DEBUG
		cout<<"is trying to put"<<now->code<<"into result"<<nowDis<<endl;
		
#endif
		bool isFull = (resNum == resGet);
		if(isFull && resultDis[resGet-1] <= nowDis)
			return ;
		if(!isFull)
			resGet ++;
		int pos=-1;
		if(resGet == 0 || nowDis < resultDis[0])
			pos = 0;
		else
			for(int i = resGet-1;i>=0 ;i--)
				if(resultDis[i] > nowDis)
					pos  = i ;
		if(pos == -1)
			pos = resGet-1;
		for(int i = resGet - 1 ;i > pos;i--)
		{
			resultDis[i] = resultDis[i-1];
			result[i]=result [i - 1];
		}
		resultDis[pos] = nowDis;
		result[pos] = *now ;
#ifdef OUT_DEBUG
		cout<<"after that result size="<<resGet<<endl;
		for(int i = 0 ;i <resGet;i++)
			cout<<"    "<<result[i].code<<"    "<<resultDis[i]<<endl;
#endif
		return ;
	}

};
//类定义结束
#endif 