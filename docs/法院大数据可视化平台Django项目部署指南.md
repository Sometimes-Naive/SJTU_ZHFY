法院大数据可视化平台Django项目部署指南

# 法院大数据可视化平台Django项目部署指南

1. 基本环境配置
* Python环境配置（略）
Python(v3.8)执行文件目录：/usr/bin/python
旧版目录：/usr/bin/python2.7

* Nginx服务器安装（略）
./configure配置：
添加nginx用户：
	
	```shell
	useradd -s /sbin/nologin -M nginx
	id nginx
	```
* 拷贝项目工程文件（用户与组均设为nginx）

- 2. 服务器配置
    - 2.1 Nginx注册系统服务
		- 创建服务文件：
		```
		vim /usr/lib/systemd/system/nginx.service 
		```

		- 服务文件内容：
		```
		[Unit]
		Description=nginx - high performance web server
		After=network.target remote-fs.target nss-lookup.target
		
		[Service]
		Type=forking
		ExecStart=/usr/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
		ExecReload=/usr/sbin/nginx -s reload
		ExecStop=/usr/sbin/nginx -s stop
		
		[Install]
		WantedBy=multi-user.target
		```
		
		- 启动服务：systemctl start nginx
		- 查看状态：systemctl status nginx

	- 2.2 uwsgi安装配置
		- 安装uwsgi
	
		```
		python3 -m pip install uwsgi
		```

		- 测试uwsgi
		在项目根目录下新建测试文件test_uwsgi.py
		
		```python
		# test_uwsgi.py
		def application(env, start_response):
		    start_response('200 OK', [('Content-Type','text/html')])
		    # return ["Hello World"] # python2
		    return [b"Hello World"] # python3
	    ```
	    
	    	然后执行shell命令
	    
	    ```shell
	    uwsgi --http :8001 --plugin python --wsgi-file test.py
	    ```
	    
	    	执行成功访问
    	```shell
    	curl http://localhost:8001
    	```
	    	显示Hello World说明uwsgi正常运行。关闭uwsgi：
    	```
    	ps aux|grep uwsgi|cut -c 9-15|xargs kill -9
    	```

		- 测试Django
		    首先得保证Django项目没有问题
		    
		```shell
		python manage.py runserver 0.0.0.0:8001
		curl http://localhost:8001
		```

			项目运行正常后.链接Django和uwsgi，到Django项目目录下执行
			
		```shell
		uwsgi --http :8001 --plugin python --module configs.wsgi
		```
			检查正常后进行下一步。
			
		- 配置uwsgi
			uwsgi支持通过配置文件的方式启动，可以接受更多的参数，高度可定制。我们在Django项目目录下新建uwsgi.ini
		
			```shell
			# Django-related settings
			
			uid = nginx 
			gid = nginx
			
			#socket = :8001
			socket = mysite.sock
			
			# the base directory (full path)
			chdir           = /var/www/CourtDataVisualization
			
			# Django s wsgi file
			module          = configs.wsgi
			
			# process-related settings
			# master
			master          = true
			
			# maximum number of worker processes
			processes       = 4
			
			# ... with appropriate permissions - may be needed
			chmod-socket    = 664
			# clear environment on exit
			vacuum          = true

			```
			
			完成后运行：
			
			```shell
			sudo uwsgi --ini uwsgi.ini 
			```
			
			
		
		- 配置nginx
			修改nginx配置文件/usr/local/nginx/conf/nginx.conf:
			
			```
			server {
			    # the port your site will be served on
			    listen      80;
			    # the domain name it will serve for
			    server_name 127.0.0.1; # substitute your machine's IP address or FQDN
			    charset     utf-8;
			
			    # max upload size
			    client_max_body_size 75M;   # adjust to taste
			
			    # Django media
			    location /media  {
			        alias /home/ubuntu/blog/media;  # your Django project's media files - amend as required
			    }
			
			    location /static {
			        alias /home/ubuntu/blog/static; # your Django project's static files - amend as required
			    }
			
			    # Finally, send all non-media requests to the Django server.
			    location / {
			        include     uwsgi_params; # the uwsgi_params file you installed
			        #uwsgi_pass 127.0.0.1:8001;
			        uwsgi_pass unix:///var/www/CourtDataVisualization/mysite.sock;
			    }
			}
			```
			

* 

的