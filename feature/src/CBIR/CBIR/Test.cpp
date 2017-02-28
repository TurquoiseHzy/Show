/*
作者：黄子懿，刘子威，许骏洲
*/
#include"ReadDataBase.h"
#include"Test.h"
int TYPENUM;
Data<30> *TDATA = new Data<30>[DATANUM];
double el_dis(vector<double> &a,vector<double> &b){
	double res = 0;
	for(unsigned int i = 0 ;i < a.size();i++){
		res += (a[i] - b[i]) * (a[i] - b[i]);
	}
	return sqrt(res);
}
double power[30]={10,10,10,15,15,15,
									4,4,4,8,8,8,
									2,2,2,4,4,4,
									1,1,1,1,1,1,
									1,1,1,1,1,1,
	};
#ifdef	NEWFANGFA
vector<string> contentType;
#endif

//批量测试
void gb_test()
{
	
	readDatabase(TDATA);
	for(int i = 0 ;i < DATANUM ;i++)
	{
#ifdef	NEWFANGFA
		if(contentType.size()==0||contentType[contentType.size()-1] != CONTENT(TDATA[i]))
		{
			contentType.push_back(CONTENT(TDATA[i]));
			TYPENUM ++;
		}
		TDATA[i].type = contentType.size();
#endif
		for(int j = 0;j<30;j++)
			TDATA[i].feature[j] *= power[j];
	}
	KDTree<30> tree;
	tree.build(TDATA,DATANUM);
	Data<30> *result;
	string path;
	path=".//ir//";
	ofstream resultout("res.txt");
	Data<30> *query = new Data <30>[QNUM];
	readQuery(query,path);
	int count = 0,c=0;
	for(int i = 0;i<QNUM;i++)
	{
		result = tree.search(BACKNUM,query[i].feature,el_dis);
		resultout<<query[i].m_fileName<<":";
		for(int j = 0 ; j <BACKNUM ; j++)
		{
			resultout<<result[j].m_fileName;
			if(j<BACKNUM-1)
				resultout<<",";
			else
				resultout<<endl;
		if(CONTENT(result[j])==CONTENT(result[0]))
			count ++;
		c++;
		}
	}
	cout<<double(count)/c<<endl;
}