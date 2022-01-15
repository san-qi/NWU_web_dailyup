# NWU_web_dailyup

西北大学晨午检填报 web 版本(后续不再维护)

    当你决定部署之前, 请通读一遍该文档

想要查看具体效果请点击[这里](http://sanqii.top/dailyup/index.html)（该网站可能已被停用，你可能需要自己部署）。 你甚至可以直接将信息记录在该网站中而不需要亲自部署, 并且该网站完全用该开源项目部署的, 你绝对可以相信它

## 用途

基于网页的晨午检填报方案, 通过 docker 完成部署后, 可以很轻易的让使用该项目的用户通过浏览器自主配置填报项目

其中个性化配置项包括：

- 在校状态

  对应晨午检"是否在校"一项

- 填报位置

  对应晨午检"所在地点"一项

- 填报状态

  由用户决定是否开启自动填报

以上配置都可以在网页上自主选择, 无需自主编写相关代码配置

## 结构

一般而言, 你可能只需要关注作为主体的 dailyup 文件夹:

```
.
├── app
│   ├── app.py
│   ├── dailyup.py
│   ├── Dockerfile
│   ├── nwu_report
│   │   ├── aes_crypt.py
│   │   └── util.py
│   └── requirements.txt
├── docker-compose.yml
├── html
│   ├── favicon.ico
│   ├── geoInfo.html
│   ├── index.html
│   ├── login.html
│   └── res
│       ├── pic1.jpg
│       ├── pic2.jpg
│       └── pic3.jpg
├── init
│   └── init.sql
└── nginx
    └── dailyup.conf

6 directories, 16 files
```

## 用法

具体使用分为两步：

1. 部署：

   - 首先, git clone 该项目
   - 项目的部署使用了 docker, 你需要安装且只需要安装它
   - 然后进入 dailyup 文件夹目录下, 执行命令 `sudo docker-compose up -d`, 完成项目的部署
   - 此时, 你可以访问这个链接了-- `http://domain:8082/dailyup` , 将 domain 换成自己的域名或者 ip 即可查看效果
   - 更进一步, **作为拓展项**, 你可以通过外部的 nginx 对 url 进行个性化配置(如果存在所谓的外部 nginx 的话), 这一步当然不是必须的。若如此做, 你可以去掉域名后的端口号(即此处的 8082), 或者可以用子域名的方式来访问。 这需要你对 nginx 有所了解, 可能会有一定的困难, 作为例子, 你可以查看这个[配置文件](./example.conf)

2. 定时填报：

   - 部署完成后, 你当然可以手动运行填报服务, 只需要执行命令 `sudo docker exec nwuapp python dailyup.py`, 即可将记录在数据库中的用户上报至学校。但是结合 crontab 等定时运行命令你可以解放自己, 完成定时填报功能

   - 这一步需要你自己做, 如果你不熟悉 crontab 命令的话, 你可以 google 到相关资料, 虽然这可能有一些困难。但是我还是没有选择用 docker 运行定时命令(事实上可以这样做), 这样做需要额外的 50M 存储空间, 甚至更多, 并不划算

总结一下, 你其实仅仅需要掌握两个命令:

- `sudo docker-compose up -d`, 执行该条命令需要在 dailyup 文件夹下
- `sudo docker exec nwuapp python dailyup.py`, 该命令对当前所处的文件路径无要求
- 其实还有第三条命令: `docker-compose down` , 这条命令可以停掉该服务。 同命令 1, 该命令仅仅在该项目的 dailyup 文件夹下才能生效

## 提示：

- 最好不要对 dailyup 文件夹的内容做任何更改, 除非你清楚你在做什么
- 最好不要在同一主机下部署该项目两次, 在同一主机下的不同项目拷贝下执行两次 `sudo docker-compose up -d` 命令, 否则会出现其它的不良反应
- 因为使用了 docker 来部署环境, 所以你的现有主机环境并不会收到污染, 该项目整体仅占用了你的 8082 端口, 这也是不能部署两次的原因
- 作为上一条提示的提示, 若你服务器中的 8082 端口已经被占用, 并且你能理解自己所作的行为, 请修改 dailyup 目录下 **docker-compose.yml** 文件中的 ports 项, 将其中的 8082 改为你想要的端口
- 前文中提及的两个命令最好是用 root 用户来执行**或**将运行该命令的用户加入到 docker 用户组中, 并去掉 sudo 命令前缀。 因为 crontab 可能不支持在其中定时执行内嵌 sudo 前缀的命令 (该条提醒是对 linux 下的部署而言)

## 作者

西北大学蒟蒻本科生

## 授权

无偿开源, 请遵循[GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)开源许可
