+++
title = 'Apple Watch Download Foundings'
summary = 'How does Apple Watch Download Stuff?'
date = 2025-01-06T20:30:00+08:00
draft = false
+++

### Introduction

```swift
2024-12-31 11:46:37.906547+0800 XXXXXXXX Watch App[340:23913] PDTask <E0CE93E2-86C0-4574-860D-233758C0163A>.<2> finished with error [9] Error Domain=NSPOSIXErrorDomain Code=9 "Bad file descriptor" UserInfo={_kCFStreamErrorCodeKey=9, NSErrorPeerAddressKey={length = 28, bytes = 0x1c1ef516 00000000 fd746572 6d6e7573 ... 6ed931cd 00000000 }, _kCFStreamErrorDomainKey=1, _NSURLErrorRelatedURLSessionTaskErrorKey=(
    "LocalDataPDTask <E0CE93E2-86C0-4574-860D-233758C0163A>.<2>",
    "LocalDataTask <E0CE93E2-86C0-4574-860D-233758C0163A>.<2>"
), _NSURLErrorFailingURLSessionTaskErrorKey=LocalDataPDTask <E0CE93E2-86C0-4574-860D-233758C0163A>.<2>}
2024-12-31 11:46:37.921402+0800 XXXXXXXX Watch App[340:23913] Task <E0CE93E2-86C0-4574-860D-233758C0163A>.<20> finished with error [9] Error Domain=NSPOSIXErrorDomain Code=9 "Bad file descriptor" UserInfo={_kCFStreamErrorCodeKey=9, NSErrorPeerAddressKey={length = 28, bytes = 0x1c1ef516 00000000 fd746572 6d6e7573 ... 6ed931cd 00000000 }, _kCFStreamErrorDomainKey=1, _NSURLErrorRelatedURLSessionTaskErrorKey=(
    "LocalDownloadTask <E0CE93E2-86C0-4574-860D-233758C0163A>.<20>",
    "LocalDataPDTask <E0CE93E2-86C0-4574-860D-233758C0163A>.<2>",
    "LocalDataTask <E0CE93E2-86C0-4574-860D-233758C0163A>.<2>"
), _NSURLErrorFailingURLSessionTaskErrorKey=LocalDownloadTask <E0CE93E2-86C0-4574-860D-233758C0163A>.<20>}
2024-12-31 11:46:37.961+0800 [Error] > [NetworkService] Download Error: URLSessionTask failed with error: Bad file descriptor
```
When you are trying to download any files from a watch app, using `URLSessionDownloadTask`(or any other wrappers) with Swift Concurrency, on a real-device watch. **3 situations** may occur:
- The Watch will dim out after 5-10 seconds, and all the running tasks will be cancelled.
- The Task progress will stuck after you press the download button. Stopped after the task has ran out of time/resources.
- The Task will success, but in a rare and **unknown** situation.

The **Weirdest** thing is, situation **2** and **3** will not happen on Watch simulator, nor main app iPhone/Simulator.

Therefore I started investigation on why it will happen.

##### Testing Devices
> iPhone 12 mini, iOS ver 15.6.1
> Apple Watch Series 5, watchOS ver 8.8.1 

### Problem Investigation

#### Preface
Within this part, I will **Exclude Situation 1**, as the dim and cancel behaviour is expected. As Apple Watch has way less power and processing power than other apple device, it is not resonable to keep demanding tasks running when you are not looking at your watch.

#### Context
There are few possible problem within the whole flow, but before we begin, we can take a look at the flow first.

