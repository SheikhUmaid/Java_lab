#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/net.h>

int main(int argc,char * argv[])
{
    int sfd,cfd;
    char buf[100];
    struct sockaddr_in serv;

    if(argc != 2)
    {
        printf("Usage:%s <PORT>\n",argv[0]);
        return 1;
    }

    sfd = socket(AF_INET,SOCK_STREAM,0);

    serv.sin_family = AF_INET;
    serv.sin_port =htons(atoi(argv[1]));
    serv.sin_addr.s_addr = INADDR_ANY;

    bind(sfd,(struct sockaddr*)&serv,sizeof(serv));
    listen(sfd,5);
    cfd = accept(sfd,NULL,NULL);

    read(cfd,buf,sizeof(buf));
    printf("Client Message:%s\n",buf);
    strcpy(buf,"Message received");
    write(cfd,buf,sizeof(buf));

    close(sfd);
    close(cfd);
    return 0;
}
