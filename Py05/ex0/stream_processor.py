from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):
    """Abstract base class defining a unified interface for all data
    processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process the input data and return a result. Must be implemented by
          subclasses."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate the input data. Must return True if valid, False
        otherwise."""
        pass

    @abstractmethod
    def format_output(self, result: Any) -> str:
        """Format the processed result into a human-readable string."""
        pass


class NumericProcessor(DataProcessor):
    """Processor for numeric data:
    validates lists of integers, converts to strings,
    calculates sum and average, and formats output."""

    def process(self, data: List[int]) -> List[str]:
        """Convert a list of integers to a list of strings.
          Returns 'Error' if processing fails.
        """
        try:
            return [str(value) for value in data]
        except Exception:
            return "Error"

    def validate(self, data: Any) -> bool:
        """Check if the input is a list of integers.
        """
        return isinstance(data, list) and all(isinstance(i, int) for i in data)

    def format_output(self, result: List[str]) -> str:
        """Return a formatted string showing count, sum,
        and average of the numeric list.
        """
        len_lst = len(result)
        sum_lst = sum([int(i) for i in result])
        avg = sum_lst / len_lst
        return f"Processed {len_lst} numeric values, sum={sum_lst}, avg={avg}"


class TextProcessor(DataProcessor):
    """Processor for text data: strips whitespace, validates string input,
    counts characters and words, and formats output."""

    def process(self, data: Any) -> str:
        """Strip leading/trailing whitespace from the input text.
        Returns 'Error' if invalid."""
        try:
            return data.strip()
        except Exception:
            return "Error"

    def validate(self, data: str) -> bool:
        """Check if the input is a string."""
        return isinstance(data, str)

    def format_output(self, result: str) -> str:
        """Return a formatted string showing character and word counts."""
        len_str = len(result)
        words = len(result.split(" "))
        return f"Processed text: {len_str} characters, {words} words"


class LogProcessor(DataProcessor):
    """Processor for log messages: generates status or error messages,
    validates log input, and formats output based on severity."""

    def process(self, data: str) -> str:
        """
        Return a log message. If input is 'Error',
        returns a simulated error log; otherwise,
        returns a normal system message.
        """
        if data == 'Error':
            return "\"ERROR: Connection timeout\""
        else:
            return "\"System ready\""

    def validate(self, data: Any) -> bool:
        """
        Check if the input is a non-empty string.
        """
        return isinstance(data, str) and len(data) > 0

    def format_output(self, result: str) -> str:
        """
        Return a formatted log message based on severity level.
        """
        if result == "\"ERROR: Connection timeout\"":
            return "[ALERT] ERROR level detected: Connection timeout"
        else:
            return "[INFO] INFO level detected: System ready"


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

    print("Initializing Numeric Processor...")
    num = NumericProcessor()
    nums = num.process([1, 2, 3, 4, 5])
    print(f"Processing data: {nums}")
    if num.validate([1, 2, 3, 4, 5]):
        print("Validation: Numeric data verified")
    else:
        print("Validation: Numeric data not verified :(")

    print(f"Output: {num.format_output(nums)}\n")

    print("Initializing Text Processor...")
    txt = TextProcessor()
    txt_str = "Hello Nexus World"
    print(f"Processing data: {txt.process(txt_str)}")
    if txt.validate(txt_str):
        print("Validation: Text data verified")
    else:
        print("Validation: Text data not verified :(")

    print(f"Output: Processed text: {txt.format_output(txt_str)}\n")

    print("Initializing Log Processor...")
    log = LogProcessor()
    log_error = txt.process(123)
    error = log.process(log_error)
    print(f"rocessing data: {log.process(log_error)}")
    if log.validate(error):
        print("Validation: Log entry verified")
    else:
        print("Validation: Log entry not verified :(")

    print(f"Output: {log.format_output(error)}\n")

    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    print(f"Result 1: {num.format_output([1, 2, 3])}")
    print(f"Result 2: {txt.format_output('hello bro how are u')}")
    print(f"Result 3: {log.format_output('valid')}\n")
    print("Foundation systems online. Nexus ready for advanced streams.")
