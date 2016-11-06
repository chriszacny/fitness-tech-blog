slugname: analyzing_algorithmic_runtimes
title: Analyzing Algorithmic Runtimes Made Easy
date: 2014-04-03
author: Chris Zacny
category: Programming
tags:
  - algorithms
  - wizardry
  - bigoh-notation

This post is intended to be part of a series of posts I plan on writing analyzing algorithmic runtimes. I recently became interested in algorithmic design and have been making my way through several algorithms textbooks; I actually was presented this material as an undergraduate back in college, and interestingly enough, it was presented differently at that time versus what is in the current textbooks I've been studying. After effectively learning this topic twice, I think there are several confusion points that trip people up.

1. Only O notation is presented and the other two notations, &Omega; and &Theta;, are ignored (this was my case; I was never presented the other two in school).
2. You see statements in the textbooks like n&sup2; = O(n&sup3;), which CLRS[1] actually admits to being an "abuse" of the equality operator.
3. These notations are presented along with the concepts of best, average, and worst case runtimes. The notations actually should be presented separately from those concepts. Only after one understands the three standard notations and how to calculate them, should they start working on best, average, and worst case runtimes (IMHO).
4. The concept of asymptotically tight bounds (what does this mean?).

Today, I'll be focusing primarily on the first point: the notations that define bounds on an algorithm's order of growth, though I'll dabble in 2 and 4 a bit also.

## Venn Diagrams ##
Remember Venn diagrams? Take a look at this:

<img src="/static/img/blog_posts/analyzing_algorithms_1/venn.png"></img>

In basic set theory, we'd write that the union of X and Y is ABCDE. We'd write that the intersection of X and Y is C. Notice that even though C is in X and Y, we only include it once in the intersected and unionized sets. Remember this diagram; we're going to use it throughout this post.

## Upper and Lower Bounds of a Function ##
Let's suppose you are asked to analyze this algorithm's runtime:

	:::python
	def algorithm(number_of_times_to_execute):
	    for i in range(0, number_of_times_to_execute):
	        print('Hello world!')

To start, we need to see how many "computer steps" this algorithm will take to execute for a certain amount of input. In our case, we'll assume that a print operation takes one step. Loops can execute a step multiple times, but evaluating the loop conditions themselves takes a single step. This means we need to step through each and every line of code and see how long it will take. The first line in the algorithm:

	:::python
	for i in range(0, number_of_times_to_execute):

will execute **0** to **number_of_times_to_execute** cycles. But on the last iteration, it checks to see if **i** is less than **number_of_times_to_execute**. So if **number_of_times_to_execute** is equal to 3, this line will actually run 4 times. So we'll just say that takes *n + 1* cycles.

The next line is contained within the loop.  

	:::python
	print('Hello world!')

This line will just take **number_of_times_to_execute** cycles. So we'll say it takes *n* cycles.

Now, we need to add the steps up. Here's that:

	:::text
	(n + 1) + (n)
	n + n + 1
	2n + 1

So we are left with 2n + 1. Let's look at it on a graph:

<img src="/static/img/blog_posts/analyzing_algorithms_1/linear_function.png"></img>

Interesting! At this point, we can begin algorithmic analysis of the runtime. Clearly it appears as though the runtime of this function is linear. Now we just need the tools to prove it.

## Big-O Notation, also Known as an Upper Bound of f(n) ##

Based on our function above, we first want to find an upper bound for its runtime. The upper bounds of functions are known in algorithmic analysis as **Big-O notation**, or simply, O. Its official definition is:

	:::text
	f(n) is one of the functions that is O(g(n)) if there exists some constant c such
	that f(n) is always <= c * g(n), for large enough n. SKIENA[2]

Ah yes. Cryptic mathematical statements. Gotta love 'em. For our specific example, this is basically saying we can state that our function f(n), 2n + 1 is "O of n" if there is some constant factor that we can multiply against n such that c * n always stays above 2n + 1 after a certain point. Let's look at what all this means in more detail.

The first point that is kind of important, is when you attempt to find an upper bound for f(n), you typically omit its multiplicative **constant factors**. That is, instead of writing that 2n + 1 is O(2n + 1) for example, you'd simply write 2n + 1 is O(n), or more simply, 2n + 1 = O(n).

