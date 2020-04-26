Git-Basics-with-Demo-Startup-Guideline

# Git基本操作与Demo项目初运行指南

&emsp;&emsp;为了精准把控项目开发过程，我们使用Git版本控制工具来便利化我们的协作。这个文档整合了Git基本操作方法并结合Demo项目详解了主要操作流程，的目的是为了让各位初步掌握Git地相关操作，并顺利地使用Demo项目。

## Git基本操作说明
&emsp;&emsp;这里先将主要的操作进行简要列举说明，下一小节将结合整个操作流程进行演示。

Git工具的核心是解决了本地项目文件与远程仓库文件之间的关系，它主要包括以下个经常使用的模块：
1. **克隆（Clone）**：用于将远程仓库克隆至本地；
2. **拉取（Pull）**：用于将远程仓库的变更同步到本地仓库；
3. **本地修改（包括新建与删除）**：在本地仓库中进行代码编写；
4. **提交（Commit）**：用于将本地仓库文件的变更进行整合打包；
5. **推送（Push）**：用于将准备好的提交推送至远程仓库；
6. **分支（Branch）**：用于在远程仓库建立新的同当前仓库中文件独立的节点；
7. **合并（Merge）**:用于将不同分支进行合并。

&emsp;&emsp;项目开发过程中，建议每人在原有分支的基础上建立属于自己的分支，可保证开发过程互不干涉。

## Demo项目初运行指南

### 配置Git环境
&emsp;&emsp;将Git同使用的代码编辑器/IDE结合使用，目前主要有两种模式：
* 使用GitHub Desktop与Sublime Text等编辑器结合
* 使用Git命令行与Pycharm等IDE结合

&emsp;&emsp;在这里我们使用第一种方案进行演示。

&emsp;&emsp;访问https://desktop.github.com/ ，并下载合适的版本进行安装，即可完成配置。

### 克隆项目到本地
&emsp;&emsp;打开GitHub Desktop，登录账号，进入程序主界面；
&emsp;&emsp;点击左上角File->Clone a repository，在弹出页面中选择"GitHub.com"，选择仓库"SJTU_ZHFY"与本地路径，开始克隆。
&emsp;&emsp;点击左侧上部"Current repository"选择项目后，选择"Current branch"，点击"New branch"，选择基于"reconstructed"创建新分支,再点击"Fetch origin"刷新；

### 项目运行
&emsp;&emsp;打开命令行，切换至仓库目录下，执行：

```
python manage.py runserver 80
```
		
&emsp;&emsp;依据提示安装完所需要的依赖，打开浏览器输入地址127.0.0.1/overview/， 便可以见到网站了。

&emsp;&emsp;在运行过程中可能会遇到些问题，请及时联系相关人员。


### 项目施工
&emsp;&emsp;此时主界面右侧应显示"No local changes"，可以直接点击下方的""Open the repository in your external editor"。并可以开始工作，可以注意到，本地仓库目录下任何文件的改动都将被记录在GitHub Desktop程序中。

### 创建提交与推送
&emsp;&emsp;在完成了一阶段工作以后在GitHub Desktop中左侧下方填写提交的主题与描述，并进行提交。提交后原"Fetch origin"按钮会变为"Push origin"，点击即可完成推送。
















