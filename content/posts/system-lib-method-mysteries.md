+++
title = 'Changes of System-Level Library Method Calls in latest iOS' 
summary = 'Method implementation changes since iOS 18.4 SDK'
date = 2025-06-29T21:00:00+08:00
draft = false
+++

### Before we begin

Let's play a simple game from the beginning. Take a look at the code below:

#### Version 1

``` swift
private var state = __res_9_state()

init() { res_9_ninit(&state) }

deinit { res_9_ndestroy(&state) }
```

#### Version 2

``` swift
private var _state: UnsafeMutablePointer<__res_9_state>?

init() {
    guard let state = malloc(MemoryLayout<__res_9_state>.size)?
        .bindMemory(to: __res_9_state.self, capacity: 1),
          res_9_ninit(state) == EXIT_SUCCESS else {
        return
    }
    
    self._state = state
}
```

### Can you spot the difference?

---

> **The below code is the implementation that uses the object above,
which is a "DNS Address Finder"**

``` swift
private func getDNSAddresses(addressInfo: res_9_sockaddr_union) -> String {
        var addressInfo = addressInfo
        var hostBuffer = [CChar](repeating: 0, count: Int(NI_MAXHOST))

        let sinlen = socklen_t(addressInfo.sin.sin_len)
        _ = withUnsafePointer(to: &addressInfo) {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
                Darwin.getnameinfo($0, sinlen,
                                   &hostBuffer, socklen_t(hostBuffer.count),
                                   nil, 0,
                                   NI_NUMERICHOST)
            }
        }
        
        return String(cString: hostBuffer)
}
    
private func getServers() -> [res_9_sockaddr_union] {
    guard let state = _state else { return [] }
        
    let maxServers = NI_MAXSERV
        
    var servers = [res_9_sockaddr_union](repeating: res_9_sockaddr_union(), count: Int(maxServers))
        
    let foundServers = Int(res_9_getservers(state, &servers, maxServers))
        
    let serverArray = Array(servers[0 ..< foundServers]).filter { $0.sin.sin_len > 0 }
        
    return serverArray
}
```

---

### Introduction/Background

The library we are using from the above code is `libresolv`, which is mainly for creating, sending, and interpreting packets to the Internet domain name servers.

> In case if you are interested, you can visit the link below,
the code is actually open-source by Apple:
[Github Repository](https://github.com/apple-oss-distributions/libresolv)

From the example above, There are a few steps to get the DNS:

1. Create a State Object (`res_9_state`), for accessing server domain from the websocket.
2. We will get the name server infomation, declared as type `res_9_sockaddr_union`.
3. We will use the array of the name server information, to get the name info from the host (as implemented in `getDNSAddresses()`)

The original implementation is built with the mixture of C and Obj-C. But as my codebase is using Swift, I eventually convert the implementation to Swift, to provide compile time safety.

But of course, there are still possible memory leaks and runtime failure, as the library is actually C Library.

### Problem

Let's go back to the **Version 1** of the code:

``` swift
private var state = __res_9_state()

init() { res_9_ninit(&state) }

deinit { res_9_ndestroy(&state) }
```

> To simplify things out, I won't try to explain how pointers and memory addresses works in Swift.
> I also won't talk about the interporality between C++ and Swift.

Before **iOS 18.4**, the implementation works just as expected, the pointers are addressing the location of the type correctly, and can allocate memory with ease

But when you upgrade your Xcode (since 16.3 as far as I know), some signatures of these libraries are actually changed.

**Before Change**
![Before Change](https://images.mingtommy.dev/before_change_libresolv.png)

**After Change**
![After Change](https://images.mingtommy.dev/changes.png)

As you can see, the implementation changes after iOS 18.4, which there is 1 extra layer of pointer, pointing to the declaration.

**And this is root cause of the problem.**

### Solution

Yes, therefore there is a **Version 2** came up, which actually works as expected, in iOS SDK `18.4` (where refactoring has done), and before that.

In order to make it work, we have to manually allocate the memory of resolver state (`__res_9_state`), point the allocated memory address to the variable. WE also need to ensure that the init returns successfully.

### Summary

For me, I think the original is way much cleaner, which is easy to understand while **Version 2** does a bit more complex.

I am not exactly sure why you will need to manually allocate a chunk of memory, and create a pointer for the object to the memory chunk. I would love to have the old version instead, cleaner syntax and less overhead on codebase.

**Thanks for reading, and see you in the next article series!!**