![Download Task Flow](https://i.postimg.cc/5NxFqmCn/Screenshot.png)

As you can see, the download request will be triggered by user manually, by first requesting the download link from the authenicated API link, then perform downloadTask base on the link, in `.m4a` file format.

#### 1. Network Flow

There are a few parts within the **network flow** that may cause the problem:
- Authentication
- Request Format
- Response Decoding
- File Format (Rare)

(1) **Authentication**
When checking the whole authentication mechanism of the application,
it has proper session token, private tokens, and API access,
it can get the download correctly, and the response is Decodable.

(2) **Request Format**
Request Header and Body includes correct information and required parameters. Also, perform normal `URLSessionTask` requests works fine,
within 

(3) **Response Decoding**
Expected to found `DecodingError` throwed by Swift, but turns out the network request is stalled, and nothing happened after waiting for several minutes.

(4) **File Format (Rare)**
Since the downloaded files are in `.m4a` format, it mainly contains audio flow and context. If there are any corrupted content within the files, download error might be occured. But when I tried to play the section online, the source plays normally.
This is marked as rare issue, as if the file is corrupted, we should discuss with backend first to check what's going on with the media file.

Therefore, seems **API calls** and **network request** are not the issue, as long as `URLSessionTask` works fine on the real device.

Therefore I shifted my focus to the Device Level Problems.

#### 2. App Level

There are mainly **4** part that maybe cause the problem:
- FileManager
- SwiftUI
- Swift Concurrency
- URLSession

(1) **FileManager**
The files I tried to save is in a folder of the document directory. As it is wihtin the app's sandbox, it provides read and write availability easily. By testing with creating database in the same folder successfully, I am sure that `FileManager` is not the issue.

(2) **SwiftUI**
Although SwiftUI has a mixed comments on how it behaves, suppose it is related to UI Flow instead of data flow, so this part will be neglected.

(3) **Swift Concurrency**
The most possible root cause is in here. Same with SwiftUI, it has a mixed comments from developers. But it sometimes brings out unexpected side effects, which is mainly about thread switching and task handling. 

> The problem would be another article, but you can check more on the internet, there are tons of forum posts/article discussing about it. And many workarounds inside.

There are **3** ways you can perform download task through `Alamofire`:

1. This implementation uses `AsyncThrowingStream` to handle the download progress update of the request, returns the URL in the response, throws error if there is any.
``` Swift
let destination: DownloadRequest.Destination = { (_, response) in
            let fileURL = destinationDirectory.appendingPathComponent(response.suggestedFilename!)
            return (fileURL, [.removePreviousFile, .createIntermediateDirectories])
        }
        
        let asyncDownloadStream = AsyncThrowingStream<(DownloadProgressState, URL?), Error> { continuation in
            session.download(urlRequest, to: destination)
                .downloadProgress { progress in
                    continuation.yield((.downloading(progress.fractionCompleted), nil))
                }
                .validate()
                .response { response in
                    switch response.result {
                    case let .success(url):
                        continuation.yield((.done, url))
                        continuation.finish()
                    case let .failure(error):
                        continuation.finish(throwing: error)
                    }
                }
        }
        
        return asyncDownloadStream
```

2. This implementation uses `Continuation` to wrap the sync call, to allow the outside to use async operations properly.
``` Swift
let destination: DownloadRequest.Destination = { (_, response) in
            let fileURL = destinationDirectory.appendingPathComponent(response.suggestedFilename!)
            return (fileURL, [.removePreviousFile, .createIntermediateDirectories])
        }
        
        return try await withCheckedThrowingContinuation { continuation in
            session.download(urlRequest, to: destination)
                .validate()
                .response { response in
                    switch response.result {
                    case let .success(url):
                        continuation.resume(returning: url)
                    case let .failure(error):
                        continuation.resume(throwing: error)
                    }
                }
                .resume()
        }
```

3. This implementation uses `Alamofire`'s original async support, to get the fileUrl:
```Swift
let destination: DownloadRequest.Destination = { (_, response) in
            let fileURL = destinationDirectory.appendingPathComponent(response.suggestedFilename!)
            return (fileURL, [.removePreviousFile, .createIntermediateDirectories])
        }
        
        return try await session.download(urlRequest, to: destination)
            .serializingDownloadedFileURL()
            .value
```

And as expected, 3 implementations does not work.

I firstly think the problem might be related to Swift Concurrency, but in order to gather more info, I dive deeper to the OS level log, by checking `sysdiagnose`.

#### 3. OS Level
> :warning: **Warning** It is NOT always a must to get system logs, use it with caution. 

There are mainly 2 ways to get OS Level logs about your application:
- Logs automatically produced by Apple System about the application sandbox
- `Sysdiagnose`

1. **Application Sandbox Log**
When you access `Settings -> Privacy -> Analytics and Improvements -> Analytics Data`, you will several logs which has the name `XXXXXX-app [DATE].ips` files, which is mainly about the incidents happened of the app. Most part of the log is not useful, but a few things might be helpful:
    - Apart from the basic information of the device running the app, and app-related information, you can also check the `Exception Type` and `Termination Reason`.
    - You may also check with the `Thread` that is performing tasks of your application, especially the threads contain the word `PDTask`(yeah basically is the problem of this article I am facing.)
2. **`Sysdiagnose`**
This is the part when things starts to get tricky. >90% of the log is not useful to us, since most of the names and value are unknown to us. But we can still try to take a look at the `threadById` section.
> You can see, in the log, if you are using any `async` operations, there will be a few things included:
> 1. `waitEvent`: which mainly indicates 2 sets of number, I guess this part acts as a pointer/ pId for the system to assign task context to continue to run.
> 2. `basePriority`: This variable pairs with a number, supposed to be the priority of the task that it should run on the thread.

These things might be useful when you are trying to debug concurrency related issues, if you really need to get into that deep.

After hours of drilling the `sysdiagnose` and the application log, nothing really shows that there is some problem of the device, or there is any problem that might have the issue! :tired_face: 

> I would like to complain a bit about `Apple` is that, it is hard to debug paired watches, especially for companion apps, to get system logs and analyze it from the iPhone is a bit frustrating. Sometimes you will need clues from OS Level to ensure that it is not a problem of OS. `iOS` do provide easier tool, but paired watches requires some hard work to get it done.

#### Everything seems normal and expected! But the download task would stuck? 

### But why Apple Music and Spotify works?
If you have `Apple Music` or `Spotify` watch app, and bought their premium subsrciption plan, download is available for the playlist.

The biggest difference here is that. In the project I am working on, the 

### Am I Missing Something?
1. **Simulator Limitation**
It is always good to use simulator to test out the UI Layout and User Behaviours. But the main problem is, it is not real device.\ 
No matter how well the simulator can mimic, it is under Mac's Architecture, instead of the real device's architecture you build for, there might be some limtations.
> e.g. `WatchConnectivity` can only be tested through real device, even in Apple's Code Example.

2. **URLSession Configuration on watchOS**
After frustrating with the problem for weeks, keep thinking in a wrong route. I started to take a step, start looking the `URLSessionConfiguration` again, to see if there any possible things that I might be missing. Then I found something below:


[waitsForConnectivity](https://developer.apple.com/documentation/foundation/nsurlsessionconfiguration/2908812-waitsforconnectivity)


[allowsCellularAccess](https://developer.apple.com/documentation/foundation/nsurlsessionconfiguration/1409406-allowscellularaccess)


[allowsConstrainedNetworkAccess](https://developer.apple.com/documentation/foundation/nsurlsessionconfiguration/3235751-allowsconstrainednetworkaccess)


After I have set the 3 things as `true` in the confirguation setup, the download suddenly works, no matter sync call or async call.

> I am not sure 100% sure if all of these 3 configuration properties are needed, but **as long as the code works, don't touch it**.

### Possible Causes
Originally, I would like to "_git blame_" the issue to **Swift Concurrency**. Since I have faced a lot of problems when dealing with concurrency(especially on Apple Watch, which thread and process resources are limited).\

But after I tweaked the properties in the `URLSessionConfiguration`, it works fine. Seems there might be some pre-defined conditions that you might need to cater, when you are performing download-related tasks.

If you didn't change the Configuration, various error will occur, which makes you jumping into different rabbit holes, trying to find where the problem is.

### Solution(?)
Just configure `URLSession` properly, with some trial and error, you can perform download tasks on Apple Watch eventually.

### Possible Alternatives
Of course, there are also workarounds, if download doesn't work no matter how:

- Handle the Download Feature with `WatchConnectivity` and the main app
Just like `Spotify`(Although there is no evidence that they use it, but the implementation seems similar), both watch companion app and main app share a playlist, when there are downloads from either sides, `watchConnectivity` will pass the downloaded file to watch app.
- The nature of Apple Watch is not for loading offline media/files, as long as it allows stable internet connection, just do the media handling online.

Side Note: Not sure about `Apple Music`, seems they have a way smoother download experience :thinking_face:?

### Last Words
Tbh, it is quite frustrating when trying to solve this issue, especially you can't root causes even till the OS Level. 

Apart from that **different side issues also blocks my debugging process**(which I have added them to the appendix), testing different frameworks also requires a lot of patience and trial testing. 
(Since you cannot test `watchConnectivity` from Simulator, meanwhile you will need at least 2 watch to compare the UI changes on different versions).

Indeed, debugging to some level requires some sort of **luck**, no one would never expect that adding a few options in `URLSessionConfiguration` with performing sync download calls can solve the problem, when the issue is so rare that only happens on real device.

Even though there is fallback plan (which is using `watchConnectivity`), I am glad that the problem is solved eventually and in the most optimal way.

As trying to debug the issue, I know a lot more about how Swift Concurrency works, how Apple Watch lifecycle performs, and much more about apple watch optimisations and limitations. It is a fruitful experience for me to build the watch app, using new and old frameworks together.

Last but not least, remind yourself, **don't get mislead by the similar foundings on the internet easily. Test the issues and solutions you found.**

With preserverance, plus a tiny bit of luck, you will solve the problem eventually, or at least get something valuable from it.

### Appendix + References
[Bad File Descriptor](https://forums.developer.apple.com/forums/thread/729762)

[Cannot Build Watch App To Real Device](https://stackoverflow.com/questions/56238712/xcode-stuck-with-loading-wheel-after-adding-apple-watch-extension)

[Cannot Reconnect To Apple Watch Device](https://forums.developer.apple.com/forums/thread/734694)

[Major Regressions in Apple Watch Development Support](https://forums.developer.apple.com/forums/thread/750801#750801021)