Ah! There is that equals sign. CLRS[1] state that this is an "abuse" of the equals sign, but they use it to their advantage. So basically you need to know that "equals" in this case means something other than equality. It basically means that the function we are analyzing is "in the set of functions." So we're saying "2n + 1 is in the set of functions that is O(n)."

We still haven't tested though whether 2n + 1 is really O(n). In fact, if we look at it on the graph, we see this:

<img src="/static/img/blog_posts/analyzing_algorithms_1/o_n_lower.png"></img>

Wait a minute... wasn't O(n) supposed to be an upper bound? What the heck happened here? The answer is we still haven't applied our constant factor to O(n) from our mathematical definition above. Let's do that now. It would be something like c * n >= 2n + 1.

	:::text
	Let n = 1
	Let c = 1

	1 * 1 >= 2 * 1 + 1
	1 >= 3 NO

Let's try:

	:::text
	Let c = 3
	3 * 1 >= 2 * 1 + 1
	3 >= 3 YES

Cool! But will the constant 3 always hold to be an upper bound for 2n + 1? Let's see on a graph.

<img src="/static/img/blog_posts/analyzing_algorithms_1/o_n_greater.png"></img>

Almost there! Anything left of x = 1 still falls below 2n + 1. However, we still haven't applied the last piece of the definition. Remember the end of the definition of O notation states: "for large enough n". Specifically, we can call the point where the O function >= 2n + 1, n&#8320;. According to the official texts, we don't care about anything to the **left** of n&#8320;. We're only concerned with the big picture - as n approaches infinity does the O function ultimately become the upper bound? In this case, it does.

Now that we've determined that 2n + 1 is one of the functions that is O(n), we can put it in our Venn Diagram:

<img src="/static/img/blog_posts/analyzing_algorithms_1/venn_left.png"></img>

We're getting closer. Now, we have to talk about lower bounds.

## Big-&Omega; Notation, also Known as a Lower Bound of f(n) ##

The second notation people need to be aware of is **Big-&Omega; notation**, or simply &Omega;. Its definition is the **opposite** of O notation:

	:::text
	f(n) is one of the functions that is Omega(g(n)) if there exists some
	constant c such that f(n) is always >= c * g(n), for large enough n. SKIENA[2]

The same concepts apply here as O, except the definition is reversed because we want to find lower bounds. So the question is, can we find a constant "c" such that 2n + 1 >= c * n? We already have! Remember c = 1 in the O definition above? Let's take a look again, except with the corresponding &Omega; definition:

	:::text
	Let n = 1
	Let c = 1

	2n + 1 >= c * n
	2 * 1 + 1 >= 1 * 1
	3 >= 1 YES

Let's plot this on a graph and see if it holds:

<img src="/static/img/blog_posts/analyzing_algorithms_1/omega_n_lower.png"></img>

And there you have it! 2n + 1 is one of the functions that is &Omega;(n)!

Let's update our Venn digram:

<img src="/static/img/blog_posts/analyzing_algorithms_1/venn_right.png"></img>

Things are starting to get pretty interesting. In fact, if you look at that Venn diagram, you'll see that 2n + 1 is in the set of functions that are both O of n and &Omega; of n. What does this mean?

<img src="/static/img/blog_posts/analyzing_algorithms_1/venn_intersect.png"></img>

## Big &Theta; Notation, also known as an Asymptotically Tight Bound on f(n)

The final notation is known as **Big-&Theta;**, or simply, &Theta;. This notation is simply the intersection of O and &Omega; for a said function, if that intersection exists:

	:::text
	f(n) is one of the functions that is Theta(g(n)) if there exists some
	constant c1 such that f(n) is always <= c1 * g(n), for large enough n
	and if there exists some constant c2 such that f(n) is always >= c2 * g(n),
	for large enough n. SKIENA[2]

Since we've found that 2n + 1 is both O(n) and &Omega;(n), we've effectively proven it is &Theta;(n). The nice thing about this is that &Theta;(n) is **asymptotically tight** for 2n + 1, meaning that it will take **no more** than O(n) (our upper bound), and **no less** than &Omega;(n) (our lower bound) for the said constants in the definition.

