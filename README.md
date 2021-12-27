# py-gen-mur

> python 机器码/用户码/注册码 生成器
<br/> python generate [m]achine_code [u]ser_code [r]egister_code

------

## 运行环境

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)

> 因内含 win32api 依赖包，该包在 Linux 环境下安装会报错，不必理会，不影响使用


## 使用场景说明


### 场景一：用户运行程序，生成机器码（文件），提供给管理员，程序自动终止

TODO

### 场景二：管理员生成用户码（文件）

TODO

### 场景三：管理员解密机器码，结合用户码，生成注册码（文件）

TODO

### 场景四：管理员提供用户码（文件）和注册码（文件）给用户

TODO

### 场景五：用户运行程序，校验三码正确，程序成功运行

TODO



## 开发者说明

<details>
<summary>展开</summary>
<br/>

### 手动打包项目

每次修改代码后，记得同步修改 [`setup.py`](setup.py) 下的版本号 `version='x.y.z'`。

```
# 构建用于发布到 PyPI 的压缩包
python setup.py sdist

# 本地安装（测试用）
pip install .\dist\xxxx-?.?.?.tar.gz

# 本地卸载
pip uninstall xxxx
```

### 手动发布项目

首先需要在 [PyPI](https://pypi.org/) 上注册一个帐号，并在本地用户根目录下创建文件 `~/.pypirc`（用于发布时验证用户身份），其内容如下：

```
[distutils]
index-servers=pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = <username>
password = <password>
```

其次安装 twine 并上传项目： 

```
# 首次发布需安装
pip install twine

# 发布项目， 若发布成功可在此查看 https://pypi.org/manage/projects/
twine upload dist/*
```

发布到 [PyPI](https://pypi.org/) 的项目名称必须是全局唯一的，即若其他用户已使用该项目名称，则无法发布（报错：`The user 'xxx' isn't allowed to upload to project 'yyy'.`）。此时只能修改 [`setup.py`](setup.py) 下的项目名称 `name`。


> 本项目已集成了 Github Workflows，每次推送更新到 master 即可自动打包并发布到 PyPI


### 关于测试

详见 [单元测试说明](tests)


### 参考资料

- [python package 开发指引](https://packaging.python.org/#python-packaging-user-guide)
- [python package 示例代码](https://github.com/pypa/sampleproject)

</details>

## 赞助途径

| 支付宝 | 微信 |
|:---:|:---:|
| ![](imgs/donate-alipay.png) | ![](imgs/donate-wechat.png) |


## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
