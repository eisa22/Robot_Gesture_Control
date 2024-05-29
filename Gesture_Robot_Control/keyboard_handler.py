import keyboard

# Global flag to control the printing of "Test"
print_test = True  # Start with printing enabled

def on_r_key():
    global print_test
    print_test = not print_test  # Toggle the flag when 'R' is pressed

if __name__ == "__main__":
    keyboard.add_hotkey('R', on_r_key)

    while True:
        if print_test:
            print("Test")
        else:
            print("Test over")  # Exit the loop if print_test is False
