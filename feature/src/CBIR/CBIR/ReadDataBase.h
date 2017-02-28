/*
作者：黄子懿，刘子威，许骏洲
ReadDataBase.h
读取特征函数数据库、计算特征函数的定义

*/
#ifndef READDATABASE_H
#define READDATABASE_H
#include<fstream>
#include<io.h>
#include "KDTree.h"
#include "atlimage.h"
#define DATANUM 5613  //数据集大小
#define QNUM 2000		//查询集大小



extern double power[30];
const double Pi = 3.1415926535898;
const double sqr2pi = sqrt(2*Pi);
//读取数据库
void readDatabase(Data<30> *data){
	ifstream fin("FinalDataBase.txt");
	for(int i = 0 ; i<DATANUM ;i++)
	{
		fin>>data[i].m_fileName;
		for(int j=0 ;j < 30;j++)
			fin>>data[i].feature[j];
		data[i].code = i ;
	}
	return ;
}

//获取文件名供输出用
void getFiles( string path, vector<string>& files ) 
{  
    long   hFile   =   0;    
    struct _finddata_t fileinfo;    
    string p;  
    if   ((hFile   =   _findfirst(p.assign(path).append("/*").c_str(),&fileinfo))   !=   -1)  {    
  
        do  {    
            if   ((fileinfo.attrib   &   _A_SUBDIR)) {    
                if   (strcmp(fileinfo.name,".")   !=   0   &&   strcmp(fileinfo.name,"..")   !=   0)    
                    getFiles(   p.assign(path).append("/").append(fileinfo.name), files   );    
            }  else  {    
                files.push_back(p.assign(fileinfo.name));  
            }    
        }   while   (_findnext(   hFile,   &fileinfo   )   ==   0);    
  
        _findclose(hFile);    
    }  
} 

//用正态分布替代二项分布
double w(double r, double alpha, int N)
{
	/*
    if(N<100){
    double c = fac(r+1,N)/fac(1,N-r);
    return c*pow(alpha,N);
    }*/
    return exp(-(r-N/2.0)*(r-N/2.0)*2.0/N)/sqr2pi*2/sqrt(N);
}

double fac(int a, int b)
{
    double sum = 1;
    while (a<=b)
    {
        sum *= a;
        a++;
    }
    return sum;
}

double K(double r, double alpha, int N, int n)
{
    double sum=0;
    for (int i = 0; i <= n; ++i)
    {
        sum+=fac(-n,-n+i-1)*fac(-r,-r+i-1)/fac(-N,-N+i-1)*(pow(1/alpha,i)/fac(1,i));
    }
    //(1-alpha)/alpha = 1
    double rou = abs(fac(1,n)/fac(-N,-N+n-1));
    return sum*sqrt(w(r,alpha,N)/rou)/sqrt(sqrt(N));
    //w(r,alpha,N)
}

//计算特征向量
void getvector(wstring imageName,vector<double> & ft)
{
	const double alpha = 0.5;
    ft.clear();
    ft.resize(30,0);
	CImage image;
	LPCTSTR name=imageName.c_str();
	image.Load(name);
    double h = image.GetHeight(), w = image.GetWidth();
    COLORREF rgb;
    double yuv[3], midyuv[3]= {0}, midsqr[3] = {0}, edgeyuv[3]={0}, edgesqr[3] = {0};
    double sum[3]={0}, sqr[3]={0};
    int byteR,byteG,byteB;
    int i,j,k;
    double M = 0, E = 0;
    for ( int x=0; x<w; x++)
    {
        for ( int y=0; y<h; y++)
        {
            rgb = image.GetPixel(x,y);
            byteR = ((rgb >> 16) & 0xff);
            byteG = ((rgb >> 8) & 0xff);
            byteB = rgb & 0xff;
            yuv[0]=16+0.257*byteR+0.504*byteG+0.098*byteB;
            yuv[1]=128-0.148*byteR-0.291*byteG+0.439*byteB;
            yuv[2]=128+0.439*byteR-0.368*byteG-0.071*byteB;
            for(i = 0; i < 3; ++i)
            {
                sum[i]+=yuv[i];
                sqr[i]+=yuv[i]*yuv[i];
            }
            if ( x >=0.25*w && x <= 0.75*w && y >= 0.25*h && y<=0.75*h )
            {
                for(i = 0; i < 3; ++i)
                {
                    midyuv[i]+=yuv[i];
                    midsqr[i]+=yuv[i]*yuv[i];
                }
                M++;
            }
            else
            {
                for(i = 0; i < 3; ++i)
                {
                    edgeyuv[i]+=yuv[i];
                    edgesqr[i]+=yuv[i]*yuv[i];
                }
                E++;
            }
            for (i = 0; i <= 2; i++)
            {
                for (j = 1; j < 3; j++)
                {
                    for (k = 1; k < 3; k++)
                    {
                        ft[18+4*i+2*j+k-3] += K(x,alpha,w-1,j)*K(y,alpha,h-1,k)*yuv[i];
                    }
                }
            }
        }
    }

    for(i = 0; i < 3; ++i)
    {
        ft[i] = midyuv[i] / M;
        ft[3+i] = sqrt(   midsqr[i]/ (M-1) - M / (M-1) * (ft[i] * ft[i] )   );
        ft[6+i] = edgeyuv[i] / E;
        ft[9+i] = sqrt(   edgesqr[i]/(E-1) - E / (E-1) * (ft[6+i] * ft[6+i] )  );
        ft[12+i] = sum[i] / (M+E);
        ft[15+i] = sqrt(   sqr[i]/(M+E-1) - (M+E) / (M+E-1) * (ft[12+i] * ft[12+i] )  );
    }
    for(i = 0; i < 30; ++i)
    {
        ft[i]*=power[i];
    }
}


//获取查询集
void readQuery(Data<30> *query,string path){
	
	vector<string > queryName;
	getFiles(path,queryName);
	ifstream qin("queryFeature.txt");
	for(int i = 0 ; i<QNUM;i++)
	{
		query[i].m_fileName=queryName[i];
			for(int j = 0 ;j < 30;j++)
				qin>>query[i].feature[j];
	}
}
#endif