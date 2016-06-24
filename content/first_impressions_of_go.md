Title: First Impressions of the Go Programming Language
Date: 2015-06-13
Modified: 2015-06-13
Category: Programming
Tags: Go, Google, Asynchronous Programming
Slug: first-impressions-of-the-go-programming-language
Authors: Chris Zacny
Summary: My impressions of the Go programming language. Overall, it seems very promising, and I'm excited to use it in future projects.

<img src="/static/img/blog_posts/first_impressions_of_go/gopher.png" class="blog-img-center"></img>

## Overview 
Have you ever encountered a new piece of technology that you were both fascinated by, and drove you kind of nuts at the same time? That is how I felt with the several hours I spent with <a href="https://golang.org/" target="_blank">the Go programming language</a> over the past week or so. I'll detail some of the specifics in this post. 

Disclaimer: these are mostly my opinions, so take them with a grain of salt.

## Why Go?
Why indeed? It is a hard question to answer. I personally used it because an open source project I use a lot had a bug I wanted to fix, and it happened to be written in Go. I'd classify Go as a sort of popular fringe language at the moment, kind of in the same vein as Rust, D, Julia, et. al. These languages are all "kind of" popular, but they still haven't quite taken off yet. In Go's case, it was developed internally at Google, so it does have some merit in terms of an initial development staff.

### But What is it Good At?
I'd say it has several things going for it:

* It is relatively terse, (but definitely NOT as terse as Python) which lends to relatively concise programs that do a lot with a little code.
* It has first class support for pointers. If you have a background in C/C++, and you use something like Python, you may miss the ability to work directly with memory; you can do so in Go.
* It is a compiled language. It was apparently built for performance.
* It is strongly-typed. might be negative in some peoples' opinions, but for me, I like to be able to see exactly what types of primitives I'm working with.
* Good functional support. Supports functional programming models out of the box (closures for example).
* Very "techy" feeling. I think Go would be a great candidate to move Computer Science students into once they've made it past the first or second level courses. I say that because it still retains the same terse feeling as Python, but allows much greater manipulation of the computer. Therefore, I think it would be an excellent second language, as students' competencies at programming improve.
* Excellent server application language. If you are attempting to build a fast, low-level server application that deals with lots of asynchronous requests, networking protocols, etc, Go would probably be a good candidate of languages. I did not use these features in my evaluation of it, so I can't speak to this point more than that.

### What is it not so Good At?

* In my opinion, it is not a beginner language. This is contrary to what I see some of its documentation state. However, just making my way through the tutorials, I definitely felt like the documentation was talking to experienced programmers that have "been there". I wouldn't recommend somebody with no programming experience pick it up; there seem to be much better languages for that (Python or Ruby would be good choices). That said, I wouldn't totally oppose it if they had a good reason.
* No classes. That said, you can sort of mimic classes by using structs and receivers on functions. I'd have to guess that this was a very conscious decision made on Google's part and I'd be interested to learn more as to why it was built like this.
* It feels "backwards". Once you write a bit of it, you'll see what I mean, but here's an example of how to declare an integer variable:
	* **var myInt int**
	* Apparently there was a reason for this; the designers wanted to write the declaration more how it would sound in your head had you not been conditioned by C++. For example, if you wanted to create "a variable of type integer", the way it is written above is more conducive to that grammar, vs. the C++ way. 

## Conclusion
I personally like the more "techy" languages, and I like the fact that Go is terse, yet gives you a lot of power. I would consider using it instead of Python when prototyping out my next server-side application. Given the claims of its speed, it might even make sense to stick with it for the full application lifecycle instead of moving to something like Java once the prototype took off. 

Overall, I'd say, if you enjoy systems programming, give it a try! 