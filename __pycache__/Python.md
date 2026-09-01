[TOC]



# 数据结构

## 栈

python可以使用列表类型实现栈；

```python
stack = []
```

**栈空判断？**

```python
if stack:
	# 语句
```

**进栈：**

```python
stack.append("元素")
```

**出栈：**

```python
stack.pop()
```

### 符号匹配问题

#### [1047. 删除字符串中的所有相邻重复项](https://leetcode-cn.com/problems/remove-all-adjacent-duplicates-in-string/) （消消乐游戏）

```python
class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack = []
        for ch in s:
            if stack and stack[-1] == ch:
                stack.pop()
            else:
                stack.append(ch)
        return ''.join(stack)
```

#### [1544. 整理字符串](https://leetcode-cn.com/problems/make-the-string-great/)

```python
class Solution:
    def makeGood(self, s: str) -> str:
        stack = []
        for ch in s:
            if stack and stack[-1] != ch and ch.lower() == stack[-1].lower():
                stack.pop()
            else:
                stack.append(ch)
        return ''.join(stack)
```

#### [20. 有效的括号](https://leetcode-cn.com/problems/valid-parentheses/)

**注意点：**

​	当栈空时，左括号才入栈，右括号时候直接返回false；

```python
class Solution:
    def isValid(self, s: str) -> bool:
        match_dict = {'(': ')', '{': '}', '[': ']'}
        stack = list()
        for ch in s:
            if ch in "({[":
                stack.append(ch)
            elif ch in ")}]":
                if stack and ch == match_dict.get(stack[-1]):
                    stack.pop()
                else:
                    return False
        return not stack
```

#### [1190. 反转每对括号间的子串](https://leetcode.cn/problems/reverse-substrings-between-each-pair-of-parentheses/)

```python
class Solution:
    def reverseParentheses(self, s: str) -> str:
        stack = list()
        for ch in s:
            if ch != ')':
                stack.append(ch)
            else:
                tmp = list()
                while stack and stack[-1] != "(":
                    tmp.append(stack.pop())
                # if stack and stack[-1] == "(":
                stack.pop()
                stack.extend(tmp)
        return ''.join(stack)
```

### 计算器问题

#### [227. 基本计算器 II](https://leetcode-cn.com/problems/basic-calculator-ii/)

#### [150. 逆波兰表达式求值](https://leetcode.cn/problems/evaluate-reverse-polish-notation/)

```C
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = list()
        for item in tokens:
            if item not in {"+", "-", "*", "/"}:
                stack.append(item)
            else:
                first_num = stack.pop()
                second_num = stack.pop()
                stack.append(int(eval(f'{second_num} {item} {first_num}')))
        return int(stack.pop())
```

### 辅助栈

#### [155. 最小栈](https://leetcode.cn/problems/min-stack/)

```python
class MinStack:
    def __init__(self):
        self.stack = list()
        self.min_stack = [math.inf]

    def push(self, val: int) -> None:
        self.stack.append(val)
        self.min_stack.append(min(val, self.min_stack[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

#### [面试题 03.05. 栈排序](https://leetcode.cn/problems/sort-of-stacks-lcci/)

```python
class SortedStack:

    def __init__(self):
        self.stack = list()

    def push(self, val: int) -> None:
        temp_stack = list() # 辅助临时栈
        while self.stack and self.stack[-1] < val:
            temp_stack.append(self.stack.pop())
        self.stack.append(val)
        while temp_stack:
            self.stack.append(temp_stack.pop())

    def pop(self) -> None:
        if self.stack:
            self.stack.pop()

    def peek(self) -> int:
        if not self.stack:
            return -1
        return self.stack[-1]

    def isEmpty(self) -> bool:
        return not self.stack
```



### 单调栈 -- 下一个最值问题

单调栈用途不太⼴泛， 只处理⼀种典型的问题， 叫做 **Next Greater Element**。    

https://lucifer.ren/blog/2020/11/03/monotone-stack/

**什么是单调栈？**

​	单调栈是一种特殊的栈，只是限制要比普通的栈更严格而已了，单调栈要求栈中的元素是单调递增或者单调递减的。 

​	递增递减是从栈顶向栈底顺序定义；

**单调栈解决什么问题？ -- 下一个最值问题**

​	**通常是一维数组，要寻找任一个元素的右边或者左边第一个比自己大或者小的元素的位置，此时我们就要想到可以用单调栈了**。

#### 单调栈模板

```c
vector<int> dailyTemperatures(vector<int> &T)
{
    vector<int> ans(T.size());
    stack<int> s; // 这⾥放元素索引， ⽽不是元素
    for (int i = T.size() - 1; i >= 0; i--) { // 倒着入栈
        while (!s.empty() && T[s.top()] <= T[i]) {
            s.pop();
        }
        a ns[i] = s.empty() ? 0 : s.top() - i; // 得到索引间距
        s.push(i);                               // 加⼊索引， ⽽不是元素
    }
    return ans;
}
```

#### [739. 每日温度](https://leetcode-cn.com/problems/daily-temperatures/)

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = list()
        res = [0] * len(temperatures)
        for i in range(len(temperatures) - 1, -1, -1):
            while stack and temperatures[i] >= temperatures[stack[-1]]:
                stack.pop()
            if stack:
                res[i] = stack[-1] - i
            stack.append(i)
        return res

```

#### [496. 下一个更大元素 I](https://leetcode-cn.com/problems/next-greater-element-i/)

```c
/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* nextGreaterElement(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize){
    *returnSize = nums1Size;

    // 初始化栈
    int *stack = (int *)calloc(nums2Size, sizeof(int));
    int top = -1;

    // 返回空间
    int *res = (int *)malloc(nums1Size * sizeof(int));
    memset(res, -1, nums1Size);

    for (int i = nums2Size - 1; i >= 0; i--) {
        while(top != -1 && nums2[i] >= nums2[stack[top]]) {
            top--; //出栈
        }

        for (int j = 0; j < nums1Size; j++) {
            if (nums2[i] == nums1[j]) { // 存在
                res[j] = top == -1 ? -1 : nums2[stack[top]];
                break;
            }
        }
        
        stack[++top] = i; // 下标入栈
    }
    return res;
}
```



#### [503. 下一个更大元素 II](https://leetcode-cn.com/problems/next-greater-element-ii/) (循环数组)

用%模拟两倍数组

```c
/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* nextGreaterElements(int* nums, int numsSize, int* returnSize){
    *returnSize = numsSize;

    // 初始化栈
    int *stack = (int *)calloc(numsSize, sizeof(int));
    int top = -1;

    // 返回数组
    int *res = (int *)malloc(numsSize * sizeof(int));
    memset(res, -1, numsSize);

    for (int i = 2 * numsSize - 1; i >= 0; i--) {
        while(top != -1 && nums[stack[top]] <= nums[i % numsSize]) {
            top--;
        }
        res[i % numsSize] = top == -1 ? -1 : nums[stack[top]];

        // 索引入栈
        top++;
        stack[top] = i % numsSize;
    }
    return res;
}
```

#### [84. 柱状图中最大的矩形](https://leetcode-cn.com/problems/largest-rectangle-in-histogram/)

九阴真经第一式代表题目；

## 队列

**定义：**队尾插入，队首出；

**性质：**先进先出；FIFO结构；

队列在bfs算法中要用；

```c
#define QUE_SIZE 100
void PushQue(int *que, int *end, int val)
{
    que[*end] = val;
    *end = (*end + 1) % QUE_SIZE;
}
int PopQue(int *que, int *front)
{
    int val = que[*front];
    *front = (*front + 1) % QUE_SIZE;
    return val;
}
int main()
{
    int que[QUE_SIZE] = {0};
    int front = 0;
    int end = 0;
    PushQue(que, &end, 1);
    int val = PopQue(que, &front);
}
```

### 单调队列

​	单调队列可以解决一些滑动窗口问题。

