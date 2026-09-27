import time
Import("env")

def wait_for_port(source, target, env):
    print("\n[Delay Script] Waiting 2 seconds for macOS to release serial port...")
    time.sleep(2)

env.AddPostAction("upload", wait_for_port)