+++
title = 'Blurring Views on Your Apple Device'
summary = 'Usage of Gaussian Blur in SwiftUI and UIKit'
date = 2025-01-26T20:30:00+08:00
draft = true
+++

### TLDR
Below shows a sample code, which blurs the image, using `SwiftUI`.

```swift
Image("dog")
    .resizable()
    .frame(width: 300, height: 300)
    .blur(radius: 20)
// This is a SwiftUI view, which applies the blur effect to the image.
```
Below shows a sample code, which blurs the image, using `UIKit`.
```swift
let imageView = UIImageView(image: UIImage(named: "example"))
imageView.frame = view.bounds
imageView.contentMode = .scaleToFill
view.addSubview(imageView)

let blurEffect = UIBlurEffect(style: .dark)
let blurredEffectView = UIVisualEffectView(effect: blurEffect)
blurredEffectView.frame = imageView.bounds
view.addSubview(blurredEffectView)
// This is a UIKit UIImageView, which you add a mask/layer on top of the image.
```
> `UIKit` actually provides us with more ways to blur a view properly. The above is just one of the example doing it.


### Introduction
SwiftUI and UIKit offer different approaches to implementing Gaussian blur effects in iOS applications.

SwiftUI providing a more streamlined API through its `blur()` modifier and Material types,
UIKit relies on traditional methods like `UIVisualEffectView` for creating blur effects.

In 99% of the cases, Apple Devices uses `Gaussian Blur` to perform blur effect calculation.
So, let's find out how it actually works under the hood!

### Gaussian Blur Basics
Gaussian blur is a widely used image processing technique that softens and smooths images by reducing high-frequency details12. Named after mathematician Carl Friedrich Gauss, this effect applies a weighted average to each pixel based on surrounding pixels, with weights determined by the Gaussian function34. The result is a smooth, gradual blending of colors that creates a soft, out-of-focus appearance.

Key characteristics of Gaussian blur include:

Adjustable blur radius to control the strength of the effect
Reduction of image noise and artifacts
Creation of depth-of-field effects to emphasize subjects
Preparation of images for further editing or manipulation
Efficient implementation in modern graphics software and mobile devices

In mobile development, Gaussian blur is commonly used for creating visually appealing backgrounds, enhancing user interface elements, and achieving various artistic effects in both photography and design applications.

TODO: Update
### Blurs in SwiftUI and Material Types
https://developer.apple.com/documentation/swiftui/view/blur(radius:opaque:)

### Blurs in UIKit

### Summary

### Extra Section (Mainly about `CoreImage`)
Sometimes, you would like to have dig deeper. You want more instead of just `Guassian Blur`.\
You want more blur filters to the image.\
You want someting more customizable.

Especially when you are interested in photography and Photo Editing.

### `CIImage` Basics

### Blur Filters
https://developer.apple.com/documentation/coreimage/cifilter/3228369-motionblurfilter

### Appendix and Resources