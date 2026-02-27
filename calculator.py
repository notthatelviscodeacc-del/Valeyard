```python
def calculator():
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("Enter expression (e.g., 5 + 3): ").strip()

            if user_input.lower() == 'quit':
                print("Goodbye!")
                break

            parts = user_input.split()
            if len(parts) != 3:
                print("Invalid format. Please use: number operator number\n")
                continue

            num1, operator, num2 = parts
            num1 = float(num1)
            num2 = float(num2)

            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    print("Error: Division by zero\n")
                    continue
                result = num1 / num2
            else:
                print(f"Unknown operator '{operator}'. Use +, -, *, /\n")
                continue

            result = int(result) if result == int(result) else result
            print(f"Result: {result}\n")

        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    calculator()
```