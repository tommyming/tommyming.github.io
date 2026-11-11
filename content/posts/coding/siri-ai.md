+++
title = "How to implement Siri AI"
summary = "Siri AI is available from iOS 27.3, which allows Siri to interact with your app's App Intent directly."
description = "What is Siri AI Developer Preview, how to implement it, how to improve it, how to measure it."
date = 2026-11-25T16:00:00+08:00
draft = true
categories = ['tech-studies']

+++
#### What is Siri AI Developer Preview?

[API Search Result](https://grok.com/c/f69a5ca8-0968-4894-812f-df2dbf80fdd2?rid=f8567ce1-985e-4ca4-bacf-538d8b70f7a2)

(demo app API above, can use it to draft an app.)

If you are following apple’s latest news, you may see developers share this news on X (formerly twitter):

(screenshot image link)

This actually a crucial step of pushing Siri towards an integrated personal assistant, which is Siri’s original goal in my point of view.

If you have used OpenClaw, Grok Bot, OpenAI Dots, etc before, then you will what personal assistant is. The core purpose is to let the AI agent assist you handle personal stuff, e.g. helps you check emails, arrange calendar, keep track of specific categories, auto-reply, etc.

Siri AI utilizes the feature of AI Personal Assistant. With Foundation Models installed on-device, Siri treats every single app as just like a sandbox/MCP server, or like a box full of tools and hands that the AI can use of your specific app.

> In case if you don’t know what MCP server is, you can try to ask your AI to “Explain MCP server to me like a 5 year old kid”. 
>
> Most of the agents should work.

Integrating your app with Siri AI allows your user to use your app’s feature without opening the app. It is one step further than Shortcuts, which you need to build step by step actions manually, by using the shortcuts app, or within your app’s codebase.

(example video of a demo podcast app I built to integrate with, and trigger the action inside with Siri AI, I need a phone to install iOS 27.3 developer beta maybe. This should be the last part of the demo, when all the below things are finished.)

> If you have Xcode 27.3 (not matter betas, RC(Release Candidate)s or stable releases), feel free to check out my demo repository, which includes all the implementation of the content of this article:
>
>
> (Demo repository Link)

As you can see, when you try to call Siri AI to help you do something, it actually triggers the app context you provided to Siri AI, and perform the functions immediately.

#### Adapt your AppIntents to Siri

Before we start to adapt, let’s see which case you are under:

1. If you are building a completely new app, you need to first build AppIntent in order to make sure the features are available to Siri AI.
2. If you are enhancing the current app, and you app does not have any App Intents, then before implementation, build intents for the features are necessary.

> If you want to know more about AppIntent, you can read the sources below:
>
> [https://developer.apple.com/documentation/appintents/getting-started-with-the-app-intents-framework](https://developer.apple.com/documentation/appintents/getting-started-with-the-app-intents-framework)  
> [https://developer.apple.com/documentation/appintents/creating-your-first-app-intent](https://developer.apple.com/documentation/appintents/creating-your-first-app-intent)

3. If you already have Intents in the current app, then you are ready to go.

[https://developer.apple.com/documentation/appintents/bringing-custom-actions-and-content-to-siri](https://developer.apple.com/documentation/appintents/bringing-custom-actions-and-content-to-siri)

(Demo of build a completely New AppIntent from scratch to adopt with Siri)

(Demo of integrate an existing AppIntent to Siri AI)

#### Update Complex Intents with Extra Guidance

Trigger a simple open action by Siri AI is easy, as it is just a one step action in the AppIntents. But sometimes, the Intents may have complex actions, which includes navigation, multi-step actions. Or the user gives ambiguous text and requests, Siri might need additional guidance to understand your app’s unique domain.

We can orchestrate Siri AI to perform complex actions, by adding agent skills in the app directory. But first, let’s build some agent skills for my demo podcast app:

(Demo of building the 2 agent skills for the demo trying out below.) 

After we finish building our skills, adding to the app directory, then we can try it out to see if Siri can perform these 2 tasks!

(Demo of getting the latest 10 podcast episodes of a specific podcast)

(Demo of finding specific podcast list, and user choose to play which one.)

Seems working good right? But we can try to improve a little bit more.

(Showcase of improving skills accuracy.)

Per my experience, there are some criteria to build a suitable agent skill for Siri to use your app, they are:

→ a list of criteria.

If you want to know more about Orchestration, you can view the Apple Documentation Below:

[https://developer.apple.com/documentation/appintents/orchestrating-complex-actions-with-app-skills](https://developer.apple.com/documentation/appintents/orchestrating-complex-actions-with-app-skills)

#### Make your App Intents works better with Siri

There are multiple ways to make the App Intents works better with Siri. Apple as provide several tools about that:

- Siri Integration Advisor: Built-in inside Xcode, it provides features to help you improve how your app intents work with Siri.

(Demo of my Siri App Intent, showing improvements screenshot)

- Siri Evaluation framework: You can imagine Siri Evals as another set of Unit Test, but specifically for Siri AI. It allows you to write scripts to evaluate the response of the

> If you want to know more about this Framework, be sure to check the EXTRA session below.

#### Current Constraints

Of course, not everything is completely ready when it is released (and it is even still developer preview!). Therefore there are still some constraints and some problems that are blockers to all of us.

- **Language Constraints**: Currently there are only very few languages are supporting. Some languages e.g. Traditional Chinese, Cantonese, Japanese, and not supported yet. Personally think this is because Foundation Model is not ready for prefill context of these languages.
- **Feature Constraints**: If your will use Private Cloud Compute, you will still face restrictions when tokens ran out. This is unavoidable, so be sure that your intent’s workload can run purely on-device.

→ I think there should be some weird problems when I am trying to build the demo app. I can also list them down here.

#### Summary

Siri AI opens another possibility for our users to interact with our apps. 

In the beginning, the user need to tap the app icon to open the app, perform manual navigation by themselves to reach content destination, using their fingers to swipe and touch.

Widgets, include Live Activities later-on, then appeared, which allows developers to build modules, that users can interact with the app’s specific function, without opening an app. 

Shortcuts with Intents then come up as a independent category, allows the user to customize multi-step action with the available intents provided from the app. 

Siri AI push this even further, allowing user to use text/verbal to perform something, and let Siri AI to understand the actions user want to do, and provide nearest-accurate response to users.

What is your thought of the next interaction stage? Send me an email, lemme know what do you think.

#### EXTRA: Siri Evaluations Framework

(I put the details into the “Extra” session, since my article’s target audience are App Developers, how to integrate with your app in the 1st priority. Talking about AI Eval requires basic understanding of “the need to evaluation stage” and “how does AI inferencing works”, which is another area of Tech.)

Documentation is in the below link:

[https://developer.apple.com/documentation/sirievaluations](https://developer.apple.com/documentation/sirievaluations)

For recent months, agents are way more capable than few years ago, which they are generate more accurate code base on our prompts, or from the AI workflow. But there is still one thing remains (and we always need to do even when LLMs are not that capable yet): how can we check if the result is what we expect?

In proper science problem solving cycle, we will first identify the problem, then implement the solution, and at last, we need to evaluate if the solution can meet the goal.

AI Eval works the same way. Maybe we think we have provided a lot of useful context to the agent through a single prompt (that makes sense!), but as code generation is a probability game under the hood, we still need to check if this is doing the right thing.

Take my demo podcast app as an example, if I want to check recommended podcast for app developers, I need to make sure Siri can filter out the correct list of podcast, which its content is partly/mainly about app development.

In order to do that, We need to follow the steps below:

- How to build a proper Eval Script
- How are we going to integrate to the current app → UI Test Target
- How to determine whether it is good or not, from the Eval.
- What can we improve, after receiving the Eval result.
  - Before-After showcase Video maybe.

Let’s do a simple demo for this part!

(Demo of AI Eval using the framework, present the results and how to improve that.)

#### References/Appendix

[https://developer.apple.com/documentation/appintents/siri-ai-developer-preview](https://developer.apple.com/documentation/appintents/siri-ai-developer-preview)