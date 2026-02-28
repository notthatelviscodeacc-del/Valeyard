```python
import sys

def print_file_line_by_line(filename):
    with open(filename, 'r') as file:
        for line in file:
            print(line, end='')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python solution.py <filename>")
        sys.exit(1)
    
    print_file_line_by_line(sys.argv[1])
```