# hackerrank-euler
## Day 0

As the first step we build solution based on problem stated on
[HackerRank](https://www.hackerrank.com/contests/projecteuler/challenges/euler254/problem) 
as Project Euler #254: Sums of Digit Factorials

That is naive approach base implemented functions definition as is.
```python
import math

def digits_sum(n):
    return sum([int(ch) for ch in str(n)])  

def f(n):
    return sum([math.factorial(int(ch)) for ch in str(n)])

def sf(n):
    return digits_sum(f(n))

def g(i):
    n = 1
    while sf(n) != i:
        n += 1
    return n

def sg(i):
    return digits_sum(g(i))

def sum_sg(n):
    return sum([sg(i) for i in range(1, n + 1)])
```

Day 0 contains initial code extended with simple reporting and test cases.

By using this approach you can compute function sg until value 45 in around 
90 seconds on 
Intel(R) Core(TM) i5-4310U CPU @ 2.00GHz   2.60 GHz.

Python code is in file euler_00_naive.py. 
Tests are in test_euler_00_naive.py. 

Initial analysis will be done next day.

## Day 1

We start with some basic refactoring.

Let's start with define factorial values for digits:
```python
import math
FACTORIALS = [math.factorial(i) for i in range(10)]
```

Next let's improve number conversion into list of digits with generator.
This generator yields digits in reverse order but digits sum is not depend on the digits order.

```python
def digits_gen(n):
    while True:
        yield n % 10
        n //= 10
        if not n:
            break

def digits_sum(n):
    return sum([d for d in digits_gen(n)])   

def f(n):
    return sum([FACTORIALS[d] for d in digits_gen(n)])
    
def sf(n): 
    return digits_sum(f(n)) 
```


Now let's look at function sg. Our final function sum_sg need 
to compute sg & g for values from 1 to n and compute sg sum as a result.
That's mean that it is good to cache g values in case of next call.
Other observation is that for every g(i) we start loop with n = 1. 
instead of find a way to resume g computation from previous n value.

So let's start the first with update sf function to store in cache 
under integer key i such the lowest integer n for which sf(n) == i.

```python
sf_cache = {}

def sf(n):
    sf_ = digits_sum(f(n))
    sf_cache.setdefault(sf_, str(n))
    return sf_
```

And instead of g(i) lets define g_sequence(i) 
which will scan n form 1 until its find g(1), g(2), ..., g(n)

```python
def g_sequence(max_i):
    n = 1
    for i in range(1, max_i + 1):
        if not sf_cache.get(i):
            start_time = time.perf_counter()
            while sf(n) != i:
                n += 1
            stop_time = time.perf_counter()
            if DEBUG:
                print(
                    f"For n = {n:10} sf(n) = {i:2}. sg({i:2}) = {sum([d for d in digits_gen(n)]):2}. "
                    f"Time: {stop_time-start_time:8.4f} seconds"
                )
        else:
            if DEBUG:
                print(
                    f"For n = {sf_cache[i]:10} sf(n) = {i:2}. "
                    f"sg({i:2}) = {sum([d for d in digits_gen(sf_cache[i])]):2}. "
                    f"Time: Computed in earlier step"
                )
    return sf_cache
```


The last change we made before detailed task analysis is the way how 
we will represent number n on which we will work.

Let's define class Digits which will represent the numbers.
Class digits will represent number as a list of integers 0-9 
representing digits starting from least significant (reversed order).
We define methods __str__, digits_gen and next.
Method next will find the next number for testing f values. 

We make them slightly better than just take the next integer.
- When we compute f(n) = x we are interested only in the minimal n giving x 
  as later we look only for minimal n such that sf(n) = s(f(n)) = i. 
  So if we have numbers n0, n1, n2, ... having the same f_value 
  we need to find the smallest one and skip all others. 
  E.g., 2 = f(2) = f(11) = f(1223) = f(2333). So, we need only 2.
- Minimal n giving f(n)=i has digits in not decreasing order. 
  If some digits are decreasing like 32 then f(23)=f(32) and 23 < 32  
- If we have sequence od digits d[0],...,d[i], d[i+1], ....d[k] then
f(d[0]....d[k]) = f(d[0])...f(d[i]) + f(d[i+1]...d[k]) based on f definition
- If we have minimal n where s(f(n)) = i, then n does not contain 0. 
  We can always substitute 10 by 2 because f(10)=f(2) and 2 < 10. We can
  substitute 20 by 12 because f(20)=f(12) and 12 < 20...


Based on this analysis we build next method. In it instead of increasing 
n by 1 when search for g(i) = n, we will take next n in a way that next 
number will be selected in a way that its digits are in increasing order. E.g. 
after 239999 next is 244444 not 24000.

```python
class Digits:
    def __init__(self, number):
        self.num = list(digits_gen(number))

    def __str__(self):
        return ''.join([chr(d+ord('0')) for d in self.num[::-1]])

    @property
    def value(self):
        return reduce(lambda x, y: x * 10 + y, self.num[::-1])

    def next(self, start_digit=0):
        def set_after_carry_on(k):
            """ Set digits after carry on 1.
            Instead of  0 fill with updated digit
            Eg. 2999 + 1 is 3333 not 3000
            """
            filler = self.num[k]
            for ii in range(k-1, start_digit - 1, -1):
                self.num[ii] = filler

        ndx = start_digit
        while True:
            if self.num[ndx] < 9:
                # Non 9 digit so increase it and set all on right to the same value
                self.num[ndx] += 1
                set_after_carry_on(ndx)
                return self
            elif ndx < len(self.num) - 1:
                # if digit 9 then go to next digit
                self.num[ndx] = 0
                ndx += 1
            else:
                # if all digits are 9, then new digit starting with
                self.num.append(1)
                set_after_carry_on(ndx+1)
                return self

```

Now speed of the algorithm is around 600 times faster, 
but it allows as to increase computing sum_sg from 45 to 55 
in time of one minute.
For g(45), n is 12378889
For g(55), n is 1333666799999999999
For g(60), n is 1233456679999999999999999999999

You can notice the n size increases very fast, so the methods 
which is based on finding incrementally such n that sf(n) = i
for i > 70 will not work.

Python code is in file euler_day_01.py. 
Tests are in test_euler_day_01.py. 

## Day 2
We will look more detailed on the way how different n gives the same f(n).

Yesterday we noticed the prospect n numbers has digits ordered 
from smallest to highest.
We also notice yesterday some reduction property: 
- if n has two 11 digits it can be 
replaced by 2 which is makes smaller number 
because its length is shorter by one digit.
  
So we know that numbers which are result of g(i) have maximum one digit 1.

If we apply the same rules to others digit we can easily find that:
- f(222) = f(3) as 2!+2!+2! = 3!
- f(3333) = f(4)
- ...
- f(888888888) = f(9) as 9 * 8! = 9!

As a result that number candidates for being n such that g(i)=n have
the following pattern:

^1{0,1}2{0,2}3{0,3}4{0,4}5{0,5}6{0,6}7{0,7}8{0,8}9*$

- digits are in ascending order
- there is max 1 time 1, 2 times 2, ..., 8 times 8 and any number of 9 digits

We can look as prospect n as pair prefix and suffix. 
- Prefix contains digits from 1 to .8 and has length in range 0..36 digits 
with the longest prefix: 12233344445555566666677777778888888
- Suffix 0 or more digits 9. Unlimited length.


We modify method which gives us next n in a way that after every increment 
we will enforce that next number will be modified in a way that enforce rules states above.

Update function will verify that digit d will not occur more that d times except 9.

```python
class Digits:
    def __init__(self, number):
        if isinstance(number, int):
            self.num = list(digits_gen(number))
        elif isinstance(number, str):
            self.num = [ord(ch) - ord('0') for ch in number[::-1]]
        else:
            self.num = number.num

    def __str__(self):
        """ Return number value as str """
        return ''.join([chr(d+ord('0')) for d in self.num[::-1]])

    @property
    def value(self):
        """ Return number value as int """
        return reduce(lambda x, y: x * 10 + y, self.num[::-1])

    def next(self, start_digit=0):
        def update(d, pos):
            """
            Keep max d digits d from position pos
            :param d: digit to verify occurs no more than d times except 9
            :param pos: starting position 
            :return: return next digit, position for next verify
            """
            # to is max position for d times digit d. if d is 9 no limit for digit 9 so position is up to 0
            to = pos - d if d < 9 else -1  
            for i in range(pos, to, -1):
                if i < 0:   # return no more updates if process the whole number
                    return None, None
                if self.num[i] < d:  # less digit not allowed, so substitute current digit on next position
                    self.num[i] = d
                if self.num[i] > d:  # higher digit OK, so process for this digit starting from current pos
                    return self.num[i], i
            # now we are after d times digit d
            if to < 0:  # exit if end of number
                return None, None
            if self.num[pos - d] <= d + 1:   # next digit must be minimum one higher than previous 
                self.num[pos - d] = d + 1
            return self.num[pos-d], pos-d  # process next number

        def update_prefix():
            """ 
            Update number to fulfill PREFIX definition 122333444455555...
            """
            start = len(self.num) - 1
            digit, start = update(self.num[start], start)
            while digit:
                digit, start = update(digit, start)
            # print(self.num)

        ndx = start_digit
        while True:
            if self.num[ndx] < 9:
                # Non 9 digit so increase it and set all on right to the same value
                self.num[ndx] += 1
                update_prefix()
                return self
            elif ndx < len(self.num) - 1:
                # if digit 9 then go to next digit
                self.num[ndx] = 0
                ndx += 1
            else:
                # if all digits are 9, then new digit starting with
                self.num[ndx] = 0
                self.num.append(1)
                update_prefix()
                return self

    def digits_gen(self):
        """"  Number digits generator """
        for d in self.num:
            yield d

```
Only 4 times faster than day before.
We need huge increase.

Let's try harder next day.

Python code is in file euler_day_02.py. 

Tests are in test_euler_day_02.py. 

## Day 3
In previous days we worked on a way how to improve speed on 
finding n such that g(i) is n. 

Now we are ready to discover that this does not help us find solution.


g(i) is defined as smallest number n such sf(n) (sum of digits f(n)) is eqal n.
For given i the smallest number having digits sum of i is number 
composed of digits 9 and up to one digit at the beginning which sum up to i,

Simply we have number with digit i % 9 at the beginning and i//9 digits n.
So f(n) has i//9 digits. 

When we have k digits f(n) this number is sum of factorial of digits n. 
The biggest factorial is for 9 digit which is less than 10**7. 
That means that for k digits f(n) the number n will have minimum 10**(k-7) digits n.

So that means that for given i, g(i) will have number n 
having minimum 10**(i//9-7) digits so value of n is 10 ** (10 ** (i//9-7)).

For i = 300, n will have 8267195767195767195767195767 
digits 9 plus prefix: 12233344445557777778.
which is 10**28 9 digits comparing to 10**26 from our approximation.

That is clear why method which is based on searching n 
will not work for bigger i.

We need to find other, cheap method for finding g(i) which is not based on 
incremental n increase and test that sf(n)=i.


We know that n  contains 
some digits from PREFIX: 122333444455555666666777777788888888 and
SUFFIX: any number of digits 9.
If n is concatenations of digits in PREFIX and SUFFIX then 
f(n) = f(PREFIX) + f(SUFFIX).
We can find (eg. generating all PREFIXES) that we have 9!-1 prefixes 
and for ay number k from range 1..9!-1 exist prefix such that f(prefix) = k.

So for given x we can find n such that f(n) = x in 
the following way: SUFFIX length is x // 9!. For prefix part we 
need to find prefix such that f(prefix) = x % 9!. 
The easiest is to make table or dictionary which maps from f(prefix)
to prefix (9!-1 elements).

Having this we can build new way of finding n in a way that for a given i 
we try to build f value which gives us i digits and from founded f 
we can build n such that f(n) = f where sum of digits of f is i.

Unfortunately not always smallest f value with sum digits = i 
gives us the smallest n, so we need to look for more numbers having 
sum of digits equal i for finding smallest n.

f(n) = f(PREFIX) + f(SUFFIX)
buf max(f(SUFFIX)) = 9!-1 so when we look at sum of digits(f(n))
we know that f(SUFFIX) can modify only lowes 6 digits of n,
while all others depend on f(SUFFIX)


So let's start and define all prefixes in dictionary which allows us 
map sf(prefix) to prefix. 

For speed up we group prefixes based on 
sf(prefix) value. Sometimes when adding f(Suffux) + f(Prefix) we
can get number with different sum od digits so you can group by sum of digits modulo 9.
. 
In general sf(a+b) != sf(a) + sf(b), but sf(a+b) = (sf(a) + sf(b)) % 9.
See for this [Digit Sum Arithmetic] 
(https://www.sjsu.edu/faculty/watkins/Digitsum00.htm).
There are many articles here about digits sum properties, but most of
them are for reduce digits sum of number until you get single digit sum.

Eg:
```python
{1: ['1', '223', '224444', '22334556', '22334555556666667','22334555556666677788'],}
```

```python
PREFIXES = defaultdict(list)

def init_prefixes():
    for i1 in range(2):
        for i2 in range(3):
            for i3 in range(4):
                for i4 in range(5):
                    for i5 in range(6):
                        for i6 in range(7):
                            for i7 in range(8):
                                for i8 in range(9):
                                    i = i1 + i2 + i3 + i4 + i5 + i6 + i7 + i8
                                    prefix = ('1' * i1 + '2' * i2 + '3' * i3 + '4' * i4 +
                                              '5' * i5 + '6' * i6 + '7' * i7 + '8' * i8)
                                    sf_ = sf(prefix)
                                    PREFIXES[sf_%9].append(prefix)
    for k in PREFIXES.keys():
        PREFIXES[k].sort(key=lambda x: int(x))
```

For suffixes, we assume the following approach:
- Define class FDigits which will keep values f(n) instead of as previously
keep values of n. One of the reason for this: g(129) = n with 
  prefix = 4466788 and suffix: 5,511,463,844 times digit 9,
  while f(n) has 16 digits only.
  
- Method next will instead iterate over n will try to find 
  next f value with same or bigger sum of digits and is multiple of 9!.
  We will take into account digits starting from position 5 and up 
  as digits 0-4 and partly 5 can be filled up to value 47 by prefix.
  
Having number n and required s = sum of digits it's very easy to 
build the lowest number n1 >= n having s digits.
- we need to increase digits starting with the least significant by incrementing 
  digit value up to 9 or less until we reach s. 
  If all digits have 9, and we do not reach s than we increase this 
  number by 1 and start procedure again from the least significant digit 
  again and again until we reach s.
- when we find such number we keep them if it is multiple of 9!. 
-  If not we increase this number until it will be multiple of 9! 
   Verify sum of digits. If sum of digits after increase is not >= s, 
   then we repeat process again
   
So our base algorithm works in the following way:
- Start with the shortest suffix = 0
- look for g(i)
- find the shortest suffix such that sf(suffix) + 47 >= i
- sf(suffix) or sf(suffix+prefix) = i than we store prefix, suffix with  
  the length of (prefix+suffix)
- next we also check for the same i and longer suffix in 
  range up to suffix len equals initial length(prefix+suffix).
  
Our search order is not strictly increasing.  Sometimes 
we can encounter situation like this:

cost:           29, len=     6, g(38) = 24447+9*1

cost:            5, len=     5, g(38) = 235+9*2

cost:            3, len=     8, g(38) = 278+9*5

Best result for i=38 is 235+9*2

As you see we search the first base on suffix length and next try to find prefix which with 
suffix gives us required sum of digits. So in this case:
- our the first finding is n =244479 which has 6 digits. 
- our second finding is 23599 which has 5 digits (the best result) but 
  found in the second step (order based on increasing number of digits 9).
- the third finding is not the best one
- we can stop looking for better results when numbers of 9 will 
  be equal length of the beset find which is 5, because every finding with 6 or more 
  digits gives us higher number because number of 9 digits in it

Let's look at FDigits class:

```python
def get_new_suffix_value(number):
    """ Return list representation of number * 9!. """
    return list(digits_gen(number * FACTORIALS[9]))


class FDigits:
    def __init__(self, number):
        if isinstance(number, str):
            if not number:
                number = '0'
            number = int(number)
        if isinstance(number, int):
            self.n = number
            self.num = get_new_suffix_value(number)
        else:
            self.num = number.num[:]
            self.n = number.n
        self.suffix = self.num[:]
        self.sum = self.suffix_digits_sum()
        self.prefix = [0]

    def __str__(self):
        """ Return number value as str """
        return ''.join([chr(d + ord('0')) for d in self.num[::-1]])

    @property
    def value(self):
        """ Return number value as int """
        return reduce(lambda x, y: x * 10 + y, self.num[::-1])

    def digits_sum(self):
        """
        Sum of suffix only digits in  n.
        Does not include 5 least significant digits and max 7 on the 6th least significant digits.
        :return:
        """
        return sum(self.num)

    def suffix_digits_sum(self):
        """
        Sum of suffix only digits in  n.
        Does not include 5 least significant digits and max 7 on the 6th least significant digits.
        :return:
        """
        suffix_sum = min(7, sum(self.num[5:6]))
        suffix_sum += sum(self.num[6:])
        return suffix_sum

    def next(self):
        """
        Finds next suffix with the same or greater suffix_digit_sum
        """

        def increase_digit(need, digit, *, max_digit=9):
            """
            Increase digit by amount needed. Return Missing amount and increased digit
            :param need: amount of sum digits needed
            :param digit: current digit value
            :param max_digit: maximum digit value
            :return: missing_amount, increased_digit
            """
            inc = min(need, max_digit - digit)
            return need - inc, digit + inc

        def revert_suffix():
            self.num = self.suffix[:]
            assert self.sum == self.suffix_digits_sum()

        def update_value(inc_sum):
            # inc_sum = max(0, self.sum - self.suffix_digits_sum())
            # try to increase digit po position 5 up to 7
            inc_sum, self.num[5] = increase_digit(inc_sum, self.num[5], max_digit=7)
            for i in range(6, len(self.num)):
                inc_sum, self.num[i] = increase_digit(inc_sum, self.num[i])
                if inc_sum == 0:
                    return 0
            return inc_sum

        def next_value_with_sum(sum_needed):
            still_needed = sum_needed - self.suffix_digits_sum()
            while still_needed > 0:
                still_needed = update_value(sum_needed - suffix_sum)
                if still_needed:
                    self.num.append(1)
                    for i in range(0, len(self.num) - 1):
                        self.num[i] = 0
                    still_needed = sum_needed - 1

        def make_suffix_value():
            current_value = self.value
            reminder = current_value % FACTORIALS[9]
            if reminder:
                self.num = list(digits_gen(current_value + FACTORIALS[9] - reminder))
            return self.suffix_digits_sum()

        # Get next suffix value [one 9 digit more so sum is increase by 9!]
        next_value = self.value + FACTORIALS[9]
        self.num = list(digits_gen(next_value))
        suffix_sum = self.suffix_digits_sum()

        while suffix_sum < self.sum:
            next_value_with_sum(self.sum)
            suffix_sum = make_suffix_value()

        self.sum = suffix_sum
        self.suffix = self.num[:]
        assert self.value % FACTORIALS[9] == 0
        self.n = self.value // FACTORIALS[9]
        self.prefix = [0]

```

The base algorithm for finding sequence of g(i):
```python
def g_sequence(max_i):
    """
    Looks for g(i) in range 1..max_i
    Define g(i) to be the smallest positive integer n such that sf(n) == i.
    Results are in a global cached dictionary
    sf(342) = 5, also sf(25) = 5 and 25 is the smallest number giving sf(i) = 5, so g(5) = 25
    :param max_i: range for compute g(i) from 1 to max_i
    :return: None
    """

    def g_find(f_number, *, max_cnt=None):
        """
        Founds n such that sf(n) == i
        :param f_number: suffix starting f(n) with n being suffix with f_number. n - 9 digits
        :param max_cnt: optional limit early stop if n not found based on amount of '9' digits
        :return: tuple <prefix value>, prefix len, suffix, len
                    if not found returns None, None, max_cnt
        """
        cost = 0
        while max_cnt is None or f_number.n < max_cnt:
            # exit in case of limit for amount of '9' digits in suffix
            cost += 1
            f_sum = f_number.digits_sum()
            if f_sum == i:
                # found sf(n) = i, where n contains only digits 9
                print(f'cost: {cost:12}, len={f_number.n:6}, g({i}) = 9*{f_number.n}')
                return 0

            needed_prefix_sum = i - f_sum
            prefix_part_sum = sum(f_number.num[0:6])
            max_prefix_sum = 47 - prefix_part_sum
            if max_prefix_sum < needed_prefix_sum or f_sum > i:
                # print(f'Too small prefix for i={i}  with 9*{n_cnt} and missing digits sum={needed_prefix_sum}')
                f_number.next()
                continue

            prefixes = PREFIXES.get(needed_prefix_sum, [])
            for prefix in prefixes:
                cost += 1
                if digits_sum(f_number.value + f(prefix)) == i:
                    print(
                        f'cost: {cost:12}, len={len(str(prefix)) + f_number.n:6}, '
                        f'g({i}) = {str(prefix)}+9*{f_number.n}')
                    return prefix
            if prefixes:
                pass
                print(f'Not found matched prefix for i={i} with 9*{f_number.n} '
                      f'and missing digits sum={needed_prefix_sum}')
            else:
                pass
                print(f'Missing prefix for i={i}  with 9*{f_number.n} and missing digits sum={needed_prefix_sum}')
            f_number.next()
        # Not found sf(n) = i when d9_counter < max_cnt
        return None

    suffix = FDigits(0)
    for i in range(1, max_i + 1):
        more_results = False
        prefix = g_find(suffix)
        current_len = len(str(prefix)) + suffix.n
        current_suffix = FDigits(suffix)
        suffix.next()
        while suffix.n <= current_len:
            tmp_prefix = g_find(suffix, max_cnt=current_len)
            if tmp_prefix is not None:
                more_results = True
                tmp_len = len(str(tmp_prefix)) + suffix.n
                if tmp_len < current_len:
                    prefix = tmp_prefix
                    current_suffix = FDigits(suffix)
            suffix.next()

        # This make memory overflow        
        # sf_cache[i] = str(prefix) + '9' * current_suffix.n
        sf_cache[i] = digits_sum(prefix) + 9 * current_suffix.n
        if more_results:
            print(f'Best result for i={i} is {str(prefix)}+9*{current_suffix.n}')
        suffix = current_suffix
    return sf_cache


def sg(i):
    """
    Define  sg(i) as the sum of the digits of g(i).
    So sg(5) = 2 + 5 = 7 as g(5) = 25.
    :param i:
    :return: sum digits of g(i)
    """
    if sf_cache.get(i) is None:
        g_sequence(i)
    return int(sf_cache[i])
```

The last thing is changing the way how we store n for g(i).
Until now, we stored n as a string which fails when store result of g(130):

```commandline
cost:          155, len=2755731929, g(128) = 2356668+9*2755731922
cost:           57, len=5511463851, g(129) = 4466788+9*5511463844
Traceback (most recent call last):
  File "C:\python\hackerrank-euler\euler\euler_day_03.py", line 358, in <module>
    total = sum_sg(nn)
  File "C:\python\hackerrank-euler\euler\euler_day_03.py", line 342, in sum_sg
    g_sequence(n)
  File "C:\python\hackerrank-euler\euler\euler_day_03.py", line 308, in g_sequence
    sf_cache[i] = str(prefix) + '9' * current_suffix.n
MemoryError
```
```python
def sg(i):
    """
    Define  sg(i) as the sum of the digits of g(i).
    So sg(5) = 2 + 5 = 7 as g(5) = 25.
    :param i:
    :return: sum digits of g(i)
    """
    if sf_cache.get(i) is None:
        g_sequence(i)
    return int(sf_cache[i])
```
Now we can see:
sum_sg(2000) is 272817460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460317460519218 
computed in 5708.60 seconds.

To verify is this is correct please register on [Project Euler](https://projecteuler.net) web page.
Go to problem 254 and enter value for sum of sg for 150.
But on HackerRank problem is more difficult you - you must build solution which is fast 
enough to pass the tests.

##Day 4
The first time we receive algorithm which which is still very slow 
but can compute g(i) for i 
up to thousands.

The solution built is not easy to build and test and fix 
especially for small i.

The reason behind is the prefix/suffix interaction. For small i, 
the prefix part summed up with suffix(missing or very small) 
introduce huge noise as both parts are very irregular - 
increase and decrease very rapidly.
Later on impact of P
prefix part is negligible as 
distance between two n's having the same sum is bigger than 36 - 
length of suffix. That makes always only one solution with given sum size i as the next  
solution the nearest n having required sum size.













