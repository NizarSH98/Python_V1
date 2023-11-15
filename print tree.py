def print_tree(rows):
    for i in range(1, rows+1):
        print(' '*(rows-i) + '*'*(2*i-1))

# Take input from the user
num_rows = int(input("Enter the number of rows for the tree: "))

# Call the function to print the tree
print_tree(num_rows)
