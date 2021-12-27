# pypi-template

> pypi 开发模板

------

'''
原理
    1. 判断路径下是否存在识别文件，若存在就解密对比，若不存在就进入机器码注册：
    2. 获取系统C盘序列号作为识别ID，并添加随机数作为混淆，生成最终机器码。
    3. 将机器码发给软件开发者，开发者将机器码解密后，添加自己的标识符号并加密生成key，发给用户。
    4. 用户输入key，程序对比并保存。
    5. 用户下次打开软件时，重新开始步骤‘1’。
说明
    1. 加密：将序列号经过Des加密，再经过base64编码。
    2. 解密：将密码经过base64解码，再经过Des解密。
    3. 写文件：将二进制字符转为十六进制保存。
    4. 读文件：将十六进制转为二进制。
'''


## 运行环境

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)


## 使用说明

1. 创建 Github Repository 时选择这个仓库做模板
2. 在 [PyPI](https://pypi.org/) 上注册一个帐号，然后生成 API Token 后，把 Token 设置到 Github Repository -> Settings -> Secrets，即为配置文件 [`autorun.yml`](./.github/workflows/autorun.yml) 的环境变量 `pypi_password`，用于 Github Workflows 自动发版
3. 在 [src](./src) 目录中创建代码，源码各级目录必须要有 `__init__.py` 文件，不然发布时不会被打包
4. 修改 [setup.py](./setup.py) 中的 `FIXME` ，按实际修改发版信息


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
