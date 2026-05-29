#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/net.h>

int main(int argc,char * argv[])
{
    int cfd;
    char buf[100];
    struct sockaddr_in serv;

    if(argc != 3)
    {
        printf("Usage:%s <IP><PORT>\n",argv[0]);
        return 1;
    }
    
    cfd = socket(AF_INET,SOCK_STREAM,0);

    serv.sin_family = AF_INET;
    serv.sin_port =htons(atoi(argv[2]));
    serv.sin_addr =inet_addr(argv[1]);

    connect(cfd,(struct sockaddr*)&serv,sizeof(serv));

    printf("Enter Message:");
    scanf("%s",buf);

    write(cfd,buf,sizeof(buf));

    read(cfd,buf,sizeof(buf));

    printf("Server reply:%s\n".buf);
    close(cfd);
    return 0;
}
