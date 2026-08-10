import subprocess
'''
                       参数位置对照表
命令行	                    argv[0]	    argv[1]	       argv[2]
node script.js arg1	      node.exe路径	script.js	    arg1
node -e "code" arg1	      node.exe路径	arg1	      undefined
node -e "code" arg1 arg2  node.exe路径	arg1	        arg2
'''

# 测试代码
test_js = """
console.log('argv 长度:', process.argv.length);
console.log('argv[0]:', process.argv[0]);
console.log('argv[1]:', process.argv[1]);
console.log('argv[2]:', process.argv[2]);
console.log('argv[3]:', process.argv[3]);
console.log('完整 argv:', process.argv);
"""

result = subprocess.run(
    ['node', '-e', test_js, 'hello-world'],
    capture_output=True,
    text=True
)

print(result.stdout)


resul = subprocess.run(
    ['node', "C05_AES.js", 'hello-world'],
    capture_output=True,
    text=True
)

print(resul.stdout)



# 执行简单命令
# subprocess.run(['ls', '-l'])  # Linux/Mac
subprocess.run(['dir'], shell=True)  # Windows

# 执行 Python 脚本
# subprocess.run(['python', 'C05_AES.py'])

# 执行 Node.js
# subprocess.run(['node', 'C05_AES.js'])

# 执行系统命令
subprocess.run(['echo', 'Hello'], shell=True)

# 捕获标准输出
result = subprocess.run(['node', '-v'], capture_output=True, text=True)
print(f"Node.js 版本: {result.stdout}")

# 捕获错误输出
result = subprocess.run(['node', 'nonexistent.js'], capture_output=True, text=True)
print(f"错误: {result.stderr}")


# 通过标准输入传递数据
result = subprocess.run(
    ['python', '-c', 'import sys; print(sys.stdin.read())'],
    input="Hello from Python",
    capture_output=True,
    text=True
)
print(result.stdout)  # 输出: Hello from Python
