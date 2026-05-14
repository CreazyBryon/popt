import sys
import pop_player

if __name__ == '__main__':
    print('hello world')
    if len(sys.argv) <= 1:
        print('No account numbers provided. Please provide account numbers as command-line arguments.')
        sys.exit(1)

    input_argument = sys.argv[1]
    numbs = [int(x) for x in str(input_argument) if x.isdigit()]
    print(f"Playing for account numbers: {numbs}")
    pop_player.st2(numbs)
    print('All done.')