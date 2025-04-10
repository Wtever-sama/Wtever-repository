def perform_integer_division():
    try:
        a, b = map(int, input().split())
        result = a/b
        print(result)
    
    except ZeroDivisionError as e:
        print(f"Error Code: {e}")
    except ValueError as e:
        print(f"Error Code: {str(e)}")
if __name__ == "__main__":
    perform_integer_division()