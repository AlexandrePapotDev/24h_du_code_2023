# Parts 2 - Correct Photos

## Description

Among the received photos you now have some very interesting photos but that need to be a little improved. But you no longer have graphic designers! Fortunately a revolutionary AI model is able to apply a correction to a photo from a simple description. You must make this tool available to your team.

With a first model of AI, you will propose to a user to describe in text what he wants to select in an image and thus produce a mask in black and white of the part of the photo to be corrected (in white the part to be modified, in black the part not concerned).

![picture1part2](https://user-images.githubusercontent.com/48018775/229306638-b76eeee9-7092-4461-b181-9e8f63a96ce8.png)

With a second AI model, you will allow the user to describe the modification he wants to make on the photo and using the previous mask. This will produce a corrected image.

![picture2part2](https://user-images.githubusercontent.com/48018775/229306639-04885a02-a88d-4eed-95f6-ea377b0a747b.png)

To evaluate your program, we will ask you to start from the “porsche-911.jpg” image in the evaluation dataset in part 1, in the “retouch” classification. Indeed an advertisement is far too visible, you must delete it with this new tool and demonstrate it to us.

## Method

* Replace a promt from original image with a new prompt
    * *image_path*     => Add the path of your image in png or jpg
    * *prompt_mask*    => Set the element to replace in the original image
    * *prompt_inpaint* => Set the new element to create a new image
    * *threshold*      => A float representing the segmentation mask (near 0 is better)

```
correction(image_path, prompt_mask, prompt_inpaint, threshold)
```
