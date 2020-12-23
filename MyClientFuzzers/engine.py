#!/usr/bin/python

class Engine(object):
  """
  Base interface for a grey box fuzzing engine.
  """

  @property
  def name(self):
    """Get the name of the engine."""
    raise NotImplementedError

  def prepare(self, input_path, output_path, target_path):
    """Prepare for a fuzzing session, by generating options. Returns a
    FuzzOptions object.

    Args:
      input_path: The main corpus directory.
      output_path: Path to the build directory.
      target_path: Path to the target.

    Returns:
      A FuzzOptions object.
    """
    raise NotImplementedError
    # 主要是这三个参数,但是不同的模糊测试框架的执行命令不同，所以在具体实现的时候可以写入不同的参数以适应
    # 具体的运行命令，但是prepare函数必须返回一个完整的可运行的命令！

  def fuzz(self, start_cmd, max_time):
    """Run a fuzz session.

    Args:
      start_cmd: The FuzzOptions object returned by prepare().
      max_time: Maximum allowed time for the fuzzing to run.

    Returns:
      A FuzzResult object.
    """
    raise NotImplementedError


  def reproduce(self, target_path, input_path, arguments, max_time):
    """Reproduce a crash given an input.

    Args:
      target_path: Path to the target.
      input_path: Path to the reproducer input.
      arguments: Additional arguments needed for reproduction.
      max_time: Maximum allowed time for the reproduction.

    Returns:
      A ReproduceResult.

    Raises:
      TimeoutError: If the reproduction exceeds max_time.
    """
    raise NotImplementedError