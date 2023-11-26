def calculate_mean(numbers):
    total = 0
    count = 0
    for num in numbers:
        total += num
        count += 1
    if count == 0:
        return 0
    else:
        return total / count

values = [1, 2, 3, 4, 5]
mean_value = calculate_mean(values)
print("The mean value is:", mean_value)
