+++
title = "Why Apple won't make their APIs(some) backward compatible? (Part 2)"
summary = "Why ABI stable makes this happen, and how we should react to do better."
date = 2026-10-06T16:00:00+08:00
draft = true
categories = ['coding']
+++

## Introduction
Long awaited **Part 2!**

Sorry for the late, it has been pretty busy these months. 
Volunteering in organize different conferences requires a lot of work and concentration.
It makes me no time to take a seat, grab the concepts, and write them down.

But finally this month has been slightly easier, which I squeezed some time to actually write about this:

**Why Swift ABI Stable feature is making backward-compatibility hard, and why well-architectured Shims can make this happen.**

## TLDR
Apple's system frameworks ship **with the OS** since Swift 5, and Swift is ABI stable — new APIs usually need a new OS version to live in. That's the default, not an accident.
 
Backward compatibility is **mostly a choice, not a technical limit**. 
 
The machinery already exists: `@backDeployed` (SE-0376) + back-deployment shims shipped inside your app — that's exactly how Swift Concurrency reached iOS 13. 

**Community pressure works** — the forums thread from Part 1 is the proof. Want `Task.immediate` / new APIs on older OSes? File feedbacks, speak up.

---

## Let's do a Recap!
> Since it has been several months since part 1 released.

In part 1, we have started discussion from my use-case: `Task.immediate` is only available starting from iOS 26.
I tried to research about the other examples, which I found out a lot of APIs from Apple, that are useful, are not actually back-deployed. (E.g. SwiftUI `WebView` is iOS 26+, `NavigationStack`/`Observation` locked behind new OS versions too.)

But, we also see some of the APIs are getting back-deployed! The most famous one is `Swift Concurrency`, which most of you would know. It got back-deployed to iOS 13, which is definitely a good thing back in the days.
(As the author writing, Xcode requires minimum deployment target of iOS 15+.)

Our goal of part 2, is to look under the hood, and figure out how does a backward compatibility happens.

---

## What does Swift ABI Stable Means? And why it affects all the Apple Frameworks?

First, let's align on the term. ABI stands for **Application Binary Interface** — it is the contract at the *binary* level: how a `struct` is laid out in memory, how arguments are passed in a function call, how the compiler mangles symbol names. Source compatibility is about what your code *reads*. ABI is about what your binary *speaks*.

"ABI stable" simply means that contract is **frozen**: a binary compiled today keeps working with the Swift runtime of tomorrow.

That means, when you are trying to build iOS 18 app to run on iOS 27, it won't crash immediately, as the Swift runtime part of iOS 18 is already a part of iOS 27's Swift runtime. The whole thing is incremental.