This means that we can reliably predict how this algorithm's order of growth will change over a large range of inputs. If we didn't have the lower bound for instance, we couldn't say that 2n + 1 is &Theta;(n). Then, as the algorithm grows, we wouldn't really have any idea of what might happen in the lower bounds space. This becomes problematic especially as n gets large, and you could potentially have wide ranges of behavior.

For example, let's say you only have that 2n + 1 is O(n). And let's say instead of printing 'Hello World!', our algorithm is doing something tricky with sorting or counting numbers to and from a huge SAN array running in parallel on a clustered node. In this case, you have no predictive indicator to guarantee that the algorithm will run really fast or really slow for a large number of inputs; this leads to optimization problems (one disk waiting a long time for another to complete for example). But in our case, we have 2n + 1 is &Theta;(n), so we know that it's order of growth will remain linear.

You can't always calculate &Theta;. Sometimes it simply isn't possible. But it's worth it to go the extra mile to see if you can to get more predictable bounds.

## 2n + 1 = O(n&sup2;)... but 2n + 1 != &Omega;(n&sup2;) or &Theta;(n&sup2;)
I wanted to talk about the abuse of the equality operator for a bit and the fact that functions can have **multiple** upper and lower bounds. Clearly, we have to put some constraints on what we mean when we state 2n + 1 = O(n&sup2;). As stated above, we are (at the moment), hypothesizing that 2n + 1 is one of the functions that is O(n&sup2;). We'll run through our basic test again to see if this holds true.

	:::text
	Let n = 1
	Let c = 3
	3^2 * 1 >= 2 * 1 + 1
	3 >= 3 YES

This looks promising; let's look at the graph.

<img src="/static/img/blog_posts/analyzing_algorithms_1/o_n_squared.png"></img>

Indeed, it looks like when n = 1, n&sup2; crosses our function and becomes an upper bound.

So we can say 2n + 1 = O(n&sup2;).

It is kind of weird in that 2n + 1 = O(n) and 2n + 1 = O(n&sup2;). But hopefully these graphs illustrate how this is possible. Just as a point of reference, here is a graph that shows both O(n) and O(n&sup2;) applied as upper bounds to our example function:

<img src="/static/img/blog_posts/analyzing_algorithms_1/multiple_bounds.png"></img>

Let's check if 2n + 1 = &Omega;(n&sup2;).

Maybe if we try to make the constant really tiny... let's try:

	:::text
	Let n = 1
	Let c = .0001
	0.00000001 * 1 <= 2 * 1 + 1
	0.00000001 <= 3. YES

We've found a case where 2n + 1 could potentially be &Omega;(n&sup2;). But if we graph it, we see the same behavior as above, in that &Omega;(n&sup2;) will **eventually** (this is the key; make sure to look at the scale in the image below) become an upper bound for 2n + 1. So 2n + 1 != &Omega;(n&sup2;).

<img src="/static/img/blog_posts/analyzing_algorithms_1/omega_n_squared.png"></img>

Because we can clearly see that 2n + 1 != &Omega;(n&sup2;), **2n + 1 != &Theta;(n&sup2;)** because n&sup2; is not a valid lower bound for 2n + 1.

## Conclusion ##
Today, we've looked at a fairly trivial example for analyzing an algorithm's runtime using the standard 3 notations, O, &Omega;, and &Theta;. In practice, it can be somewhat challenging to calculate all three notations, so I'll come back to this in a future post, where we will look at an actual algorithm and see how to come up with its runtime. I also plan on delving a bit more into best, worst, and average case scenarios and how those fit in with the notations.

Hopefully you now have a basic understanding of how to calculate the different notational values and what they mean in relation to f(n). Confused? Drop me a line and I'll clarify as necessary.

## References ##

[1] Thomas H. Cormen, Charles E. Leirserson, Ronald L. Rivest, and Clifford Stein. *Introduction to Algorithms*. Massachusetts Institute of Technology, third edition, 2009.

[2] Steven S. Skiena. *The Algorithm Design Manual*. Springer, second edition, 1998.
