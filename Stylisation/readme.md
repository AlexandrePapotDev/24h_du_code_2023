# Part 3 - Stylize your photos

The communication service aims to produce a book that tells this race. To stand out, it is important to give a style to this support!

Here again an AI can help you, you have free time to find a solution and implement it in your application.

Example :

![picture1part3](https://user-images.githubusercontent.com/48018775/229314375-d191a067-7abd-4d65-8f78-e5e29d74f715.png)

To evaluate your program, we will ask you to start from the image you modified in Part 2 and to decline it according to 3 style images that we will provide you at the time of the evaluation.

## Method

* Replace a promt from original image with a new prompt
    * *path*       => Add the path of your image in png or jpg
    * *prompt*     => Set the element to replace in the original image

```
image_from_prompt(path, prompt)
```

* Tranfer a chosen style to the older style
    * *content_path*        => Add the path of your image in png or jpg
    * *style_path*          => Add the path of your image style in png or jpg
```
perform_style_transfer(content_path, style_path)
```