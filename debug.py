from os import getenv

def debug_based_on_env():
  if getenv("PY_DEBUG") == "1":
    import multiprocessing
    if multiprocessing.current_process().pid > 1:
      import debugpy

      debugpy.listen(("0.0.0.0", 5678))
      print("Waiting for debugging client", flush=True)
      debugpy.wait_for_client()
