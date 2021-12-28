# py-gen-mur

> python 机器码/用户码/注册码 生成器
<br/> python generate [m]achine_code [u]ser_code [r]egister_code

------

## 运行环境

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)

> 因内含 win32api 依赖包，该包在 Linux 环境下安装会报错，不必理会，不影响使用


## 使用场景说明

> 详见 [测试用例](./tests/test.py)


### 场景步骤一（管理员本地，可选）

因代码开源，不建议使用 `crypt.Crypt()` 默认类。

建议使用此工具时，自定义指定 `crypt.Crypt()` 构造函数的 `key` 和 `iv` 。

本代码中提供了 `crypt.gen_des_key()` 和 `crypt.gen_des_iv()` 的方法，但是生成后必须找地方另外存储这两个值，否则之前使用其生成的注册码无法再解密。

```python
from crypt import *

my_des_key = gen_des_key()
my_des_iv = gen_des_key()

my_crypt = Crypt(
    key = my_des_iv, 
    iv = my_des_iv
)
```


### 场景步骤二（用户本地）

1. 用户运行【生成机器码】的程序
2. 生成放有【加密机器码】的文件
3. 把【加密机器码】的文件提供给管理员


```python
from user import *

u_machine_code = gen_machine_code()
```

### 场景步骤三（管理员本地）

1. 管理员解密用户提供的【加密机器码】文件
2. 同时为用户分配【随机用户码】文件
3. 结合两者生成【注册码】文件
4. 把【随机用户码】文件和【注册码】文件提供给用户

```python
from admin import *

a_machine_code = read_machine_code()
a_user_code = gen_user_code()
a_register_code = gen_register_code(
    a_machine_code, a_user_code
)
```


### 场景步骤四（用户本地）

1. 用户运行应用主程序
2. 主程序读取【用户码】文件（或让用户输入用户码）
3. 主程序在用户本地重新生成【机器码】
4. 主程序利用【用户码】和【机器码】生成【注册码】
5. 主程序比对【生成的注册码】和【管理员提供的注册码】内容是否一致
6. 若一致，程序运行；否则，程序终止

```python
from user import *

u_user_code = read_user_code()
rst = verify_authorization(u_user_code)
if rst == True :
    app.run()
else :
    exit(1)
```


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
pip install .\dist\py-gen-mur-?.?.?.tar.gz

# 本地卸载
pip uninstall py-gen-mur
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
