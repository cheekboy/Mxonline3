FROM centos:7
env LC_CTYPE=en_US.UTF-8
run yum install -y epel-release && yum install -y gcc python34-pip python34 python34-devel mysql-devel

#run yum install -y https://centos7.iuscommunity.org/ius-release.rpm&&yum makecache
#run yum install -y python36u,pip36u,python36u-devel
#WORKDIR /opt/apps/p8h_backend

COPY . .
run pip3.4 install -r requirements.txt
#package.json /opt/apps/p8h_backend

RUN python3.4 manage.py runserver 