​	[239. 滑动窗口最大值](https://leetcode-cn.com/problems/sliding-window-maximum/)

### 循环队列

数组模拟，循环队列的实现：

```c
	#define MAX_QUEUE_NUM
	typedef struct StQueue {
	    int data[MAX_QUEUE_NUM];
	    int front;
	    int rear;
	} Queue;
	 
	int QueueIsEmpty (Queue *q)
	{
	    if (q->front == q->rear) {
	        printf("queue empty\n");
	        return -1;
	    }
	    return 0;
	}
	 
	int QueueSize(Queue *q)
	{
	    return (q->rear + MAX_QUEUE_NUM - q->front) % MAX_QUEUE_NUM;
	}
	 
	int QueueIsFull(Queue *q)
	{
	    if ((q->rear + 1) % MAX_QUEUE_NUM == q->front) {
	        printf("queue full\n");
	        return -1;
	    }
	}
	int QueueAdd (Queue *q, int val)
	{
	    if ((q->rear + 1) % MAX_QUEUE_NUM == q->front) {
	        printf("queue full\n");
	        return -1;
	    }
	 
	    q->data[q->rear] = val;
	    q->rear = (q->rear + 1) % MAX_QUEUE_NUM;
	    return 0;
	}
	 
	int QueueRemove (Queue *q, int *val)
	{
	    if ((q->rear  == q->front) {
	        printf("queue empty\n");
	        return -1;
	    }
	 
	    *val = q->front[q->rear];
	    q->front = (q->front + 1) % MAX_QUEUE_NUM;
	    return 0;
	}
```

#### [649. Dota2 参议院](https://leetcode-cn.com/problems/dota2-senate/)

### 优先级队列

​	**什么是优先队列？**首先是一个队列，入队时和普通队列一样，但是出队时先**自动排序**再出队。

​	优先队列可以实现大小堆。

## 哈希表

#### [1797. 设计一个验证系统](https://leetcode-cn.com/problems/design-authentication-manager/)

#### [1418. 点菜展示表](https://leetcode-cn.com/problems/display-table-of-food-orders-in-a-restaurant/)

#### [1357. 每隔 n 个顾客打折](https://leetcode-cn.com/problems/apply-discount-every-n-orders/)

## 二叉树

![二叉树大纲](https://img-blog.csdnimg.cn/20210219190809451.png) 

### 二叉树的遍历

​	二叉树的深度遍历见DFS章节;

​	二叉树的层序遍历见BFS章节;

### 二叉树属性

#### [226. 翻转二叉树](https://leetcode-cn.com/problems/invert-binary-tree/)

```c++
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if (root == NULL) return root;
        swap(root->left, root->right);  // 中
        invertTree(root->left);         // 左
        invertTree(root->right);        // 右
        return root;
    }
};
```

#### [104. 二叉树的最大深度](https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/)

可以使用BFS，每一层加1；

```python
from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        que = deque([root])
        count = 0
        while que:
            count += 1
            size = len(que)
            for _ in range(size):
                node = que.popleft()
                if node.left:
                    que.append(node.left)
                if node.right:
                    que.append(node.right)
        return count
```



#### [111. 二叉树的最小深度](https://leetcode-cn.com/problems/minimum-depth-of-binary-tree/)

```python
from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        que = deque([root])
        count = 0
        while que:
            count += 1
            size = len(que)
            for _ in range(size):
                node = que.popleft()
                if node.left is None and node.right is None:  # 记录第一次叶子节点的层数
                    return count
                if node.left:
                    que.append(node.left)
                if node.right:
                    que.append(node.right)
        return count
```

# 算法篇

## 双指针 - 单循环

### 左右双指针 -- 对向移动

#### 模板

**Python左右指针模板：**

```c
def fun(s):
	left = 0
    right = len(s) - 1
    while left < right:
		// 动作
        // 调整left    left++
        // 调整right   right--
```

==对向移动！二分属于左右指针；==，==数组使用双指针，需要排序；==

#### 典型题目

##### [344. 反转字符串](https://leetcode-cn.com/problems/reverse-string/)

左右指针法：

```python
class Solution:
    def reverseString(self, s: List[str]) -> None:
        left = 0
        right = len(s) - 1
        while left <= right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1
```

**反转字符串库函数法：**

```python
class Solution:
    def reverseString(self, s: List[str]) -> None:
        s[:] = s[::-1]
```

- `s[::-1]`表示反转s中的元素
- `s[:]`表示数组中所有子模块
- `s[:]=s[::-1]`表示将原数组反转后赋值给s中每一个对应的位置
- `s=s[::-1]`表示将s反转后赋值给新的对象s（`可以通过id函数查看内存地址`），与题意`原地修改`不符。

##### [977. 有序数组的平方](https://leetcode.cn/problems/squares-of-a-sorted-array/)

```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        ans = []
        left = 0
        right = len(nums) - 1
        while left <= right:
            left_pow = nums[left] ** 2
            right_pow = nums[right] ** 2
            if left_pow > right_pow:
                ans.append(left_pow)
                left += 1
            else:
                ans.append(right_pow)
                right -= 1
        ans.reverse()
        return ans
```

##### [11. 盛最多水的容器](https://leetcode.cn/problems/container-with-most-water/)(中等)

若向内**移动短板** ，水槽的短板` min(h[i], h[j]) `可能变大，因此下个水槽的面积可能增大 。

若向内**移动长板** ，水槽的短板 `min(h[i], h[j]) `不变或变小，因此下个水槽的面积一定变小 。

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1

        max_area = 0
        while left < right:
            width = right - left
            h = min(height[left], height[right])
            area = width * h
            max_area = max(max_area, area)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area
```

##### [9. 回文数](https://leetcode.cn/problems/palindrome-number/)

可以用左右指针；

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        elif x == 0:
            return True
        s = str(x)
        return s == s[::-1]
```

##### [2105. 给植物浇水 II](https://leetcode-cn.com/problems/watering-plants-ii/)

```python
from typing import List


class Solution:
    def __init__(self):
        self.water_a = 0
        self.times_a = 0
        self.water_b = 0
        self.times_b = 0
        self.left = 0
        self.right = 0

    def do_a(self, plants: List[int], capacity_a: int, capacity_b: int):
        if self.water_a >= plants[self.left]:
            self.water_a -= plants[self.left]
        else:
            self.times_a += 1
            self.water_a = capacity_a - plants[self.left]

    def do_b(self, plants: List[int], capacity_a: int, capacity_b: int):
        if self.water_b >= plants[self.right]:
            self.water_b -= plants[self.right]
        else:
            self.times_b += 1
            self.water_b = capacity_b - plants[self.right]

    def minimumRefill(self, plants: List[int], capacity_a: int, capacity_b: int) -> int:
        self.left = 0
        self.right = len(plants) - 1
        self.water_a = capacity_a
        self.water_b = capacity_b
        while self.left < self.right:
            self.do_a(plants, capacity_a, capacity_b)
            self.do_b(plants, capacity_a, capacity_b)
            self.left += 1
            self.right -= 1
        if self.left == self.right:
            if self.water_a >= self.water_b:
                self.do_a(plants, capacity_a, capacity_b)
            else:
                self.do_b(plants, capacity_a, capacity_b)
        return self.times_a + self.times_b
```

### 快慢双指针 -- 同向移动

#### 模板

```python
def fun(nums):
    left = 0
    right = 0
    while right < len(nums):
        # 处理 left移动
        right += 1
```

#### **典型题目**

##### [27. 移除元素](https://leetcode-cn.com/problems/remove-element/)

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        slow = 0
        for num in nums: # 快指针带着慢指针跑
            if num != val:
                nums[slow] = num
                slow += 1
        return slow

```

python库函数法：

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        while val in nums:
            nums.remove(val)
        return len(nums)
```

### 滑动窗口和双指针区别

https://leetcode-cn.com/problems/get-equal-substrings-within-budget/solution/jie-zhe-ge-wen-ti-ke-pu-yi-xia-hua-dong-6128z/

目前将计算过程仅与「**两端点**」相关的称为「**双指针**」；

将计算过程与「**两端点表示的区间**」相关的称为「**滑动窗口**」。 

**滑动窗口：**

- 滑动窗口一定是**同向移动**；
- 滑动窗口不是方法，就是问题本身；

**双指针：**

- 双指针可以**同向移动、可以双向移动**；
- 双指针是一种方法，而不是问题本身；

## 滑动窗口

滑动窗口算法属于双指针高级用法；

一般用来求解**连续子数组**或**连续子串**问题。

滑动窗口可以将暴力法的`O(n^2)`降低`为O(n)`。

### 模板 -- 双while循环

```c
left = 0
right = 0
while right < len(s):
    window.add(s[right])  # 扩张窗口值
    while valid: # 窗口值判断条件
        window.remove(s[left]) # 缩小窗口值
        left += 1
   	# 更新最大值
    right += 1
```

难度在于如何处理这个valid条件。

### 典型题目

#### LeetCode  [209. 长度最小的子数组](https://leetcode-cn.com/problems/minimum-size-subarray-sum/)

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        right = 0
        window_num = 0
        res = math.inf
        while right < len(nums):
            window_num += nums[right]
            while window_num >= target:
                res = min(res, right - left + 1) # 获取窗口属性
                window_num -= nums[left]
                left += 1
            right += 1
        return 0 if res == math.inf else res
```

### 练习题

注意事项：一定要在满足题目要求的地方进行更新，不一定在伸缩窗口内。

#### [1208. 尽可能使字符串相等](https://leetcode-cn.com/problems/get-equal-substrings-within-budget/)

```python
class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        left = 0
        right = 0
        window_nums = 0
        size = 0
        while right < len(s):
            window_nums += abs(ord(s[right]) - ord(t[right]))
            while window_nums > maxCost:
                window_nums -= abs(ord(s[left]) - ord(t[left]))
                left += 1
            size = max(size, right - left + 1)  # 更新窗口属性
            right += 1
        return size
```

#### [1004. 最大连续1的个数 III](https://leetcode-cn.com/problems/max-consecutive-ones-iii/)

```python
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        right = 0
        window_nums = 0
        max_nums = 0
        while right < len(nums):
            if nums[right] == 0:
                window_nums += 1  # 扩大窗口值
            while window_nums > k:
                if nums[left] == 0:
                    window_nums -= 1  # 缩小窗口值
                left += 1
            max_nums = max(max_nums, right - left + 1)
            right += 1
        return max_nums
```

#### [76. 最小覆盖子串](https://leetcode-cn.com/problems/minimum-window-substring/)

给定一个字符串S和子字符串T，请在S中找出包含T所有字母的最小子串。



#### LeetCode  [3. 无重复字符的最长子串](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)

```python
from collections import defaultdict

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        right = 0
        cnt = defaultdict(int)
        max_len = 0
        while right < len(s):
            cnt[s[right]] += 1
            while cnt[s[right]] > 1:
                cnt[s[left]] -= 1
                left += 1
            max_len = max(max_len, right - left + 1)
            right += 1
        return max_len
```

#### [1695. 删除子数组的最大得分](https://leetcode-cn.com/problems/maximum-erasure-value/)

```c
// 求累加和最大的无重复元素的连续子数组
// 正数才能用滑动窗口
class Solution:
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        left = 0
        right = 0
        cnt = defaultdict(int)
        max_len = 0
        while right < len(nums):
            cnt[nums[right]] += 1
            while cnt[nums[right]] > 1:
                cnt[nums[left]] -= 1
                left += 1
            max_len = max(max_len, sum(nums[left:right + 1]))
            right += 1
        return max_len
```

#### [1052. 爱生气的书店老板](https://leetcode-cn.com/problems/grumpy-bookstore-owner/)

#### [2024. 考试的最大困扰度](https://leetcode-cn.com/problems/maximize-the-confusion-of-an-exam/)

#### [1658. 将 x 减到 0 的最小操作数](https://leetcode-cn.com/problems/minimum-operations-to-reduce-x-to-zero/)

#### [1839. 所有元音按顺序排布的最长子字符串](https://leetcode-cn.com/problems/longest-substring-of-all-vowels-in-order/)

#### [1838. 最高频元素的频数](https://leetcode-cn.com/problems/frequency-of-the-most-frequent-element/)

#### [904. 水果成篮](https://leetcode-cn.com/problems/fruit-into-baskets/)

### 固定大小窗口

#### [1423. 可获得的最大点数](https://leetcode-cn.com/problems/maximum-points-you-can-obtain-from-cards/)

转化为固定窗口问题，找最小连续子数组；

```python
class Solution:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        # 滑动窗口大小为 n-k
        windowSize = n - k
        # 选前 n-k 个作为初始值
        s = sum(cardPoints[:windowSize])
        minSum = s
        for i in range(windowSize, n):
            # 滑动窗口每向右移动一格，增加从右侧进入窗口的元素值，并减少从左侧离开窗口的元素值
            s += cardPoints[i] - cardPoints[i - windowSize]
            minSum = min(minSum, s)
        return sum(cardPoints) - minSum
```

## 二分法

**考试问题具有有序或者单调性，又需要降低时间复杂度，一般可以采用二分法（logN）。**

**二分法概念：**该算法的基本思想是将所要査找的序列的中间位置的数据与所要査找的元素进行比较，如果相等，则表示査找成功，否则将以该位置为基准将所要査找的序列分为左右两部分。 

**使用前提：**首先得**排序**；

### 恰好搜索

#### 模板

​	这种情况只要找到即可，不需要边界位置，是二分查找的最基本操作。

##### 左闭右闭 (优选)

​	左闭右开：**[left, right]**

- `right = len - 1`;

- `while left <= right`；因为==left == right有意义==，所以用<=

- `right = mid - 1;` 

  **左闭右闭模板：**

  ```c
  int BinarySearch(int nums[], int len, int target)
  {
      int left = 0;
      int right = len - 1;
      while (left <= right) {
          int mid = left + (right - left) / 2; // 防止溢出
          if (nums[mid] == target) {
              return mid; // 找到即停止
          } else if (nums[mid] < target) {
              left = mid + 1;
          } else if (nums[mid] > target) {
              right = mid - 1;
          }
      }
      return -1;
  }
  ```

#### 典型题目

##### [704. 二分查找](https://leetcode-cn.com/problems/binary-search/)

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (right + left) // 2
            if nums[mid] > target:
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                return mid
        return -1
```

##### [74. 搜索二维矩阵](https://leetcode-cn.com/problems/search-a-2d-matrix/)

```c
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        row = len(matrix)
        col = len(matrix[0])
        left = 0
        right = row * col - 1
        while left <= right:
            mid = (left + right) // 2
            mid_value = matrix[mid // col][mid % col]  # 关键步骤
            if mid_value > target:
                right = mid - 1
            elif mid_value < target:
                left = mid + 1
            else:
                return True
        return False
```

##### [240. 搜索二维矩阵 II](https://leetcode-cn.com/problems/search-a-2d-matrix-ii/)

对每一行都使用一次二分查找，判断target 是否在该行中 。

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for col in matrix:
            index = bisect.bisect_left(col, target)
            if index < len(col) and col[index] == target: # bisect_left可能会越界
                return True
        return False
```

**Z字搜索法：**

从矩阵右上角（0， n - 1)开始搜索；

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        row = len(matrix)
        col = len(matrix[0])
        x = 0
        y = col - 1
        while x < row and y >= 0:
            if matrix[x][y] < target:
                x += 1
            elif matrix[x][y] > target:
                y -= 1
            else:
                return True
        return False
```

### 寻找左边界

#### 模板

左边界概念：

​	1、如果target存在，就是最左边位置索引；（如4 4 4 4 4中最左边的4）

​	2、如果target不存在，就是第一个大于target的元素下标；

找左边界时注意事项：

- 调整 `if (nums[mid] == target)` 条件；==当满足相等时不要停止，继续向左区间寻找。==
- 调整函数最终返回值: `return left ;`

##### 左闭右闭（优选）

```c
def BinarySearch(nums, target):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        else:
            right = mid - 1
    return left
```

python库函数：

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        return bisect.bisect_left(nums, target)
```

### 寻找右边界

#### 模板

右边界概念：

​	1、如果target存在，就是最右边位置索引；（如44444中最右边的4）

​	2、如果target不存在，就是第一个小于target的元素下标；

**寻找右边界时代码模板如下：**

- 调整 `if (nums[mid] == target)` 条件；当满足相等时不要停止，==继续向右区间寻找==。 
- 调整函数最终返回值: `return right;`

##### 左闭右闭（优选）

```python
def BinarySearch(nums, target):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    return right
```

### 寻找左边界典型题

#### [35. 搜索插入位置](https://leetcode-cn.com/problems/search-insert-position/)

```c
// 寻找左边界
int searchInsert(int* nums, int numsSize, int target){
    int left = 0;
    int right = numsSize - 1;
    while (left <= right) { // 左闭右闭
        int mid = left + (right - left) / 2;
        if (nums[mid] > target) {
            right = mid - 1;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else if (nums[mid] == target) {
            right = mid - 1;
        }
    } 
    return left;
}
```

#### [69. x 的平方根 ](https://leetcode-cn.com/problems/sqrtx/)

```c
int mySqrt(int x)
{
    int left = 0;
    int right = x;
    while (left <= right) { // 左闭右闭
        long long mid = left + (right - left) / 2;
        long long temp = mid * mid; // 平方
        if (temp > x) {
            right = mid - 1;
        } else if (temp < x) {
            left = mid + 1;
        } else if (temp == x) {
            return mid;
        }
    }
    return left - 1;
}
```

#### [278. 第一个错误的版本](https://leetcode-cn.com/problems/first-bad-version/)

#### [875. 爱吃香蕉的珂珂](https://leetcode-cn.com/problems/koko-eating-bananas/)

有一定的贪心思想，**target有一定的转化。**可信考试考过类似的。

```c
// 求数组最大值
int Max(int *piles, int pilesSize)
{
    int max = 0;
    for (int i = 0; i < pilesSize; i++) {
        if (piles[i] > max) {
            max = piles[i];
        }
    }
    return max;
}

int GetTime(int *piles, int pilesSize, int k)
{
    int time = 0;
    for (int i = 0; i < pilesSize; i++) {
        time += (piles[i] - 1) / k + 1; // 关键
    }
    return time;
}

int minEatingSpeed(int *piles, int pilesSize, int h)
{
    int left = 1;
    int right = Max(piles, pilesSize) - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (GetTime(piles, pilesSize, mid) == h) { // 寻找左边界
            right = mid - 1;
        } else if (GetTime(piles, pilesSize, mid) > h) {
            left = mid + 1;
        } else if (GetTime(piles, pilesSize, mid) < h) {
            right = mid - 1;
        }
    }
    return left;
}
```

#### [1011. 在 D 天内送达包裹的能力](https://leetcode-cn.com/problems/capacity-to-ship-packages-within-d-days/)

```c
int GetDay(int* weights, int weightsSize, int mid)
{
    int total = 0;
    int need = 1;
    for (int i = 0; i < weightsSize; i++) {
        if (total + weights[i] > mid) {
            need++;
            total = 0;
        }
        total += weights[i];
    }
    return need;
}
int shipWithinDays(int* weights, int weightsSize, int days){
    int sum = 0;
    int max = 0;
    for (int i = 0; i < weightsSize; i++) {
        sum += weights[i];
        max = fmax(max, weights[i]);
    }

    // 以下是左边界模板
    int left = max;
    int right = sum;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (GetDay(weights, weightsSize, mid) > days) {
            left = mid + 1;
        } else if (GetDay(weights, weightsSize, mid) < days) {
            right = mid - 1;
        } else if (GetDay(weights, weightsSize, mid) == days) {
            right = mid - 1;
        }
    }
    return left;
}
```

#### [2187. 完成旅途的最少时间](https://leetcode-cn.com/problems/minimum-time-to-complete-trips/)

#### [1760. 袋子里最少数目的球](https://leetcode-cn.com/problems/minimum-limit-of-balls-in-a-bag/)

#### [378. 有序矩阵中第 K 小的元素](https://leetcode-cn.com/problems/kth-smallest-element-in-a-sorted-matrix/)

#### [1552. 两球之间的磁力](https://leetcode-cn.com/problems/magnetic-force-between-two-balls/)

#### [1482. 制作 m 束花所需的最少天数](https://leetcode-cn.com/problems/minimum-number-of-days-to-make-m-bouquets/)

#### [1631. 最小体力消耗路径](https://leetcode-cn.com/problems/path-with-minimum-effort/)

#### 寻找左右边界 leetCode34题

http://3ms.huawei.com/km/blogs/details/10635119

### 可信考试

可信考试考过二分，参考http://3ms.huawei.com/km/groups/3803117/blogs/details/10629165?l=zh-cn

**什么时候使用二分：**

1）序列是有序的、且数据量巨大，需要对处理的时间复杂度进行优化；

2）给出一个要求达到的目标值，求出某个自变量能满足目标的最小/最大值，该自变量和目标之间存在单调关系（单调增或单调减）。注：大部分使用二分的场景存在单调关系，但不一定是必须的。

## 前缀和

 如何区分是用前缀和还是用滑动窗口，如果有负数就用前缀和。

如果只使用前缀和, 时间复杂度还是太高了 ，使用哈希表优化。

### 定义

**前缀和数组是数组自身的固有性质，数组的每一个元素都有对应的前缀和值。**

​	前缀和其实就是高中数学数列前n项和。

​	前缀和 = 从**0到自身**的所有元素求和。

**前缀和数学表达式：**

​	针对数组     `arr[n]`,定义一个前缀和数组`PreSum[n]`，满足:

​			`PreSum[i] = a[0] + a[1] + a[2] + ...... a[i]`

**如何快速求i到j之间元素的和？（包含i和j所在元素）**

​	`preSum[j] - preSum[i - 1] `

### python前缀和模板

**实际前缀和下标从1开始；**

计算求前缀和数组模板如下：

```python
presum = [0] # 0作为辅助
for num in nums: # nums是输入数组
	presum.append(presum[-1] + num)
```

例题：

```python
nums = [1,2,3]
presum = [0]
for num in nums:
	presum.append(presum[-1] + num)
print(presum) # [0, 1, 3, 6]
```

### 二维前缀和

sum[i][j存储左上角坐标为(0, 0)，右下角坐标为(i, j)的子矩阵的和。

### 典型题目

#### [560. 和为 K 的子数组](https://leetcode-cn.com/problems/subarray-sum-equals-k/)

如果使用前缀和，再使用暴力法时间复杂度达到n^2，超出时间限制；

```c

```

即使使用了前缀和，并没有提高运行速度。

因为查找子数组和的时候用了两层for循环查找。

**使用哈希表优化：**

#### [523. 连续的子数组和](https://leetcode-cn.com/problems/continuous-subarray-sum/)

#### [1915. 最美子字符串的数目](https://leetcode-cn.com/problems/number-of-wonderful-substrings/)

#### [1744. 你能在你最喜欢的那天吃到你最喜欢的糖果吗？](https://leetcode-cn.com/problems/can-you-eat-your-favorite-candy-on-your-favorite-day/)

### 练习题目

https://leetcode-cn.com/problems/subarray-sum-equals-k/solution/de-liao-yi-wen-jiang-qian-zhui-he-an-pai-yhyf/

## BFS 广度优先搜索

BFS参考https://labuladong.gitee.io/algo/1/6/

BFS 的核心思想应该不难理解的，就是把一些问题抽象成图，从一个点开始，向四周开始扩散。一般来说，我们写 BFS 算法都是用**队列**这种数据结构，每次将一个节点周围的所有节点加入队列。 

BFS解决**最短路径**问题；

BFS 相对 DFS 的最主要的区别是：BFS 找到的路径一定是最短的，但代价就是空间复杂度可能比 DFS 大很多。 

### BFS通用模板

广度优先搜索算法，常用来解决**最短路径问题**，第一次遍历到目的节点，所经历的路径是最短路径。

只能用来求解无权图的最短路径。

二叉树的BFS由于不会走回头路，所以不需要`visited`数组标记；

**BFS通用框架:**

```python
from collections import deque


def BFS(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []
    que = deque([root])
    res = []
    while que:
        size = len(que)  # 记录每层尺寸
        for _ in range(size):
            node = que.popleft()
            # 执行特定处理
            if node.left:
                que.append(node.left)
            if node.right:
                que.append(node.right)
    return res
```

`visited` 的主要作用是防止走回头路，大部分时候都是必须的，但是像一般的二叉树结构，没有子节点到父节点的指针，不会走回头路就不需要 `visited`。 

### 二叉树BFS

二叉树的层序遍历，就是图论的广度优先搜索在二叉树中的应用。需要借助==**队列**==实现。队列先进先出，符合一层一层遍历的逻辑。

#### 二叉树层序遍历模板

##### [102. 二叉树的层序遍历](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/)

**Python:**

```python
from collections import deque


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        que = deque([root])
        res = []
        while que:
            size = len(que)  # 记录每层尺寸
            level = []
            for _ in range(size):
                node = que.popleft()
                level.append(node.val)
                if node.left:
                    que.append(node.left)
                if node.right:
                    que.append(node.right)
            res.append(level)
        return res
```

##### [107. 二叉树的层序遍历 II](https://leetcode.cn/problems/binary-tree-level-order-traversal-ii/)

**思路：**

​	相对于102.二叉树的层序遍历，就是最后把result数组反转一下就可以了。

**Python：**

```python
class Solution:
    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        que = deque([root])
        res = []
        while que:
            size = len(que)  # 记录每层尺寸
            level = []
            for _ in range(size):
                node = que.popleft()
                level.append(node.val)
                if node.left:
                    que.append(node.left)
                if node.right:
                    que.append(node.right)
            res.append(level)
        res.reverse()  # 原地反转
        return res
```

#### 练习题目

#### [655. 输出二叉树](https://leetcode.cn/problems/print-binary-tree/)

```python
from collections import deque


class Solution:
    def get_height(self, root: Optional[TreeNode]) -> int:
        height = -1
        que = deque([root])
        while que:
            size = len(que)
            height += 1
            for _ in range(size):
                cur = que.popleft()
                if cur.left:
                    que.append(cur.left)
                if cur.right:
                    que.append(cur.right)
        return height

    def printTree(self, root: Optional[TreeNode]) -> List[List[str]]:
        height = self.get_height(root)
        print(height)
        m = height + 1
        n = 2**m - 1
        # res = [["" for _ in range(n)]] * m  # 浅拷贝，不可行
        res = [[""] * n for _ in range(m)]
        print(res)
        que = deque([(root, 0, (n - 1) // 2)])
        while que:
            cur, r, c = que.popleft()
            res[r][c] = str(cur.val)
            if cur.left:
                que.append((cur.left, r + 1, c - 2**(height - r - 1)))
            if cur.right:
                que.append((cur.right, r + 1, c + 2**(height - r - 1)))
        return res
```

##### [199. 二叉树的右视图](https://leetcode.cn/problems/binary-tree-right-side-view/)

给定一个二叉树的 **根节点** `root`，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。 

**思路：**

​	层序遍历的时候，判断是否遍历到单层的最后面的元素，如果是，就放进result数组中，随后返回result就可以了。

**Python:** 

```python
from collections import deque


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        res = []
        que = deque([root])
        while que:
            size = len(que)
            most_right = 0
            for _ in range(size):
                node = que.popleft()
                most_right = node.val
                if node.left is not None:
                    que.append(node.left)
                if node.right is not None:
                    que.append(node.right)
            res.append(most_right)
        return res
```

##### [637. 二叉树的层平均值](https://leetcode.cn/problems/average-of-levels-in-binary-tree/)

给定一个非空二叉树的根节点 `root` , 以数组的形式返回每一层节点的平均值。与实际答案相差 `10-5` 以内的答案可以被接受。 

**思路：**层序遍历每层的时候，求和取均值。

**Python:**

```c++
class Solution {
public:
    vector<double> averageOfLevels(TreeNode* root) {
        queue<TreeNode*> que;
        if (root != NULL) que.push(root);
        vector<double> result;
        while (!que.empty()) {
            int size = que.size();
            double sum = 0; // 统计每一层的和
            for (int i = 0; i < size; i++) {
                TreeNode* node = que.front();
                que.pop();
                sum += node->val; // 统计每一层的和
                if (node->left) que.push(node->left);
                if (node->right) que.push(node->right);
            }
            result.push_back(sum / size); // 将每一层均值放进结果集
        }
        return result;
    }
};
```

##### [515. 在每个树行中找最大值](https://leetcode.cn/problems/find-largest-value-in-each-tree-row/)

​	给定一棵二叉树的根节点 `root` ，请找出该二叉树中每一层的最大值。 

**思路：**层序遍历，取每一层的最大值

**python:**

```python
class Solution:
    def largestValues(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        if root is None:
            return res
        que = deque([root])
        while que:
            size = len(que)
            tmp = -float("inf")  # 最小值
            for _ in range(size):
                node = que.popleft()
                tmp = max(tmp, node.val)
                if node.left:
                    que.append(node.left)
                if node.right:
                    que.append(node.right)
            res.append(tmp)
        return res
```

##### [116. 填充每个节点的下一个右侧节点指针](https://leetcode.cn/problems/populating-next-right-pointers-in-each-node/)

给定一个 **完美二叉树** ，其所有叶子节点都在同一层，每个父节点都有两个子节点。二叉树定义如下： 

```c
struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
```

**思路：**

本题依然是层序遍历，只不过在单层遍历的时候记录一下本层的头部节点，然后在遍历的时候让前一个节点指向本节点就可以了。

**Python:**

```c++
class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        if not root:
            return None
        que = deque([root])
        while que:
            size = len(que)
            for i in range(size):
                cur = que.popleft()
                if i < size - 1:
                    cur.next = que[0]
                if cur.left:
                    que.append(cur.left)
                if cur.right:
                    que.append(cur.right)
        return root
```

##### [117. 填充每个节点的下一个右侧节点指针 II](https://leetcode.cn/problems/populating-next-right-pointers-in-each-node-ii/)

这道题目说是二叉树，但116题目说是完整二叉树，其实没有任何差别，一样的代码一样的逻辑一样的味道 

##### [104. 二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)

**思路：**

​	二叉树最大深度就是二叉树的层数。

**Python：**

```c++
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        que = deque([root])
        count = 0
        while que:
            count += 1
            size = len(que)
            for _ in range(size):
                cur = que.popleft()
                if cur.left:
                    que.append(cur.left)
                if cur.right:
                    que.append(cur.right)
        return count
```

##### [111. 二叉树的最小深度](https://leetcode.cn/problems/minimum-depth-of-binary-tree/)

**思路：**

​	当左右孩子都为空的时候，才说明遍历的最低点了 。层序遍历时判断什么时候遇到左右孩子全为空。

**Python:**

```python
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        que = deque([root])
        count = 0
        while que:
            count += 1
            size = len(que)
            for _ in range(size):
                cur = que.popleft()
                if cur.left is None and cur.right is None:
                    return count
                if cur.left:
                    que.append(cur.left)
                if cur.right:
                    que.append(cur.right)
        return count
```



##### [103. 二叉树的锯齿形层序遍历](https://leetcode-cn.com/problems/binary-tree-zigzag-level-order-traversal/)

```python
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        res = []
        que = deque([root])
        flag = 0
        while que:
            ans = []
            size = len(que)
            for _ in range(size):
                cur = que.popleft()
                ans.append(cur.val)
                if cur.left:
                    que.append(cur.left)
                if cur.right:
                    que.append(cur.right)
            if flag:
                ans.reverse()
            flag = 0 if flag else 1
            res.append(ans)
        return res
```

### 多叉树BFS

跟二叉树类似；

#### [429. N 叉树的层序遍历](https://leetcode.cn/problems/n-ary-tree-level-order-traversal/)

**Python:**

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
"""

class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        if root is None:
            return []
        res = []
        que = deque([root])
        while que:
            level = []
            size = len(que)
            for _ in range(size):
                cur = que.popleft()
                level.append(cur.val)
                for child in cur.children: # 多叉树的区别
                    que.append(child)
            res.append(level)
        return res
```

### 网格 BFS

为了防止经过已经走过的点，加入`visited`数组；树是不需要`visited`数组的。

```python

```

#### 典型题目

##### [1091. 二进制矩阵中的最短路径](https://leetcode-cn.com/problems/shortest-path-in-binary-matrix/)

##### [1162. 地图分析](https://leetcode-cn.com/problems/as-far-from-land-as-possible/)

LeetCode111.二叉树的最小深度（简单） 

LeetCode752.打开转盘锁（中等） 

##### [773. 滑动谜题](https://leetcode-cn.com/problems/sliding-puzzle/)

### 图

![img](https://pic3.zhimg.com/80/v2-1bbc3c5ab37b83a279675c647ccac7d2_1440w.webp)

```python
# 用字典表示一个图
graph={'A':['B','C'],
'B':['A','C','D'],
'C':['A','B','D','E'],
'D':['B','C','E','F'],
'E':['D','C'],
'F':['D']}
```

代码模板：

```python
def BFS(graph, s):
    queue = []
    queue.append(s)
    seen = set()
    seen.add(s)
    while len(queue) > 0:
        vetex = queue.pop(0)
        nodes = graph[vetex]
        for w in nodes:
            if w not in seen:
                queue.append(w)
                seen.add(w)
        print(vetex)


def DFS(graph, s):
    stack = []
    stack.append(s)
    seen = set()
    seen.add(s)
    while len(stack) > 0:
        vetex = stack.pop()
        nodes = graph[vetex]
        for w in nodes:
            if w not in seen:
                stack.append(w)
                seen.add(w)
        print(vetex)
```





## DFS 深度优先搜索

​	DFS本质上是一种枚举，借助递归实现。

​	DFS一般解决有多少条满足条件的路径；

**深度优先搜索的步骤：**

​	1、递归下去；

​	2、回溯上来。

**DFS思想通用模板：**

```c
const visited = {}
function dfs(i) {
    if (满足特定条件）{
        // 返回结果 or 退出搜索空间
    }

    visited[i] = true // 将当前状态标为已搜索
    for (根据i能到达的下个状态j) {
        if (!visited[j]) { // 如果状态j没有被搜索过
            dfs(j)
        }
    }
}
```

### 二叉树深度遍历（DFS）

​	树的前序遍历、中序遍历、后序遍历都属于DFS深度优先搜索遍历。

​	区别就是方向是**单向的不会回头**。

**前序遍历：**

```c++
class Solution {
public:
    void traversal(TreeNode* cur, vector<int>& vec) {
        if (cur == NULL) return;
        vec.push_back(cur->val);    // 中
        traversal(cur->left, vec);  // 左
        traversal(cur->right, vec); // 右
    }
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> result;
        traversal(root, result);
        return result;
    }
};
```

**递归三要素：**

1、确定递归函数的参数和返回值；

2、确定**终止条件**；

3、确定单层递归的逻辑；

#### [144. 二叉树前序遍历](https://leetcode-cn.com/problems/binary-tree-preorder-traversal/)

1. **确定递归函数的参数和返回值**：因为要打印出前序遍历节点的数值，所以参数里需要传入vector在放节点的数值，除了这一点就不需要在处理什么数据了也不需要有返回值，所以递归函数返回类型就是void，代码如下：

   ```c
   void traversal(TreeNode* cur, vector<int>& vec)
   ```

2. **确定终止条件**： 在递归的过程中，如何算是递归结束了呢，当然是当前遍历的节点是空了，那么本层递归就要要结束了，所以如果当前遍历的这个节点是空，就直接return。

   ```c
   if (cur == NULL) return;
   ```

3. **确定单层递归的逻辑**：前序遍历是中左右的循序，所以在单层递归的逻辑，是要先取中节点的数值，代码如下：

   ```c
   vec.push_back(cur->val);    // 中
   traversal(cur->left, vec);  // 左
   traversal(cur->right, vec); // 右
   ```

**完整的前序遍历C代码：**

```c
void preorder(struct TreeNode *root, int *res, int *resSize)
{
    if (root == NULL) {
        return;
    }
    res[(*resSize)++] = root->val;
    preorder(root->left, res, resSize);
    preorder(root->right, res, resSize);
}

int *preorderTraversal(struct TreeNode *root, int *returnSize)
{
    int *res = malloc(sizeof(int) * 2000);
    *returnSize = 0;
    preorder(root, res, returnSize);
    return res;
}
```

**Python代码：**

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(cur: TreeNode):
            if cur is None:
                return
            res.append(cur.val)
            dfs(cur.left)
            dfs(cur.right)
        res = []
        dfs(root)
        return res
```

#### [94. 二叉树中序遍历](https://leetcode-cn.com/problems/binary-tree-inorder-traversal/)

```c++
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(cur: TreeNode):
            if cur is None:
                return
            dfs(cur.left)
            res.append(cur.val)  # 中序
            dfs(cur.right)
        res = []
        dfs(root)
        return res
```

#### [145. 二叉树后序遍历](https://leetcode-cn.com/problems/binary-tree-postorder-traversal/)

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(cur: TreeNode):
            if cur is None:
                return
            dfs(cur.left)
            dfs(cur.right)
            res.append(cur.val)
        res = []
        dfs(root)
        return res
```

#### 前序遍历+回溯

##### [257. 二叉树的所有路径](https://leetcode.cn/problems/binary-tree-paths/)

```python
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        def dfs(cur: TreeNode, path: str):
            if cur is None:
                return
            path += str(cur.val)  # 节点加入到当前路径
            if cur.left is None and cur.right is None:
                res.append(path)
                return
            path += "->"
            dfs(cur.left, path)
            dfs(cur.right, path)

        res = []
        dfs(root, "")
        return res
```

传参字符串和传参列表是不一样的，列表是可变对象。

#### [112. 路径总和](https://leetcode-cn.com/problems/path-sum/)

#### [113. 路径总和 II](https://leetcode-cn.com/problems/path-sum-ii/)

通过访问一个结点 将该节点的值与count相减 直到遇到count==0时并且左右孩子为NULL时 该路径就是要找的路径 

#### [865. 具有所有最深节点的最小子树](https://leetcode-cn.com/problems/smallest-subtree-with-all-the-deepest-nodes/)

### 多叉树DFS

删除目录；

### 网格 DFS

​	网格结构要比二叉树结构稍微复杂一些，它其实是一种简化版的**图**结构。 

​	要写好网格上的 DFS 遍历，我们首先要理解二叉树上的 DFS 遍历方法，再类比写出网格结构上的 DFS 遍历。 

​	参考labuladong算法小抄的《FloodFill算法详解及应用》。

​	参考https://leetcode-cn.com/problems/number-of-islands/solution/dao-yu-lei-wen-ti-de-tong-yong-jie-fa-dfs-bian-li-/

#### 	网格DFS模板

```c
// 判断是否出界函数
boolean inArea(int[][] grid, int x, int y) {
    return 0 <= x && x < grid.length 
        	&& 0 <= y && y < grid[0].length;
}

// (x, y)为坐标位置
void dfs(int grid[][], int x, int y)
{
    // 如果出界
    if (!inArea(grid, x, y)) { 
        return;
    }
    // 这里和二叉树的区别，网格需要防止往回走
    if (grid[r][c] != 1) { // 如果这个格子不是岛屿，直接返回
        return;
    }
    grid[r][c] = 2; // 将格子标记为「已遍历过」
    
    // 访问上下左右四个相领结点
    dfs(grid, x, y - 1); // 上
    dfs(grid, x, y + 1); // 下
    dfs(grid, x - 1, y); // 左
    dfs(grid, x + 1, y); // 右
}
```

首先，网格结构中的格子有多少相邻结点？答案是上下左右四个。对于格子 (r, c) 来说（r 和 c 分别代表行坐标和列坐标），四个相邻的格子分别是 (r-1, c)、(r+1, c)、(r, c-1)、(r, c+1)。换句话说，网格结构是「**四叉树**」的。

![网格结构中四个相邻的格子](https://pic.leetcode-cn.com/63f5803e9452ccecf92fa64f54c887ed0e4e4c3434b9fb246bf2b410e4424555.jpg) 

`grid[r][c]` 会出现数组下标越界异常的格子，也就是那些超出网格范围的格子。 

![网格 DFS 的 base case](https://pic.leetcode-cn.com/5a91ec351bcbe8e631e7e3e44e062794d6e53af95f6a5c778de369365b9d994e.jpg) 

**如何避免重复遍历?**

网格结构的DFS与二叉树DFS的最大不同之处在于，二叉树不会往回走，但是网格有可能往回走，会遍历中可能遇到遍历过的结点 ，陷入死循环。需要标记已经遍历过的格子。

#### 典型题

200岛屿数量

- 1. 岛屿数量
- 1. 岛屿的周长
- 1. 岛屿的最大面积
- 1. 不同岛屿的数量
- 1. 图像渲染
- 1. 被围绕的区域
- 剑指 Offer 13. 机器人的运动范围

#### 练习题

##### [200. 岛屿数量](https://leetcode.cn/problems/number-of-islands/)

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        row = len(grid)
        col = len(grid[0])

        def dfs(i, j):
            if i < 0 or i >= row or j < 0 or j >= col:  # 越界
                return
            if grid[i][j] == "0":  # 海水
                return
            grid[i][j] = "0"  # 陆地标记为海水
            dfs(i - 1, j)
            dfs(i + 1, j)
            dfs(i, j - 1)
            dfs(i, j + 1)

        count = 0
        for i in range(row):
            for j in range(col):
                if grid[i][j] == "1":
                    count += 1
                    dfs(i, j)
        return count
```



##### [695. 岛屿的最大面积](https://leetcode-cn.com/problems/max-area-of-island/)

```c
class Solution:
    def dfs(self, grid, i, j) -> int:
        if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]):  # 越界
            return 0
        if grid[i][j] != 1:  # 非水
            return 0
        grid[i][j] = 2  # 标记走过
        ans = 1
        ans += self.dfs(grid, i - 1, j)
        ans += self.dfs(grid, i + 1, j)
        ans += self.dfs(grid, i, j - 1)
        ans += self.dfs(grid, i, j + 1)
        return ans

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        ans = 0
        for i, l in enumerate(grid):
            for j, n in enumerate(l):
                ans = max(self.dfs(grid, i, j), ans)
        return ans

```

##### [827. 最大人工岛](https://leetcode-cn.com/problems/making-a-large-island/)

##### [10.颜色填充](https://leetcode-cn.com/problems/color-fill-lcci/)

```c
bool inArea(int** image, int imageSize, int* imageColSize, int sr, int sc)
{
    return 0 <= sr && sr < imageSize && 0 <= sc && sc < imageColSize[0];  
}

void dfs(int** image, int imageSize, int* imageColSize, int sr, int sc, int origColor, int newColor)
{
    if (!inArea(image, imageSize, imageColSize, sr, sc)) { // 出界
        return;
    }
    if (image[sr][sc] != origColor) { // 非目标值或者走过的值
        return;
    }
    image[sr][sc] = newColor;
    dfs(image, imageSize, imageColSize, sr + 1, sc, origColor, newColor);
    dfs(image, imageSize, imageColSize, sr - 1, sc, origColor, newColor);
    dfs(image, imageSize, imageColSize, sr, sc + 1, origColor, newColor);
    dfs(image, imageSize, imageColSize, sr, sc - 1, origColor, newColor);
}

int** floodFill(int** image, int imageSize, int* imageColSize, int sr, int sc, int newColor, int* returnSize, int** returnColumnSizes){
    *returnSize = imageSize;
    *returnColumnSizes = imageColSize;
    int origColor = image[sr][sc];
    if (newColor == origColor) {
        return image;
    }
    dfs(image, imageSize, imageColSize, sr, sc, origColor, newColor);
    return image;
}
```

##### [463. 岛屿的周长](https://leetcode-cn.com/problems/island-perimeter/)

##### [417. 太平洋大西洋水流问题](https://leetcode-cn.com/problems/pacific-atlantic-water-flow/)

##### [1020. 飞地的数量](https://leetcode-cn.com/problems/number-of-enclaves/)

##### [1391. 检查网格中是否存在有效路径](https://leetcode-cn.com/problems/check-if-there-is-a-valid-path-in-a-grid/)

##### [1034. 边界着色](https://leetcode-cn.com/problems/coloring-a-border/)

##### [1706. 球会落何处](https://leetcode-cn.com/problems/where-will-the-ball-fall/)

##### [1992. 找到所有的农场组](https://leetcode-cn.com/problems/find-all-groups-of-farmland/)

## 回溯算法

**定义:** 一种通过搜索所有可能的候选解来找出所有的解的算法。

回溯算法是一种纯暴力法。本质上是穷举。

实际上就是⼀个**决策树**的遍历过程，为啥叫决策树？因为在每个节点其实都在做决策。

	+ 其核心就是 for 循环⾥⾯的递归
	
	+ 在递归调用之前「做选择」
	
	+ 在递归调用之后「撤销选择」     

**for循环可以理解是横向遍历，backtracking（递归）就是纵向遍历** 

回溯算法属于递归，回溯函数=递归函数；

### Python回溯算法模板

**回溯模板：**

```python
def backtrack(路径, 选择列表):
    if 满足结束条件:
        result.add(路径)
        return
    
    for 选择 in 选择列表:
        做选择
        backtrack(路径, 选择列表)  # 下一步往哪走
        撤销选择
```

回溯算法属于N叉树的深度遍历，属于多叉树DFS一种。

**Python回溯模板：**

```python
res = []
path = []

def backtrack(未探索的区域, res, path):
    if path 满足条件:
        res.add()  # 深度拷贝
        # return 如果不需要继续搜索就return
    for 选择 in 未探索区域当前可能的选择:
        if 当前选择满足要求:
            path.add(当前选择) # 做选择 
            backtrack(新的未探索区域, res, path)  # 下一步往哪走
            path.pop()  # 撤销选择
```

### 典型例题

#### [组合](https://leetcode.cn/problems/combinations/)

组合和排列的区别：**组合无序，排列有序**。

**Python实现：**

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = [] 
        path = []

        def dfs(start):
            if len(path) == k:
                res.append(path.copy())
                return
            for i in range(start, n + 1):
                path.append(i)  # 做选择
                dfs(i + 1)
                path.pop()  # 撤销选择
        dfs(1)
        return res
```

#### [组合总和](https://leetcode.cn/problems/combination-sum-iii/)(不可重复使用)

```python
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        res = []
        path = []

        def dfs(start):
            if len(path) == k and sum(path) == n:
                res.append(path.copy())
                return
            for i in range(start, 10):
                path.append(i)
                dfs(i + 1)
                path.pop()
        dfs(1)
```

#### [组合总和](https://leetcode.cn/problems/combination-sum/)（可重复使用）

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        path = []

        def dfs(start):
            if sum(path) == target:
                res.append(path.copy())
                return
            if sum(path) > target:  # 不加会超时退出
                return
            for i in range(start, len(candidates)):
                path.append(candidates[i])
                dfs(i)  # 可以重复
                path.pop()
        dfs(0)
        return res
```

#### [组合总和](https://leetcode.cn/problems/combination-sum-ii/)（不可重复使用 + 返回值列表去重）

下次再做

#### 电话号码的组合

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits: # 必须有，否则返回[""]
            return []
        table = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz"
        }
        res = []
        path = []

        def dfs(start):
            if start == len(digits):
                res.append("".join(path))
                return
            key = digits[start]
            for i in table[key]:
                path.append(i)
                dfs(start + 1)
                path.pop()

        dfs(0)
        return res
```



#### 切割

其实只要意识到这是切割问题，**切割问题就可以使用回溯搜索法把所有可能性搜出来**。

[复原IP地址](https://programmercarl.com/0093.%E5%A4%8D%E5%8E%9FIP%E5%9C%B0%E5%9D%80.html#%E5%9B%9E%E6%BA%AF%E4%B8%89%E9%83%A8%E6%9B%B2)

#### 全排列问题

排序是有序的，组合是无序的。

**排列是有序的，也就是说 [1,2] 和 [2,1] 是两个集合**。

处理排列问题就不用使用startIndex了， 但排列问题需要一个used数组，标记已经选择的元素。

因为排列问题，每次都要从头开始搜索，例如元素1在[1,2]中已经使用过了，但是在[2,1]中还要再使用一次1。 

**而used数组，其实就是记录此时path里都有哪些元素使用了，一个排列里一个元素只能使用一次**。 

#### N皇后问题

#### [1219. 黄金矿工](https://leetcode-cn.com/problems/path-with-maximum-gold/)



## 贪心算法

![贪心算法大纲](https://code-thinking-1253855093.file.myqcloud.com/pics/20210917104315.png) 

### 贪心思想 

​	**贪心的本质是选择每一阶段的局部最优，从而达到全局最优**。 

​	**贪心算法并没有固定的套路**。 难点在于如何通过局部最优推出全局最优，说白了就是常识性推导和举反例。

### 典型题目

#### [455. 分发饼干](https://leetcode.cn/problems/assign-cookies/)

**思路：**

​	尽可能不要造成饼干的浪费，大饼干既可以满足胃口大的孩子也可以满足胃口小的孩子。

​	局部最优：大饼干分给胃口大的；

​	全局最优：尽快喂饱尽可能多的孩子；

```python
class Solution:
    # 思路1：优先考虑胃饼干
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort()
        s.sort()
        res = 0
        for i in range(len(s)):
            if res <len(g) and s[i] >= g[res]:  #小饼干先喂饱小胃口
                res += 1
        return res
```



#### [1648. 销售价值减少的颜色球](https://leetcode-cn.com/problems/sell-diminishing-valued-colored-balls/)

#### [1705. 吃苹果的最大数目](https://leetcode-cn.com/problems/maximum-number-of-eaten-apples/)

考查贪心+堆

## 动态规划（可信不考）

​	重叠子问题；

​	用**递推**而不是递归，动态规划中每一个状态一定是由上一个状态推导出来的。

​	难点是确定**递推公式** 。

### 题目

#### [509. 斐波那契数](https://leetcode.cn/problems/fibonacci-number/)

#### [70. 爬楼梯](https://leetcode.cn/problems/climbing-stairs/)

#### [746. 使用最小花费爬楼梯](https://leetcode.cn/problems/min-cost-climbing-stairs/)

#### [62. 不同路径](https://leetcode.cn/problems/unique-paths/)

如果是递归实现DFS解决，会超时；

```c
int Dfs(int i, int j, int m, int n)
{
    if (i > m || j > n) {
        return 0; // 越界了
    }
    if (i == m && j == n) { 
        return 1; // 找到了一种方法
    }
    return Dfs(i + 1, j, m, n) + Dfs(i, j + 1, m, n); // 不会回头
}
int uniquePaths(int m, int n){
    return Dfs(1, 1, m, n);
}
```

采用动态规划做不会超时，涉及二维动态数组；

动态规划采用空间换时间的思想，可以降低时间复杂度。

```c
int uniquePaths(int m, int n){
    int dp[1000][1000] = {0};
    for (int i = 0; i < m; i++) {
        dp[i][0] = 1;
    }
    for (int j = 0; j < n; j++) {
        dp[0][j] = 1;
    }
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }
    return dp[m - 1][n-1];
}
```

#### [63. 不同路径 II](https://leetcode.cn/problems/unique-paths-ii/)

```c
int uniquePathsWithObstacles(int **obstacleGrid, int obstacleGridSize, int *obstacleGridColSize)
{
    int dp[1000][1000] = {0};
    int m = obstacleGridSize;
    int n = obstacleGridColSize[0];
    for (int i = 0; i < m && obstacleGrid[i][0] == 0; i++) {
        dp[i][0] = 1;
    }
    for (int j = 0; j < n && obstacleGrid[0][j] == 0; j++) {
        dp[0][j] = 1;
    }
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            if (obstacleGrid[i][j] == 1) {
                continue;
            }
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }
    return dp[m - 1][n - 1];
}
```



## 纯模拟题

### [1041. 困于环中的机器人](https://leetcode-cn.com/problems/robot-bounded-in-circle/)

### [2069. 模拟行走机器人 II](https://leetcode-cn.com/problems/walking-robot-simulation-ii/)

### [749. 隔离病毒](https://leetcode-cn.com/problems/contain-virus/)

### [LCP 03. 机器人大冒险](https://leetcode-cn.com/problems/programmable-robot/)

### [535. 找出数组游戏的赢家](https://leetcode-cn.com/problems/find-the-winner-of-an-array-game/)

### [816. 模糊坐标](https://leetcode-cn.com/problems/ambiguous-coordinates/)

### [1894. 找到需要补充粉笔的学生编号](https://leetcode-cn.com/problems/find-the-student-that-will-replace-the-chalk/)

### [2105. 给植物浇水 II](https://leetcode-cn.com/problems/watering-plants-ii/)

### [1324. 竖直打印单词](https://leetcode-cn.com/problems/print-words-vertically/)

### [393. UTF-8 编码验证](https://leetcode-cn.com/problems/utf-8-validation/)

### [面试题 03.03. 堆盘子](https://leetcode-cn.com/problems/stack-of-plates-lcci/)





# Python必备语法

## 数字类型

数字类型是不可变对象；

+ 整型 int

+ 浮点型 float
+ 复数

### 数字类型强制转换

- **int(x)** 将x转换为一个整数。
- **float(x)** 将x转换到一个浮点数。

### 数字运算

#### /、//、%

+ `/` ：小数除法

```python
>>> 9 / 2
4.5
```

+ `//`：整除除法，向下取整 

  **注意：** `//`得到的并不一定是整数类型的数，它与分母分子的数据类型有关系。

```python
>>> 9 // 2
4
>>> -9 // 2
-5
>>> 7.0 // 2
3.0
```

注意：

+ `%`：取余

#### 次方运算 `**`

+ 方式一：基于`**`运算符

```python
>>> 2 ** 3  # 2的3次方
8
```

+ 方式二：基于python自带库函数`pow(x, y)`

```python
>>> pow(2, 3)
8
```

#### 开平方根

基于三方库`math`的`sqrt(x)`函数，返回x平方根，结果float类型。

```python
>>> import math
>>> math.sqrt(16)
4
```

#### 整除运算，向上取整

**注意：** 除法运算如果想向上取证，借用`math.ceil()`函数

```python
import math
math.ceil(9 / 2)
```

#### 位运算

`& | ^ ~ << >>`都是C语言类似；

如果表示二进制，使用`0b`开头；

```python
>>> a = 0b00111100
>>> a
60
```

如果10进制想转二进制：

```python
>>> bin(60)
'0b00111100'
```

### 两数交换 `a, b = b, a`

python变量本质不是存储值，而是引用一个内存地址。变量的每一次初始化，都开辟了一个新的空间，将新内容的地址赋值给变量。

### 无穷大和无穷小

**方法一**：

```python
max_num = float("inf") # 无穷大

min_num = -float("inf") # 无穷小
```

**方法二：** 从Python3.5开始，您可以使用`math.inf`

```python
import math
max_num = math.inf # 无穷大
min_num = -math.inf
```



### 常用函数

+ 取绝对值`abs(x)`
+ 小数向上取整`math.ceil(x)`
+ 小数向下取整`math.floor(x)`
+ 两数最大值`max(x1, x2)`
+ 两数最小值`min(x1, x2)`

## 字符串类型

**==字符串是不可变对象；==**不能增删改；

Python 不支持字符类型，单字符在 Python 中也是作为一个字符串使用。

### 创建

```python
# 创建空对象
s1 = ''
s2 = str()
# 创建非空对象
s3 = "abc"
```

### 访问（查）

切片访问：`变量[头下标:尾下标]`

下标访问某字符：`s[i]`，如s[1]

### 更新（改）

字符串是不可变对象，更新相当于把新的字符串对象挂接在原变量名。

```python
var1 = 'Hello World!'
print("已更新字符串 : ", var1[:6] + 'Runoob!')
```

### 类型转换

#### 字符串转整型

+ 10进制字符串转为int

  ```python
  int("12")
  # 输出12
  ```

+ 16进制字符串转int

  ```python
  int("12", 16)
  # 输出18
  ```

+ 二进制字符串转int

  ```python
  int('10100111110', 2)    
  ```

#### 整型转字符串

+ int转为10进制string

  ```shell
  str(18)
  ```

+ int转化为16进制string

  ```shell
  hex(18)
  ```

+ int转为2进制字符串

  ```shell
  bin(10)
  ```

### 字符串运算符

+ 字符串拼接：`+`
+ 字符串重复：`*`
+ 下标访问某字符：`[]`，如s[1]
+ 截取字符串：`[:]`，**左闭右开原则**，以 **0** 为开始值，**-1** 为从末尾的开始位置。
+ **判断是否是子串**：`in`和`not in`

+ 原始字符串，排除转义效果：`r"内容"`

### 格式化字符串

+ **方式一：**`%`，将一个值插入到一个有字符串格式符 %s 的字符串中

```python
>>> print("我叫%s, 今年%d岁!" % ('小明', 10))
# 我叫小明, 今年10岁!
```

常用格式化符号：`%s`字符串、`%d`整数、`%x`无符号十六进制

格式化符辅助指令：`-`左对齐、`*`定义小数点精度

+ **方式二：**`str.format`函数

```python
>>> "{} {}".format("hello", "world")    # 不设置指定位置，按默认顺序
'hello world'
 
>>> "{0} {1}".format("hello", "world")  # 设置指定位置
'hello world'
 
>>> "{1} {0} {1}".format("hello", "world")  # 设置指定位置
'world hello world'
```

也可以设置参数：

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
print("网站名：{name}, 地址 {url}".format(name="菜鸟教程", url="www.runoob.com"))
 
# 通过字典设置参数
site = {"name": "菜鸟教程", "url": "www.runoob.com"}
print("网站名：{name}, 地址 {url}".format(**site))
 
# 通过列表索引设置参数
my_list = ['菜鸟教程', 'www.runoob.com']
print("网站名：{0[0]}, 地址 {0[1]}".format(my_list))  # "0" 是必须的
```

+ **方式三：**`f-string`字面量格式化字符串

仅python3.6之版本支持；

```python
>>> name = 'Runoob'
>>> f'Hello {name}'  # 替换变量
'Hello Runoob'
```

用了这种方式明显更简单了，不用再去判断使用 %s，还是 %d。

### 常用函数

#### 子字符串查找`find`

`str.find(substr, beg, end)`，从左往右查找，如果存在返回第一个匹配索引，不存在返回-1；

`str.index(substr,beg, end)`，如果存在返回第一个匹配索引，不存在会==抛出异常==；**index不推荐使用**；

`str.rfind()`，和`find`类似，从右往左查找；

`str.rindex()`，和`index`类似，从右往左查找；

#### 字符串修剪`strip`

`str.strip()`用于删除字符串首尾指定字符或字符序列（默认空格或换行符），并返回新字符串对象；

对应的单边修剪有：`str.lstrip()`只修剪左边，`str.rstrip()`只修剪右边；

#### 字符串切割`split`

​		`str.split(str="xx", num)`，指定分隔符对字符串进行切片，如果第二个参数 num 有指定值，则分割为 num+1 个子字符串。返回**字符串列表**。

#### 字符串替换replace

语法：

```python
str.replace(old, new[, max])
```

`replace() `方法把字符串中的 `old`（旧字符串） 替换成 `new`(新字符串)，如果指定第三个参数`max`，则替换不超过 max 次。替换后返回新的字符串对象；

```python
s = "this is string example....wow!!! this is really string"
new_s = s.replace("is", "was")
print(new_s)  # 新的内存空间
print(s) # 原字符串不变
#  thwas was string example....wow!!! thwas was really string
#  this is string example....wow!!! this is really string
```

#### str.join()

```python
str.join(sequence)
```

将序列中的元素以指定的字符连接生成一个新的字符串。

+ 列表转字符串
+ 字符串调整后转字符串

**例子：**

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

symbol = "-"
seq = ("a", "b", "c") # 字符串序列
# seq = "abc"
print(symbol.join(seq))

# a-b-c
```

#### 字符串类型判断

+ `isdigit()` 如果字符串只包含数字，返回 True，否则False

+ `isalpha()` 如果字符串至少有一个字符并且所有字符都是字母或中文字则返回 True, 否则返回 False

  `str.islower()` 检测字符串是否由小写字母组成。

  `str.isupper() `检测字符串中所有的字母是否都为大写。

#### 字符串大小写类型转换

`str.lower()`将字符串中的所有大写字符转为小写。

`str.upper()`将字符串中的所有小写字母转为大写。

[1047. 删除字符串中的所有相邻重复项](https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/)

```python
class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack = []
        for v in s:
            if stack and v == stack[-1]:
                stack.pop()
            else:
                stack.append(v)
        return "".join(stack)
```

## 列表 （可模拟栈）

列表是可变对象；

**python3之后需要直接导入List类：**

```python
from typing import List
```

### 创建列表

```python
# 创空列表
list1 = list()
list2 = []
# 带初始值创建列表
list3 = ['Google', 'Runoob', 1997, 2000]
# 使用*法创建，注意是浅拷贝
list4 = [1, 2, 3] * 3
```

### 访问列表

+ 索引访问单元素：`list[i]`
+ 切片访问`[:]`，遵循左闭右开

### 更新列表(增、改)

+ **修改原有值**

由于列表是可变对象，可以直接对指定位置元素进行修改；

```python
#!/usr/bin/python3
 
list = ['Google', 'Runoob', 1997, 2000]
 
print ("第三个元素为 : ", list[2])
list[2] = 2001
print ("更新后的第三个元素为 : ", list[2])
```

+ **列表末尾添加新元素**，`append()`函数

  列表属于线性结构，`append()`函数可以直接在列表末尾添加新元素。

+ **在列表末尾追加另一个列表**，`list.extend`函数

  ```python
  list1 = ['Google', 'Runoob', 'Taobao']
  list2 = [0, 1, 2, 3, 4]
  list1.extend(list2)
  # ['Google', 'Runoob', 'Taobao', 0, 1, 2, 3, 4]
  ```

+ **插入**

### 删除

+ `del`语句

  **删除单一元素：**`del listname[index]`

  **删除一段连续元素：**`del listname[start:end]`

  删除整个列表对象：`del listname`

```python
list1 = ['Google', 'Runoob', 1997, 2000]
del list1[2]  # 删除指定元素
del list1[1:3]  # 删除一段元素
del list1  # 删除整个列表对象
```

+ `pop(index)`函数，按照索引删除；
`pop`函数默认索引为-1，删除列表最后元素，可以通过指定`index`删除指定元素，比如删除首元素`pop(0)`；
+ `clear()`函数，会清空为空列表`[]`；
+ `remove`函数，按照值进行删除，如果不存在会报异常；且只会删除第一个和指定值相同的元素。

```python
nums = [40, 36, 89, 2, 36, 100, 7]
#第一次删除36
nums.remove(36)
print(nums)
#第二次删除36
nums.remove(36)
```

### 列表操作运算符

+ 列表拼接 `+`
+ 列表重复 `*`
+ 存在判断`in`
+ 循环迭代 `for x in [1, 2 ,3]`

### python自带库函数

+ 列表长度：`len(list)`
+ 列表最大值 : `max(list)`
+ 列表最小值：`min(list)`
+ 将元素转化为列表：`list(seg)`

### 列表常用类方法

+ 统计某个元素的次数：`list.count(x)`
+ 找到指定元素第一个匹配值的索引：`list.index(obj)`，没找到会抛出异常；
+ 列表原地反转：`list.reverse()`，没有返回值；
+ 将对象插入列表: `list.insert(obj)`

#### 列表或字符串转字符串

Python中的一个字符串方法，它可以将一个字符串列表或元组中的所有元素连接起来。

```python
str.join(sequence)
```

### 列表排序

**sort 与 sorted 区别：**

+ sort 是应用在 list 上的方法，sorted 可以对所有可迭代的对象进行排序操作。
+ sort是对列表原地进行进行操作，**没有返回值**；sorted新建空间，有返回值；

#### sorted排序内置函数（优先使用）

#### sort排序方法 (原地排序)

默认reverse = False, 升序；

+ 按元素0（学号）排序

```python
students = [[3, 'Jack', 12], [2, 'Rose', 13], [1, 'Tom', 10], [5, 'Sam', 12], [4, 'Joy', 8]]
students.sort(key=lambda x: x[0])
print(students)
```

+ 按元素2（年龄）降序排序

```python
students = [[3, 'Jack', 12], [2, 'Rose', 13], [1, 'Tom', 10], [5, 'Sam', 12], [4, 'Joy', 8]]
students.sort(key=lambda x: x[2], reverse=True)
print(students)
```

+ **两字段排序**，按年龄为主要关键字，名字为次要关键字倒序排序；

```python
students = [[3, 'Jack', 12], [2, 'Rose', 13], [1, 'Tom', 10], [5, 'Sam', 12], [4, 'Joy', 8]]
students.sort(key=lambda x: [x[2], x[1]], reverse=True)
print(students)
```

+ 两元素一个升序，一个降序；**通过负数**

  ```python
  sort(key=lambda x: [x[1], -x[2], x[0]]) # lambda表达式，设计题排序必备
  ```

#### 题目

[**1825. 【软件认证】按身高和体重排队**](https://oj.rnd.huawei.com/problems/1825/submissions)

```python
class Solution:
    def sort_student(self, heights, widths):
        player_info = []
        for i in range(len(heights)):
            player_info.append((i + 1, heights[i], widths[i]))
        player_info.sort(key=lambda x: [x[1], x[2], x[0]])
        return [v[0] for v in player_info]


if __name__ == "__main__":
    count = int(input().strip())
    heights = list(map(int, input().strip().split(' ')))
    widths = list(map(int, input().strip().split(' ')))
    function = Solution()
    result = function.sort_student(heights, widths)
    print(' '.join(map(str, result)))
```

## 元组

元组是不可变对象；

### 创建元组

```python
# 创建空元组
tup1 = () 
tup2 = tuple()
# 有初始值元素
tup3 = (1, 2, 3)
tup4 = (1,) # 元组中只包含一个元素时，需要在元素后面添加逗号, 否则括号会被当作运算符使用。
```



### 元组推导式跟列表不一样

元组推导式返回的结果是一个**生成器对象**，而列表、字典、集合返回的都是相应对象本身；

如果使用元组推导式之后想返回元组对象，使用`tuple()`函数；

```python
a = (x for x in range(1,10))
# <generator object <genexpr> at 0x7faf6ee20a50>  # 返回的是生成器对象
tuple(a)
# 使用 tuple() 函数，可以直接将生成器对象转换成元组 (1, 2, 3, 4, 5, 6, 7, 8, 9)
```

##字典（哈希表）

字典是可变对象；

+ 键必须唯一。
+ 键必须是不可变类型 （数字、字符串、元组），键不能是列表。

### 创建字典

```python
# 创建空字典
dict1 = {}
dict2 = dict()
# 创建初值字典
dict3 = {'name': 'runoob', 'likes': 123, 'url': 'www.runoob.com'}
```

### 访问字典值

+ 直接`dict[key]`访问，但是如果键不存在会报错。

  ```python
  >>> tinydict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
  >>> tinydict['Age']
  7
  
  >>> tinydict["haha"]
  Traceback (most recent call last):
    File "D:\Program Files\JetBrains\PyCharm 2023.1.3\plugins\python\helpers\pydev\pydevconsole.py", line 364, in runcode
      coro = func()
    File "<input>", line 1, in <module>
  KeyError: 'haha'
  ```

+ `dict.get(key, default=None)`函数

  返回指定键的值，如果键不在字典中返回 default 设置的默认值；

  传参时不要加`default=`，因为Python 的底层是 C 写的，调用底层 C语言 的时候，在编译时无法解析这个参数的名称，而目前Python的底层设计无法解决这个问题，所以这里直接传入 default 的参数即可，不要加入`default=`，这样使用也不会造成问题。


### 添加或修改键值

+ 方式一：[]形式修改

```python
tinydict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
tinydict['Age'] = 8 # 如果键已存在，修改键值
tinydict['School'] = "菜鸟教程" # 如果键不存在，添加新的键值对
```

+ 方式二：`dict.setdefault(key, defult=None)`，但如果键不存在于字典中，将会添加键并将值设为default。

```python
tinydict = {'runoob': '已经存在', 'google': '不存在就添加'}

print("Value : %s" % tinydict.setdefault('runoob', None))  # 已经存在不会设置默认值
print("Value : %s" % tinydict.setdefault('Taobao', '淘宝'))  # 不存在，设置默认值
"""
Value : 已经存在
Value : 淘宝"""
```

### 删除字典元素

clear方法是删除字典所有元素，del 会直接删除该字典对象；

+ 删除字典单一元素

  1、`del dict[key]`

```python
del tinydict['Name'] # 删除某一个键值对
```

​		2、`tinydict.pop(key)`

+ 删除字典对象

  ```python
  del tinydict # 删除整个字典对象
  ```

+ 清空字典为空字典：`tinydict.clear()`

### 字典类常见方法

+ `dict.copy` 返回一个字典的浅拷贝
+ `dict.fromkeys()`创建一个新字典
+ `dict.items()`返回健值对列表
+ `dict.keys()`返回键列表
+ `dict.values`返回值列表
+ `dict.update(dict2)` 把字典参数 dict2 的 **键/值**对更新到字典 dict 里

### 遍历字典

（1）遍历key值

```python
 a = {'a': '1', 'b': '2', 'c': '3'}
 for key in a:
 	print(a[key])   
```

`for key in a:`和 `for key in a.keys():`完全等价。

（2）遍历value值

```python
 a = {'a': '1', 'b': '2', 'c': '3'}
 for value in a.values():
 	print(value)
```

（3）遍历字典键值对

```python
for kv in a.items():
    print(kv)
"""
('a', '1')
('b', '2')
('c', '3')
"""
```

（4）遍历字典健值

```python
for key,value in a.items():  
```

### 字典排序（本质是列表排序）

https://www.runoob.com/python3/python-sort-dictionaries-by-key-or-value.html

本质是列表排序

#### 键key排序+值value排序

```python
key_value = {2: 56, 1: 2, 5: 12, 4: 24, 6: 18, 3: 323}

print(sorted(key_value.keys()))  # 健列表排序
print(sorted(key_value.values()))  # 值列表排序
print(sorted(key_value.items()))  # 健、值二维列表排序
"""
[1, 2, 3, 4, 5, 6]
[2, 12, 18, 24, 56, 323]
[(1, 2), (2, 56), (3, 323), (4, 24), (5, 12), (6, 18)]
"""
```

#### 字典二维排序

键值排序必须加`items()`，按列表排序；

```python
key_value = {2: 56, 1: 2, 5: 12, 4: 24, 6: 18, 3: 323}
print(sorted(key_value.items(), key=lambda x: (x[1], x[0])))  # 注意必须有items()
"""
[(1, 2), (5, 12), (6, 18), (4, 24), (2, 56), (3, 323)]
"""
```

#### 元素是字典的列表排序

```python
lis = [{"name": "Taobao", "age": 100},
       {"name": "Runoob", "age": 7},
       {"name": "Google", "age": 100},
       {"name": "Wiki", "age": 200}]

print("列表通过 age 升序排序: ")
print(sorted(lis, key=lambda x: x['age']))

# 先按 age 排序，再按 name 排序
print(sorted(lis, key=lambda x: (x['age'], x['name'])))

print("列表通过 age 降序排序: ")
print(sorted(lis, key=lambda x: x['age'], reverse=True))

"""
列表通过 age 升序排序: 
[{'name': 'Runoob', 'age': 7}, {'name': 'Taobao', 'age': 100}, {'name': 'Google', 'age': 100}, {'name': 'Wiki', 'age': 200}]
[{'name': 'Runoob', 'age': 7}, {'name': 'Google', 'age': 100}, {'name': 'Taobao', 'age': 100}, {'name': 'Wiki', 'age': 200}]
列表通过 age 降序排序: 
[{'name': 'Wiki', 'age': 200}, {'name': 'Taobao', 'age': 100}, {'name': 'Google', 'age': 100}, {'name': 'Runoob', 'age': 7}]
"""
```

### defaultdict 对象

```python
from collections import defaultdict
```

调用字典时候如果是`dict()`字典，会返回异常；

defaultdict的作用是在于，当字典里的key不存在但被查找时，不会触发异常，会先添加该元素到字典中，值为默认值。

```python
# 创建一个空字典
dict =defaultdict(factory_function)
```

这个`factory_function`可以是`list、set、str`等，作用是当key不存在时，返回的是工厂函数的默认值，比如list对应`[]`，

+ str对应的是`""`
+ set对应`set()`
+ int对应`0`
+ list对应`[]`

## 集合

集合（set）是一个无序的不重复元素序列。

### 创建集合

注意：创建一个空集合必须用 `set()` 而不是 `{}`，因为 `{}` 是用来创建字典。

```python
# 创建空集合
jihe = set()
# 创建有初始值的集合
jihe2 = {1, 2, 3, 4}
# 将其他有序数列转换为集合
jihe3 = set('abracadabra')
b = set([1, 2, 3, 4])  # {1, 2, 3, 4}
```

### 交集&  并集|  差集-

```python
s1 = set("abc")
s2 = set("ade")
# 交集&
>>>s1 & s2
{'a'}
# 并集
>>>s1 | s2
{'c', 'b', 'e', 'a', 'd'}
# 差集
>>> s1 - s2
{'c', 'b'}
```

### 添加元素 s.add(x)

将元素 x 添加到集合 s 中，如果元素已存在，则不进行任何操作。

还有一个方法，也可以添加元素，且参数可以是列表，元组，字典等，语法格式`s.update( x )`

### 删除元素 s.remove(x)

将元素 x 从集合 s 中移除，**如果元素不存在，则会发生错误。**

**推荐使用：**`s.discard(x)`，如果元素不存在，不会发生错误。

### 计算集合元素个数

```python
len(s)
```

```python
thisset = set(("Google", "Runoob", "Taobao"))
len(thisset)
```

### 清空集合

```python
s.clear()
```

## 队列

### deque双端队列

python的deque对象本质是一个双端队列，可以在队列的两端进行操作；

#### 创建一个双端队列

```python
from collections import deque
d = deque() # 创建一个空队列
d = deque(maxlen=20) # 创建队列时限制队列长度
d2 = deque([1, 2, 3]) # 基于列表创建一个队列
```

#### 队尾添加元素

入队和列表类似，使用`append()`函数；

因为是双端队列，如果需要队头添加元素，使用`appendleft()`

#### 队首删除元素

队首出队使用`popleft()`;

因为是双端队列，如果需要队尾删除元素，使类似列表的`pop()`函数；

### 普通队列：Queue 

**建议优先使用deque！**

**注意：**

+ Queue不可下标访问，一般做题用deque最好，`TypeError: 'Queue' object is not subscriptable`

deque可以下标访问元素，而Queue不行。比如这题https://leetcode.cn/problems/animal-shelter-lcci/

+ 判断Queue为空必须用empty函数，**不能直接使用`while Queue:`**

#### 创建一个空队列

```python
from queue import Queue #先进先出队列
q = Queue()
```

#### 入队和出队

```python
q.put("元素")   # 入队
q.get()        # 出队
```

#### 其他方法

```python
q.empty() # 判断队列是否为空
q.full()  # 判断队列是否满了
q1 = Queue(3)  # 创建队列时指定队列大小，超出大小一致阻塞
```

### Python 优先队列

入队时按照优先级进行排序，出队时按照最高优先级取值；

#### PriorityQueue对象

```python
from queue import PriorityQueue
```

`queue.PriorityQueue`这个优先级队列的实现在内部使用了`heapq`，时间和空间复杂度与`heapq`相同。
区别在于`PriorityQueue`是同步的，提供了锁语义来支持多个并发的生产者和消费者。
`PriorityQueue`提供的是基于**类**的接口，而`heapq`是**基于函数**的接口。因此优先使用`PriorityQueue`。

**入队`put()`和出队`get()`：**

```python
from queue import PriorityQueue

q = PriorityQueue() # 创建一个优先级队列
q.put([priority, value]) # 入队 
q.get() # 出队，默认返回最小值
```

+ **优先级值越小，优先级越高**，越先被取出;
+ 如果不输入优先级值，默认元素大小自身作为优先级，`get()`==**默认返回最小值**==；

#### `heapq`模块

##### heapify函数—将现有列表直接转化为堆结构

```python
import heapq
array = [10, 17, 50, 7, 30, 24, 27, 45, 15, 5, 36, 21]
heapq.heapify(array)
print(array)
# [5, 7, 21, 10, 17, 24, 27, 45, 15, 30, 36, 50]
print(heapq.heappop(array))
print(array)
# [7, 10, 21, 15, 17, 24, 27, 45, 50, 30, 36]
```

如不想影响原列表，可以新建一个空列表作为堆结构。

##### nlargest和nsmallest

```pyth
import heapq
array = [10, 17, 50, 7, 30, 24, 27, 45, 15, 5, 36, 21]
heapq.heapify(array)
print(heapq.nlargest(3, array))  # 获取堆中最大几个数
print(heapq.nsmallest(3, array))  # 获取堆中最小几个数
```

##### 小顶堆（每次返回最小值)

**什么是优先队列？**首先是一个队列，入队时和普通队列一样，但是出队时先**自动排序**再出队。

```python
import heapq
array = [10, 17, 50, 7, 30, 24, 27, 45, 15, 5, 36, 21]
heap = []
for num in array:
    heapq.heappush(heap, num) # 加入优先队列中，默认升序
# 弹出最小元素
heapq.heappop(heap)
```

##### 大顶堆（每次返回最大值）

python没有直接构造大顶堆的方法，但是可以巧妙解决；两次负号。

```python
import heapq
array = [10, 17, 50, 7, 30, 24, 27, 45, 15, 5, 36, 21]
heap = []
for num in array:
    heapq.heappush(heap, -num)  # 加入优先队列中，默认升序
# 弹出最小元素
heapq.heappop(heap)
print(heap)
#  [-45, -36, -27, -30, -17, -21, -24, -7, -15, -5, -10]
```

### 典型题

[1845. 座位预约管理系统](https://leetcode.cn/problems/seat-reservation-manager/)

```python
import heapq


class SeatManager:

    def __init__(self, n: int):
        self.seat = [i for i in range(1, n + 1)]
        heapq.heapify(self.seat)

    def reserve(self) -> int:
        return heapq.heappop(self.seat)

    def unreserve(self, seatNumber: int) -> None:
        heapq.heappush(self.seat, seatNumber)
```

#### [347. 前 K 个高频元素](https://leetcode-cn.com/problems/top-k-frequent-elements/)

**普通做法要排序：**

```python
from collections import defaultdict

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        dic = defaultdict(int)
        res = []
        for val in nums:
            dic[val] += 1
        dic_sort = sorted(dic.items(), key=lambda x: x[1], reverse=True)  # 降序
        for i in range(k):
            res.append(dic_sort[i][0])
        return res
```

优先队列做法：

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        heap = [[j, i] for i, j in count.items()]
        heapq.heapify(heap)  # 小堆
        large = heapq.nlargest(k, heap)
        return [j for i, j in large]
```



## python二分查找

`bisect`是python内置模块，用于有序序列的插入和查找。

```python
import bisect
```

使用时首先要排序；

`bisect()`和`bisect_right()`等同;

`bisect.bisect`和`bisect.bisect_right`返回**大于x**的第一个下标 (相当于C++中的`upper_bound`);

`bisect.bisect_left`返回**大于等于x**的第一个下标(相当于C++中的`lower_bound`)。

### bisect()和bisect_right()  -- 大于

```python
import bisect

a = [1, 4, 6, 8, 12, 15, 20]
position = bisect.bisect(a, 13)
print(position)
# 5
position = bisect.bisect(a, 15)
print(position)
# 6
```

### bisect_left()  -- 大于等于

```python
import bisect

a = [1, 4, 6, 8, 12, 15, 20]
position = bisect.bisect_left(a, 13)
print(position)
# 5
position = bisect.bisect_left(a, 15)
print(position)
# 5
```

bisect_left() 有可能越界；

```python
a = [1, 4, 6, 8, 12, 15, 20]
position = bisect.bisect_left(a, 21)
print(position)
# 7
```

### 二分法题目

[875. 爱吃香蕉的珂珂](https://leetcode.cn/problems/koko-eating-bananas/)

```python
import math


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        left = 1
        right = max(piles)
        while left <= right: # 左闭右闭
            mid = (left + right) // 2
            # count = 0
            # for pile in piles:
            #     count += math.ceil(pile / mid)
            count = sum(math.ceil(pile / mid) for pile in piles)
            if count > h:
                left = mid + 1
            else:
                right = mid - 1
        return left
```

## 正则表达式re

### findall函数

`re.findall()`：返回包含所有匹配项的列表；如果没找到返回空列表

**用法：**

```python
import re

re.findall(r"格式字符串", 待匹配字符串)
```

**示例：**

```python
import re
 
str = 'aabbabaabbaa'

# 一个"."就是匹配除 \n (换行符)以外的任意一个字符
print(re.findall(r'a.b',str))#['aab', 'aab']

# *前面的字符出现0次或以上
print(re.findall(r'a*b',str))#['aab', 'b', 'ab', 'aab', 'b']

# 贪婪，匹配从.*前面为开始到后面为结束的所有内容
print(re.findall(r'a.*b',str))#['aabbabaabb']

```

**1. 符号 . 就 是匹配除 \n (换行符)以外的任意一个字符**

```text
print(re.findall(r'a.b',str))
#['aab', 'aab']
```

**2.符号 \* 前面的字符出现0次或以上**

#### 1104. 【软件认证】电话号码转换

https://oj.rnd.huawei.com/problems/1104/details

## 常用库函数或对象

### Counter函数

```python
from collections import Counter
```

+ 求出频率字典

  ```python
  from collections import Counter
  lists = ['a', 'a', 'b', 5, 6, 7, 5]
  a = Counter(lists)
  print(a)  # Counter({'a': 2, 5: 2, 'b': 1, 6: 1, 7: 1})
  ```

+ 找出频率最大的几组值

  ```python
  from collections import Counter
  lists = ['a', 'a', 'b', 5, 6, 7, 5]
  a = Counter(lists)
  print(a.most_common(2))# 返回频率前n的几组值
  # [('a', 2), (5, 2)]
  ```

  

**例子：**

```python
a.elements() # 获取a中所有的键,返回的是一个对象,我们可以通过list来转化它
a['zz']  # 访问不存在的时候,默认返回0
a.update("aa5bzz") # 更新被统计的对象,即原有的计数值与新增的相加,而不是替换
a.subtrct("aaa5z") # 实现与原有的计数值相减,结果运行为0和负值
```

[347. 前 K 个高频元素](https://leetcode-cn.com/problems/top-k-frequent-elements/)

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        res = count.most_common(k)
        return [v[0] for v in res
```

#### [748. 最短补全词](https://leetcode.cn/problems/shortest-completing-word/)

### zip和zip_largest

zip返回的结果以最短的序列为准，zip_longest以最长的序列为准。

如果zip_logest遇到长度不一致的序列，缺少部分会填充None。

+ `zip` 以短的长度为准

  ```python
  a = [1, 2, 3, 4]
  b = [5, 6]
  print(list(zip(a, b)))
  # [(1, 5), (2, 6)]
  ```

+ `zip_largest` 以长的长度为准，短的补`None`

  使用`zip_largest`需要导入`from itertools import zip_longest`

  ```python
  from itertools import zip_longest
  
  a = [1, 2, 3, 4]
  b = [5, 6]
  print(list(zip_longest(a, b)))
  #  [(1, 5), (2, 6), (3, None), (4, None)]
  ```

#### [1768. 交替合并字符串](https://leetcode.cn/problems/merge-strings-alternately/)

```python
from itertools import zip_longest


class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        res = ""
        for x, y in zip_longest(word1, word2):
            if x:
                res += x
            if y:
                res += y
        return res
```

# Python输入输出

## 输入单个字符串

```python
if __name__ == "__main__":
    s = input().strip()
```

## 输入字符串列表

```python
if __name__ == "__main__":
    arrs = input().strip().split() 
```

## 输入整数

```python
if __name__ == "__main__":
    i = int(input().strip())
```

## 输入整型列表

```python
if __name__ == "__main__":
    arrs = list(map(int, input().strip().split()))  # map返回的列表必须用list函数转换
```

# 树的考题

## 构建树

#### [剑指 Offer 07. 重建二叉树](https://leetcode.cn/problems/zhong-jian-er-cha-shu-lcof/)

## 二叉树真题

**二叉树的标准数据结构:**

```python
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
```

通常需要记录每一层元素作为辅助：

```python
level_dict = {}
level_dict["层号"] = ["节点1", "节点2", "节点3"] # 字典
```

### [20230210上机编程[二叉树构建]](http://3ms.huawei.com/km/groups/3803117/blogs/details/13671425?l=zh-cn)

```python
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Solution:
    def create_tree(self, operations: List[List[int]]) -> Optional[TreeNode]:
        root = TreeNode(-1)
        level = {0: [root]}

        for i in range(len(operations)):
            height = operations[i][0]
            index = operations[i][1]
            node = level[height][index]  # 由题目保证存在
            if not node.left:
                node.left = TreeNode(i)
                level.setdefault(height + 1, []).append(node.left)
            elif not node.right:
                node.right = TreeNode(i)
                level.setdefault(height + 1, []).append(node.right)
        return root


if __name__ == "__main__":
    operations = [[0, 0], [0, 0], [1, 1], [1, 0], [0, 0]]
    res_root = Solution().create_tree(operations)


    def dfs(root):
        if not root:
            return
        print(root.val)
        dfs(root.left)
        dfs(root.right)


    def bfs(root):
        que = deque([root])
        while que:
            size = len(que)
            for _ in range(size):
                node = que.popleft()
                print(node.val)
                if node.left:
                    que.append(node.left)
                if node.right:
                    que.append(node.right)


    # dfs(res_root)
    bfs(res_root)
```

http://3ms.huawei.com/doc3ms/index.html?type=all&i18n=zh-cn&text=%E4%BA%8C%E5%8F%89%E6%A0%91#/

## 多叉树真题

多叉树数据结构：

+ **多叉树构造标准结构体**

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.child = []  # 子节点们
```

有时子节点需要知道父节点信息，可以在结构体中添加父节点字段`self.father = None`;

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.child = []  
        self.father = None  # 辅助结构，记录父节点
```

有时需要记录每一行的元素作为辅助信息，健为层数，值为每层列表；

```python
level_dict = {}
level_dict["层号"] = ["节点1", "节点2", "节点3"]
```

+ 直接用hash表，键为根节点，值为子节点列表；

### [1189. 【软件认证】删除指定目录](http://oj.rnd.huawei.com/problems/1189/details)

题目中要求某一子目录挂接在其前面、最近的上一层目录下，因此借助每层字典辅助；

题目中要求删除，因此需要子节点记录父节点；

遍历列表时要拷贝；

```python
from typing import List


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.child = []
        self.father = None  # 一般不加，后面remove时候临时补充的


class Solution:
    def __init__(self):
        self.count = 0

    def del_directorys(self, dir_name_bunch: List[str], dir_tree_lines: List[str]) -> int:
        # 构建树
        # 处理根节点
        root = TreeNode(dir_name_bunch[0])  # 新建根节点
        level_dict = {1: [root]}  # 刷新辅助结构
        dir_tree_lines.pop(0)  # 第一个数据拿掉
        for line in dir_tree_lines:
            spl_list = line.split("|-")
            level, val = len(spl_list), spl_list[-1]
            
            # 刷新树结构
            node = TreeNode(val)  # 创建一个节点
            father = level_dict[level - 1][-1]  # 找到最近的父节点
            father.child.append(node)
            
            # 刷新当前节点辅助结构
            level_dict.setdefault(level, []).append(node)  # 记录每层元素
            node.father = father  # 记录父节点

        def dfs_delete(root: TreeNode):  # 后续遍历
            if not root:
                return
            for i in root.child[:]:  # remove导致列表在变，需要浅拷贝一下
                dfs_delete(i)
            if not root.child and root.val in dir_name_bunch:
                root.father.child.remove(root)
                self.count += 1

        dfs_delete(root)
        return self.count


if __name__ == "__main__":
    dir_name_bunch = list(map(str, input().strip().split()))
    num = int(input().strip())
    dir_tree_lines = [input().strip() for _ in range(num)]
    function = Solution()
    results = function.del_directorys(dir_name_bunch, dir_tree_lines)
    print(results)
```



### 【案例开放107】20221125上机编程[目录树收缩显示]

```python
from typing import List, Tuple


class Solution:
    def __init__(self):
        self.node_count = 0


# org_tree每个元素为父子节点对，org_tree[i][0]为父节点，org_tree[i][1]为子节点
def get_nodes_num(self, org_tree: List[Tuple[str]], depth: int) -> int:
    if depth > len(org_tree):
        return 0
    # 使用字典构造树, key=节点名称, value=子节点数组
    tree_dict = {}
    for father, child in org_tree:
        tree_dict.setdefault(father, []).append(child)
    # dfs遍历
    root = org_tree[0][0]
    self.dfs([root], tree_dict, 1, depth)
    return self.node_count


def dfs(self, nodes, tree_dict, cur_layer, depth):
    if cur_layer == depth:
        self.node_count += len(nodes)
    for node in nodes:
        value = tree_dict.get(node, [])
        # 如果只有一个元素，表示只有一层目录，直接继续dfs，不用更新
        if len(value) == 1:
            self.dfs(value, tree_dict, cur_layer, depth)
            continue
        # 当不是最后的叶子节点，而且也不是一个元素，
        if len(value) > 1:
            self.dfs(value, tree_dict, cur_layer + 1, depth)
```



# python薄弱点

## 二维矩阵

二阶矩阵创建时注意浅拷贝现象；python 浅复制问题 对列表做乘法，对列表修改会修改同一个对象，会导致所有列表都被修改。

如创建m行n列：

正确：`res = [[""] * n for _ in range(m)]`

浅拷贝错误写法：`res = [["" for _ in range(n)]] * m`

参考博客：https://zhuanlan.zhihu.com/p/88197389

**创建二维列表正常方式：**

```python
res = [[0 for i in range(n)] for j in range(m)]  # m行n列
```



# 真题

### 一、破冰船的破冰次数

```python
class Soution:
    def get_number_ice_break(self, route: str, limit: int) -> int:
        count = 0
        x, y = 0, 0
        status = dict()  # 开始破冰时间，健为(x, y)
        for i, val in enumerate(s):
            if val == "U":
                y += 1
            elif val == "D":
                y -= 1
            elif val == "L":
                x -= 1
            elif val == "R":
                x += 1
            if (x, y) not in status.keys():
                count += 1
            else:
                if (i + 1) - status.get((x, y)) > limit:
                    count += 1
            status[(x, y)] = i + 1  # 不管在不在都刷新一次
        return count


if __name__ == "__main__":
    s = input()
    limit = int(input())
    cla = Soution()
    print(cla.get_number_ice_break(s, limit))

```



### 【案例开放126】20230512上机编程[简易文件读写]学习交流

```python
import sys

from collections import defaultdict

class TextFileSys:
    def __init__(self):
        self.text_dic = {}
        # 文件状态
        # 模式
        # 当前内容
        # 位置

    def open(self, filename: str, mode: str) -> int:
        if filename not in self.text_dic:  # 如果该文件不存在
            if mode != 'r' or mode != 'r+':
                self.text_dic[filename] = [1, mode, "", 0]  # 打开 模式 内容 位置
                return 0
        #  如果文件存在
        cur = self.text_dic[filename]
        # 打开时是否清空内容
        if mode in ['w', 'w+']:
            cur[2] = ""
            cur[3] = 0
        if cur[0] == 0:
            cur[0] = 1
            return 0
        return -1

    # ok
    def close(self, filename: str) -> int:
        if filename not in self.text_dic:
            return -1
        cur = self.text_dic[filename]
        if cur[0] == 1:
            cur[0] = 0
            return 0
        return -1

    def write(self, filename: str, content: str):
        if filename not in self.text_dic:
            return -1
        cur = self.text_dic[filename]
        if cur[0] == 1 and cur[1] in ['r+', 'w', 'w+', 'a', 'a+']:  # 打开状态且可写
            pos = cur[3]
            tmp = cur[2]
            cur[2] = tmp[0: pos] + content
            cur[3] = len(cur[2])
            return cur[3]
        return -1

    def readALL(self, filename: str):
        if filename not in self.text_dic:
            return "error"
        cur = self.text_dic[filename]
        if cur[0] == 1 and cur[1] not in ['w', 'a']:
            tmp = cur[2]
            if not tmp:
                return None
            return tmp
        return "error"

if __name__ == "__main__":
    num = int(sys.stdin.readline().strip())
    sys.stdin.readline()
    print("null")
    function = TextFileSys()
    for _ in range(num - 1):
        cmd, value = sys.stdin.readline().strip().split("=")
        paras = value.strip().split(' ')
        filename = paras[0]
        if cmd == "open":
            mode = paras[1]
            print(function.open(filename, mode))
        elif cmd == "write":
            content = paras[1]
            print(function.write(filename, content))
        elif cmd == "close":
            print(function.close(filename))
        elif cmd == "readAll":
            print(function.read_all(filename))
        else:
            print("error input")
```





#  注意事项

什么时候扣0分：

+ 最大圈复杂度大于20
+ 最大签到嵌套深度大于等于8

函数不能超过100行；

圈复杂度 (10,15]扣3分，(15,20]扣5分；

其他情况扣分不会超过20%
