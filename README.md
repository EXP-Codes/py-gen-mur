# py-gen-mur

> python 机器码/用户码/注册码 生成器
<br/> python generate [m]achine_code [u]ser_code [r]egister_code

------

## 运行环境

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)


## 安装说明

执行脚本： 

```
python -m pip install --upgrade pip
python -m pip install py-gen-mur
```


## 使用场景说明

> 使用场景详见 [测试用例](./tests/test.py) 。


### 场景步骤一（管理员本地，可选）

因代码开源，不建议使用 `mur.crypt.Crypt()` 默认类。

建议使用此工具时，自定义指定 `mur.crypt.Crypt()` 构造函数的 `key` 和 `iv` 。

本代码中提供了 `mur.crypt.gen_des_key()` 和 `mur.crypt.gen_des_iv()` 的方法，但是生成后必须找地方另外存储这两个值，否则之前使用其生成的注册码无法再解密。

```python
from mur.crypt import *

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
from mur.user import *

u_machine_code = gen_machine_code(my_crypt)
```

> 实际使用时可复制 [`gen_machine_code.py`](./gen_machine_code.py) 到需要发布的程序，由用户执行生成【机器码】


### 场景步骤三（管理员本地）

1. 管理员解密用户提供的【加密机器码】文件
2. 同时为用户设置授权天数，生成【用户码】文件
3. 结合两者生成【注册码】文件
4. 把【用户码】文件和【注册码】文件提供给用户

```python
from mur.admin import *

a_machine_code = read_machine_code()
days = input('请输入授权天数：')    # 0 表示永久
a_user_code = gen_user_code(days, my_crypt)
a_register_code = gen_register_code(
    a_machine_code, a_user_code, my_crypt
)
```

> 实际使用时可在本仓库中执行 [`python gen_register_code.py`](./gen_register_code.py) 为用户生成【用户码】和【注册码】


### 场景步骤四（用户本地）

1. 用户运行应用主程序
2. 主程序读取【用户码】文件（或让用户输入用户码）
3. 主程序在用户本地重新生成【机器码】
4. 主程序利用【用户码】和【机器码】生成【注册码】
5. 主程序比对【生成的注册码】和【管理员提供的注册码】内容是否一致
6. 若一致，且授权未过期，程序运行；否则，程序终止

```python
from mur.user import *

u_user_code = read_user_code()
rst = verify_authorization(u_user_code, my_crypt)
if rst == True :
    app.run()
else :
    exit(1)
```


## 使用注意

凡是使用了此工具的程序，在发布该程序时，建议不要直接用 `Pyinstaller` 打包成 `*.pyc`，然后供用户使用，否则很容易被反编译破解。

建议先对源码做加密处理，再提供给用户使用。有两个方法，任选一个即可：

### Cython 编译为动态链接

1. 先使用 `Cython` 生成 `*.py` 的动态连接 `*.pyd` 文件
2. 再使用 `Pyinstaller` 打包，才供用户使用。

> 可参考文档《[Cython + Pyinstaller 防止反编译打包](https://www.jianshu.com/p/4a0be62ee3e2?share_token=64cb40ef-ad3b-4f2e-abd6-3bf95af210b6)》


### Pyinstaller 加密

1. 先用 pip 命令安装 `tinyaes` 和 `pycrypto` （需要提前安装 Microsoft Visual Studio 和设置环境变量 CL）
2. 使用 `Pyinstaller` 打包时增加 `--key ${password}` （此时编译的中间文件为 `*.pyc.encrypted`）。

可参考文档：

- 《[Pyinstaller 打包的 exe 之一键反编译 py 脚本与防反编译](https://blog.csdn.net/as604049322/article/details/119834495?share_token=a97db520-65be-4a54-b9cf-0a452163fb9d)》
- 《[谈谈 Pyinstaller 的编译和反编译，如何保护你的代码](https://chengxuyuanwenku.tumblr.com/post/611434747121549312/%E8%B0%88%E8%B0%88-pyinstaller-%E7%9A%84%E7%BC%96%E8%AF%91%E5%92%8C%E5%8F%8D%E7%BC%96%E8%AF%91%E5%A6%82%E4%BD%95%E4%BF%9D%E6%8A%A4%E4%BD%A0%E7%9A%84%E4%BB%A3%E7%A0%81)》
- 《[Microsoft Windows Python-3.6 PyCrypto installation error](https://stackoverflow.com/questions/41843266/microsoft-windows-python-3-6-pycrypto-installation-error/46921479#46921479)》


