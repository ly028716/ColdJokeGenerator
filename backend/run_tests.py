"""
测试运行脚本
"""
import subprocess
import sys
import os

def run_tests():
    """运行测试"""
    print("开始运行测试...")
    
    # 设置环境变量
    os.environ["TESTING"] = "1"
    
    # 运行pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term-missing"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("测试运行完成！")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"测试运行失败: {e}")
        return e.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)