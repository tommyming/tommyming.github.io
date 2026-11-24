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

Siri AI is still a developer preview. A demo can look finished while real use still hits the limits below.

- **Only a few languages work**: English is the one you can count on. Traditional Chinese, Cantonese, and Japanese are not supported yet. A sentence that mixes English and Chinese often fails too, even when the same request works in English. The on-device model is just not ready for those languages yet. Your code can be correct and still never run, because Siri never connects the sentence to your action.

- **A translated title does not add a language**: A Chinese show name in your list does not fix this. Translating the intent title and description does not turn the language on either. If most of your users do not speak English, treat Siri AI as an English-only beta, and keep Shortcuts for everyone else.

- **Build for the phone, not the cloud**: Design for the on-device model. Private Cloud Compute is only a fallback, and it still has a usage limit. When that limit runs out, the request stops. It does not just get slower, and your app cannot raise the limit.

- **Keep each action small**: Do the search inside your app. Give Siri a short result: one show, a short list, or one episode. Do not ask it to read the whole library in one turn. A long skill plus a big list of shows is the first thing that leaves the phone and hits the cloud limit. Also return a short line Siri can say back. A huge result, or a silent success, still leaves the user unsure if the episode started.

- **Siri only sees actions you turn on**: An intent that already works in Shortcuts stays hidden until you mark it for Siri AI. Using the feature inside the app does not count. A vague title is almost as bad. If two intents both sound like "search podcasts," Siri picks one and goes. The user sees the wrong action, not an error.

- **Use words a person would say**: Siri will not turn "the show I listened to yesterday" into a raw id unless you show it how that phrase maps to a show. If a field can be left empty, Siri may guess instead of asking. Make risky fields required, and stop if the value is not one of yours.

- **Do not send your whole library**: Siri does not have your database. It only sees your tools, your skill text, and what you send back. "Play the last episode" fits. Pasting every show and episode does not. The answers get worse, not faster. Ten episodes is a result. Ten shows with their full history is too much text.

- **Say what fuzzy words mean**: "Closest" can mean location, popularity, or a similar topic. If you do not define it, Siri will guess. Pick one meaning in your code: similar topic, same category, or a tag you chose. If the steps are search, then the user picks, then play, write that order in the skill. Otherwise Siri may skip ahead and play the wrong episode.

- **The spoken name and the id must match**: Give each show a short name a person would say, and a stable id your code looks up. If those two drift apart, the next step plays a different episode from the one the user just agreed to.

- **Preview builds change**: Xcode 27.3 and iOS 27.3 are still previews. What worked last week can fail in the next beta. The usual gap is not broken code. It is the gap between "my action runs when I call it" and "Siri picks that action from a sentence." A passing test does not prove the second one. Run the check again after each beta before you blame your code.

- **Say clearly when a value is missing**: Sometimes the action runs, but the show name comes in empty because Siri did not match what the user said. Tell the user that. Do not play a random episode to fill the gap.

- **Do not trust the confirm step yet**: In the preview, Siri may ask to confirm when you did not ask for that, or skip a confirm you expected. For buy, send, or delete, put the confirm in your own code.

- **Examples teach more than descriptions**: A skill can read well and still pick the wrong action. Siri follows the examples more than the paragraph above them. One bad example teaches the wrong action faster than a careful description can fix. "Play last episode" and "play latest episode" will get mixed up if the wording overlaps. The demo looks broken even when both actions are correct.

- **Do not promise this replaces the app**: Not yet. Do not advertise a language Siri cannot take. Phones that cannot run the on-device model never get this path, so Shortcuts still has to work there. Actions that must be right every time need a confirm you control. An action that works today can miss in the next beta.

The integration is still worth doing. Keep each action useful inside these limits, and leave the in-app path for anything that does not fit.

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

For recent months, agents are way more capable than few years ago, which they are generate more accurate code base on our prompts, or from the AI workflow. But there is still one thing remains (and we always need to do even when LLMs are not that capable yet): how can we check if the result is what we are expecting?

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
