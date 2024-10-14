def twoSum(nums, target):
    for i in range(len(nums)):
        j = i + 1
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                print([i, j])
               

nums = [1, 3, 5]
target = 4

twoSum(nums, target)