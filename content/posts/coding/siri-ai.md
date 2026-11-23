+++
title = "How to implement Siri AI"
summary = "Siri AI is available from iOS 27.3, which allows Siri to interact with your app's App Intent directly."
description = "What is Siri AI Developer Preview, how to implement it, how to improve it, how to measure it."
date = 2026-11-22T16:00:00+08:00
draft = true
categories = ['tech-studies']

+++
### What is Siri AI Developer Preview?

If you are following apple’s latest news, you may see developers share this news on X (formerly twitter):

![Siri AI is Available to all developers](https://images.mingtommy.dev/siri-ai-available-dev.png)

This actually a crucial step of pushing Siri towards an integrated personal assistant, which is closer to Siri’s original goal in my point of view.

If you have used OpenClaw, Grok Bot, OpenAI Dots, etc before, then you will what personal assistant is. The core purpose is to let the AI agent assist you handle personal stuff, e.g. helps you check emails, arrange calendar, keep track of specific categories, auto-reply, etc.

Siri AI utilizes the feature of AI Personal Assistant. With Foundation Models installed on-device, Siri treats every single app as just like a sandbox/MCP server, or like a box full of tools and hands that the AI can use of your specific app.

> In case if you don’t know what MCP server is, you can try to ask your AI to “Explain MCP server to me like a 5 year old kid”. 
>
> Most of the agents should work.

Integrating your app with Siri AI allows your user to use your app’s feature without opening the app. It is one step further than Shortcuts, which you need to build step by step actions manually, by using the shortcuts app, or within your app’s codebase.

> If you want to know more about how to make your app ready for Siri, you can make a look at Apple's WWDC Video this year:
>
> https://developer.apple.com/videos/play/wwdc2026/344/

In order to try this out, I downloaded XCode 27.3 Beta, build up a demo podcast app with several App Intents, to see how this works:

(example video of a demo podcast app I built to integrate with, and trigger the action inside with Siri AI, I need a phone to install iOS 27.3 developer beta maybe. This should be the last part of the demo, when all the below things are finished.)

> If you have Xcode 27.3 (not matter betas, RC(Release Candidate)s or stable releases), feel free to check out my demo repository, which includes all the implementation of the content of this article:
>
> https://github.com/tommyming/siri-ai-podcast-demo-app

As you can see, when you try to call Siri AI to help you do something, it actually triggers the app context you provided to Siri AI, and perform the functions immediately.

### Adapt your AppIntents to Siri

Before we start to adapt, let’s see which case you are under:

1. If you are building a completely new app, you need to first build AppIntent in order to make sure the features are available to Siri AI.
2. If you are enhancing the current app, and you app does not have any App Intents, then before implementation, build intents for the features are necessary.

> If you want to know more about App Intents, you can read the sources below:
>
> https://developer.apple.com/documentation/appintents/getting-started-with-the-app-intents-framework
> https://developer.apple.com/documentation/appintents/creating-your-first-app-intent

3. If you already have Intents in the current app, then you are ready to go.

https://developer.apple.com/documentation/appintents/bringing-custom-actions-and-content-to-siri

Let's do a simple integration example:

We can start with building a AppIntent which helps me search my last played podcast episode and play it.

![The Intent will checks your last played episode, and play it](https://images.mingtommy.dev/siri-last-played-episode-intent.png)

But when you try to tell Siri to help you play it, it doesn't work! Because Siri AI (not Siri) does not such AppIntent exist.
In order to expose to Siri, we need to add an Swift Attribute to the Intent Struct:

![Adopt Siri with Attribute called "AppIntent dot tool"](https://images.mingtommy.dev/last-played-intent-adopt-siri-ai.png)

Then when you try again, the AppIntent should be able to trigger by Siri AI using natural language, without any extra setups and click actions.

Most of the time, you will only need this kind of setup to your AppIntent. It is already good enough for user's day-to-day use.

But sometimes, your app has more functions, and you want to guide Siri AI to perform a flow in your app. In this case, you may actually need **Extra Guidance**.

### Update Complex Intents with Extra Guidance

Trigger a simple open action by Siri AI is easy, as it is just a one step action in the AppIntent. 

In some cases, Intents may have complex actions, which includes navigation, multi-step actions, or the user gives ambiguous text and requests, Siri might need additional guidance to understand your app’s unique domain.

In order to achieve the flow, we can orchestrate Siri AI to perform complex actions by 2 things:

1. **Input Control**. Provide multiple text options in the App Intent to ensure biggest capture rate of what user is talking about.
2. **Output Control**. Pre-define agent skills for specific App Intent, make sure Siri AI can refer to the correct destination, and possibly trigger correct result.

But before we do the implementation, let’s take a look at the 2 complex intents I am trying to implement:

The first one is to ask 10 latest episode of user's target podcast:

(intent image here)

The second one is to search the closest podcast, base on user's definition:

(intent image here)

---

You can choose how you build the skills, pre-built `skill-creator` skill from different agent providers, or you build it yourself.

Here is the skills I built using `skill-creator`:

- 10 latest episode of user's target podcast

- the closest podcast, base on user's definition

---

After we finish building our skills, adding to the app directory, then we can try it out to see if Siri can perform these 2 tasks!

(Conversation of getting the latest 10 podcast episodes of a specific podcast)

(Conversation of finding specific podcast list, and user choose to play which one.)

Seems working good right? But we can try to improve a little bit more.

#### How to build better Agent Skills for your app's Intents?

Per my experience, there are some criteria to build a suitable agent skill for Siri to use your app, they are:

(list of criterias that make a good App Intent Agent skikls)

Lets take a look at the difference of the agent skills:

(Demo of search, before and after, in a table)

If you want to know more about Orchestration, you can view the Apple Documentation Below:

https://developer.apple.com/documentation/appintents/orchestrating-complex-actions-with-app-skills

### Make your App Intents works better with Siri

There are multiple ways to make the App Intents works better with Siri. Apple as provide several tools about that:

#### Siri Integration Advisor: 

Built-in inside Xcode, it provides features to help you improve how your app intents work with Siri.

You can found it from the menu shown below:

![Where Siri Integration Advisor Locates](https://images.mingtommy.dev/where-is-siri-integration-advisor.png)

After clicking this, then you can see some suggestion curated by Xcode:

![Suggestions on how to improve the App Intents](https://images.mingtommy.dev/siri-advisor-interface.png)

You can check out the suggestions to improve the App Intents in your app.

#### Siri Evaluation framework

You can imagine Siri Evals as another set of Unit Test, but specifically for Siri AI. It allows you to write scripts to evaluate the response of the

> If you want to know more about this Framework, be sure to check the EXTRA session below.

### Current Constraints

Of course, not everything is completely ready when it is released (and it is even still developer preview!). Therefore there are still some constraints and some problems that are blockers to all of us.

- **Language Constraints**: Currently there are only very few languages are supporting. Some languages e.g. Traditional Chinese, Cantonese, Japanese, and not supported yet. Personally think this is because Foundation Model is not ready for prefill context of these languages.
- **Feature Constraints**: If your will use Private Cloud Compute, you will still face restrictions when tokens ran out. This is unavoidable, so be sure that your intent’s workload can run purely on-device.

→ I think there should be some weird problems when I am trying to build the demo app. I can also list them down here.

### Summary

Siri AI opens another possibility for our users to interact with our apps. 

In the beginning, the user need to tap the app icon to open the app, perform manual navigation by themselves to reach content destination, using their fingers to swipe and touch.

Widgets, include Live Activities later-on, then appeared, which allows developers to build modules, that users can interact with the app’s specific function, without opening an app. 

Shortcuts with Intents then come up as a independent category, allows the user to customize multi-step action with the available intents provided from the app. 

Siri AI push this even further, allowing user to use text/verbal to perform something, and let Siri AI to understand the actions user want to do, and provide nearest-accurate response to users.

What is your thought of the next interaction stage? Send me an email, lemme know what do you think.

### EXTRA: Siri Evaluations Framework

> I put framework details into the “Extra” session, since my article’s target audience are App Developers, how to integrate with your app in the 1st priority. 
>
> Talking about AI Eval requires basic understanding of **the need of evaluation stage** and **how does AI Inferencing works**, which is another area of Tech.

Documentation is in the link below:

https://developer.apple.com/documentation/sirievaluations

For recent months, agents are way more capable than few years ago, which they are generate more accurate code base on our prompts, or from the AI workflow. But there is still one thing remains (and we always need to do even when LLMs are not that capable yet): how can we check if the result is what we expect?

In proper science problem solving cycle, we will first identify the problem, then implement the solution, and at last, we need to evaluate if the solution can meet the goal.

AI Eval works the same way. Maybe we think we have provided a lot of useful context to the agent through a single prompt (that makes sense!), but as code generation is a probability game under the hood, we still need to check if this is doing the right thing.

Take my demo podcast app as an example, if I want to check recommended podcast for app developers, I need to make sure Siri can filter out the correct list of podcast, which its content is partly/mainly about app development.

#### How to build a proper Eval Script

- 
- How are we going to integrate to the current app → UI Test Target
- How to determine whether it is good or not, from the Eval.
- What can we improve, after receiving the Eval result.
  - Before-After showcase Video maybe.

Let’s do a simple demo for this part!

(Demo of AI Eval using the framework, present the results and how to improve that.)

### References/Appendix

https://developer.apple.com/documentation/appintents/siri-ai-developer-preview