> In case if you want to know more about Swift ABI, you can read the [link](https://www.swift.org/blog/abi-stability-and-more/) here.

Sounds weird? Well, it is actually one of the biggest milestones in Swift history: **since Swift 5 (2019), Swift is ABI stable on Apple platforms.** And that leads to a change that matters to this whole story:

> The Swift runtime no longer ships inside your app. It ships inside the OS.

Before Swift 5, every Swift app bundled its own copy of the Swift runtime. Your app, my app, every app on the store — all carrying the same runtime, again and again. ABI stability made it safe to move that runtime into the OS, and let every app share one single copy.

This is also how the modern Apple framework stack is built: `SwiftUI`, `Combine`, `Observation` they are compiled into the OS image, living in `/System/Library/Frameworks`. 

(Screenshot here.)

#### And here comes the problem: there is no App Store for `SwiftUI`!

You can ship an app update any day, Xcode can release any week. But an OS-hosted framework has exactly one release vehicle: the OS itself, several times a year.

So when you build against the iOS 26 SDK, you are building against the *newest* copy of these frameworks. On a device running iOS 18, `Task.immediate` is not hidden behind some flag — **the runtime on that device simply does not have it.** Nothing to call.

Put the chain together:

ABI stable → runtime and frameworks live inside the OS → the OS is their only update channel → new APIs default to "new OS only".

To be fair, ABI stability is not the villain here. It gave us smaller apps and a system-wide Swift. And there *is* a loophole to deliver new APIs to old systems: ship the missing parts **inside your app**. That loophole has a name, and we will meet it later in this post — back-deployment shims.

---

## Difficulty of Backward Compatibility

Now we know where the frameworks physically live. Next question: if the will exists, what makes back-porting actually *hard*?

Let's clear a misunderstanding first: **this is not an issue of the Swift compiler.** The compiler side is completely solved — availability attributes, compile-time diagnostics, `#available` runtime checks, all of them work fine. If you call an iOS 26 API under an iOS 18 target, Xcode stops you politely:

(Screenshot slot: Xcode availability error, e.g. "'immediate' is only available in iOS 26 or newer".)

The hard part sits one layer below: **where does the implementation live at runtime?** For an API to work on an old OS, there are only two worlds it can live in:

- **Inside the OS.** Then an old OS simply has no implementation — there is nothing to call. This is where `Task.immediate` sits today.
- **Inside your app.** A small library ships together with your binary, and on old OSes the call goes there instead. This world exists, and it has a name — back-deployment. (Hold that thought for the next section.)

Option 2 is technically fine, but it is not free. Every back-deployed API has to behave the same across a pile of runtimes — iOS 13, 15, 17, 26... — and every combination is a slot in the testing matrix, plus bugs that only reproduce on the old runtimes. Multiply that by *every* API Apple could back-deploy, *every* year, forever.

And this is why I keep saying it is mostly a choice: the mechanism already exists, standing in plain sight — `@backDeployed` ([SE-0376](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0376-function-back-deployment.md)), the same one we met in Part 1. The compiler supports it. The toolchain supports it. Whether an API gets to ride it is a policy and resource decision, not a technical limit.

---

## Talking back about Task.immediate

OK, time to bring back our main character.

Quick context (and if you missed it, the [SwiftLee article](https://www.avanderlee.com/concurrency/immediate-tasks-in-swift-concurrency-explained/) is here): the everyday `Task { }` does not start when you write it. The operation gets enqueued, hops over to the cooperative pool (or back to the actor), and only then runs. Most of the time you never notice — until you do UI work on `MainActor` and lose a frame waiting for the hop.

`Task.immediate` is Apple's answer for exactly that:

(Paste the declaration of `Task.immediate` from the SDK / swiftinterface here.)

The behavior: the operation starts executing **right away, on the current executor**, and keeps running until its first suspension point. No enqueue hop, no lost frame. It is one of those APIs where you go "wait, we didn't have this before?"

And which OS do you need for it?

(Screenshot slot: the docs page showing `Task.immediate` with "iOS 26+" availability — same style as Part 1's screenshot.)

Yes. iOS 26. The fix for an annoyance that has existed since the iOS 13 days of concurrency, shipped for the newest OS only. Sound familiar? Not Again?

---

## Under the hood

So how would back-deployment even work, physically? This is where my favorite finding of this whole research lives: **SwiftConcurrencyShims**.

Remember the two worlds above. When Swift Concurrency got back-ported to iOS 13, Apple did not teleport code into old OSes — they shipped the missing pieces **inside your app**. When your deployment target is older than the OS that first carried the concurrency runtime, the toolchain links a back-deployment library into your binary (you may have seen `libswift_Concurrency.dylib` hanging around in there).

Then there is the compiler trick. Put `@backDeployed` on a declaration, and instead of calling the OS copy directly, the call goes through a small stub emitted into that shim library. The stub checks at runtime: does *this* OS already have the real implementation? Great, jump to it. It doesn't? No problem, use the copy shipped inside the app.

(Screenshot slot: the evidence you found — declarations carrying back-deployment attributes inside the concurrency shims / swiftinterface, e.g. `@backDeployed(before: ...)` on `Task` APIs.)

And here is the part that makes me sigh: plenty of concurrency APIs did ride this road — which is exactly why `async/await` works on iOS 13 devices today. The machinery exists, it is proven, and it ships with every Xcode.

---

## Why backport is important?

You may ask: "it's one API, why the drama?"

Papercuts like this one are where the hacks come from. You need to work on different workarounds, probably wrapping something with `MainActor.run` to hope that the task runs immediately (which we all know, is probably not, under Swift Concurrency.)

An official `Task.immediate` kills the whole category — one API lands, and an entire family of workarounds can be deleted.

The API might be not important to the user, or even to some of you guys! (since you may not have the use-case of it.) 
But if that API that good enough majority of people using it, you want to implement it, then you found out the API is not available to all the supported versions of your app.

That gap — between the oldest OS your users run and the newest OS that has the API — is exactly where your users live.
You can just ignore those users, keep the signatures to be exclusive to iOS 26+. But sometimes, not everyone has a new iPhone, not everyone can update to iOS 26, and those features are not hardware exclusive.

---

## Sum-up

Writing these two posts, my conclusion didn't really change — it got sharper:

It is not "Apple can't". It is "Apple (so far) chose not to".

The ABI story explains why new APIs default to new OSes. The shims story proves the escape hatch exists and works. Both are true at the same time, and sitting between them is just... decisions.

Which is why the community part matters. Remember the [forums thread](https://forums.swift.org/t/will-swift-concurrency-deploy-back-to-older-oss/49370?page=3) from Part 1? Developers pushed, and `async/await` landed on iOS 13. That was not a gift, that was pressure. If you want `Task.immediate` (or your own favorite iOS-26-only API) on older OSes: file feedbacks, reply on the forums, write about it. It works, and there are receipts.

The findings were genuinely fun to dig into — and if I missed something, or you know why `Task.immediate` skipped the shims, my inbox is open.

I hope to write some more about compilers, different programming languages, or maybe Machine Learning Compilers (which I did a talk at COSCUP this august), and prob something about AI!

See you in next article! 
