import subprocess
import sys


if __name__ == "__main__":
    process1 = subprocess.Popen([sys.executable, "images/images.py"])
    process2 = subprocess.Popen([sys.executable, "getContainers/video.py"])

    process1.wait()
    process2.wait()

    print("Ambos os módulos foram encerrados.")
