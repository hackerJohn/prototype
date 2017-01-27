#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include "edsim_naive.h"

//返回随机数
double Bern(double r);

//初始设置
//平均到达间隔（期望）
double g_avg_arrv_intv = 5;
//平均服务时间（期望）
double g_avg_serv_time = 500;

//统计用户数目
int g_online_user_cnt = 0;

FILE *g_log_file = NULL;

void userArrival(void);
void userDeparture(void);
void logOnlineUserCount(void);

int main(int argc, const char *argv[])
{
	g_log_file = fopen("online_user_cnt.txt", "w");
	if (g_log_file==NULL){
		fprintf(stderr, "Open log file failed\n");
		return 1;
	}

	double end_time = 100000;


	Event first_arrv(0.0, &userArrival);
	enqueue(first_arrv);

	run_sim(end_time);

	fclose(g_log_file);
	return 0;
}

void logOnlineUserCount(void)
{
	fprintf(g_log_file, "%f %d\n", now(), g_online_user_cnt);
}

void userDeparture(void)
{
	--g_online_user_cnt;
	logOnlineUserCount();
}

void userArrival(void)
{
	++g_online_user_cnt;
	logOnlineUserCount();

	double interval = Bern(g_avg_arrv_intv)*g_avg_arrv_intv;
	double serv_time = Bern(g_avg_serv_time)*g_avg_serv_time;
	Event next_arrv(now()+interval, &userArrival);
	Event departure(now()+serv_time, &userDeparture);
	enqueue(next_arrv);
	enqueue(departure);
}

//随机数生成
double uniform()
{
	return ((double)rand())/( ((double)(RAND_MAX)) + 1);
}
//伯努力分布（0-1分布）
double Bern()
{ 
	return ((int(uniform())%2)); 
}
double Bern(double r)
{ 
	return (int(r * bern())%2);
}
