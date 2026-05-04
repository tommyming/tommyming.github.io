+++
title = "Why Apple won't make their APIs(some) backward compatible? (Part 1)"
summary = "Talking about stuff behind the scenes, and API design philosophy why this will happen."
date = 2026-05-04T16:00:00+08:00
draft = false
categories = ['coding']
+++

## Introduction
Suppose you have built an app, no matter vibe-coded with AI or manually. You set the supported version to iOS 26, submit to app store. The app released and received some positive reviews.

__Suddenly, you received an email:__

> Hello, I would like to know if iOS 18 support is available? 
>
> I currently dun wanna update to iOS 26 to my phone, but your app looks so great that I wanna give a try!!!

You checked, agreed that there are still a significant portion of Apple users that are using the older OSes. 

You changed the minimum supported version to iOS 18, you saw an error from a widely used API, you checked the supported version, then you saw this:

![SwiftUI WebView, only available iOS 26+](https://images.mingtommy.dev/swiftui-webview.png "Seems SwiftUI WebView is only available from iOS 26.")

You then probably cursed a bit, wondering why it is so hard for Apple to support new APIs in older versions.

---

And yes, thats one of the most common frustrations that iOS App Developers will face.

Recently, I read a blog about `Task.immediate` from [SwiftLee](https://www.avanderlee.com/concurrency/immediate-tasks-in-swift-concurrency-explained/).

> good blog btw, be sure don't miss it if you want to know how `Task.immediate` works!!

And then I search on Apple Developer Website, turns out it is `iOS 26` only. 

![picture of Immediate Task](https://images.mingtommy.dev/task-immediate.png "Task.immediate only available from iOS 26")

Only 1 sentence pops up from my head:
#### Not Again?

## Wait, this is not something New?
Yes, Apple likes to keep new APIs in distance from the old OS versions.

You may see quite a lot from `SwiftUI`, some from `UIKit`, if you are a iOS Developer.


The most famous example would be `NavigationStack` and `NavigationLink`. Originally `NavigationLink` is not a complete design, there are some flaws inside, thats why Apple published `NavigationStack` on iOS 16+.

In the old days, when I am still supporting iOS 14-15, I cannot really use the new APIs, you have to find an alternative from the community. Mostly we need to use `FlowStacks` (This is my savior during the old days), to implement more proper navigation, to prevent `SwiftUI View` redrawing issues.


Another example would be `Observation Framework` vs `ObservableObject`.
The former one observes the property based on `getter` and `setter` mehcanism, while the latter one relies on `Combine`.

Observation Framework only supports `iOS 17+`. If your app has a lower minimum supported version, then sorry, you probably have to use the old one.

![Observation framework photo, available from iOS 17](https://images.mingtommy.dev/observation.png "The Observation Framework that replaces Observable Object")

---

#### This kinda sucks and, probably, one of the reasons you dislike iOS development, right?

No worries, I do feel the same with you. You can't actually just upgrade your minimum versions, probably because of user base, or your company's business decisions. No matter how much the documentation writes about a bunch of advantages, and, you just can't use it.

And thats why a lot of community workarounds exists. You are not alone, there are many more developers faced this problem.

> Somehow you may wonder...

## Why some do backward-compatible?

The most famous example would be `Swift Concurrency`.

![Swift Concurrency Page Photo](https://images.mingtommy.dev/swift-concurrency.png "Swift Concurrency main page, now got several tutorials and Task as the first introduction.")

Originally when announced, Swift Concurrency only supports `iOS 15+`, which is kinda a great problem.

Therefore, a lot of developers have speak out their concerns on back-porting Swift Concurrency to older versions. You can read [this](https://forums.swift.org/t/will-swift-concurrency-deploy-back-to-older-oss/49370?page=3) in case if you are interested what was happening in the past.

Eventually, Swift Concurrency now supports `iOS 13+`, which is actually something good. (Let's not talk about the design flaws and improvements made these years, this could be a big topic).


And another new attribute appeared, named `@backDeployed` has implemented by Apple, you can check the Swift Evolution Proposal [here](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0376-function-back-deployment.md)

Although not all the APIs/functions can be back-deployed, this is already a good step to support the possibility of backward-compatibility.

--- 

## Make a pause here for the next episode

After finishing all the history and stuff, let's make a pause here. You can find a lot more newer APIs that are not supporting older versions.

I will talk about that in the next episode, and my `Task.immediate` case!

Stay in touch!
