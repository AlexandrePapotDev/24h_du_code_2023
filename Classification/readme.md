# Part 1 - Classify quickly the photos

## Description

The communication service of 24 hours received a huge quantity of photos from a lot of sources. Some are professional and some aren't... But amateur photos, spectator photos can contain gem so we cannot neglect them !

Your mission is to train a classification model to classify the photos received in 3 categories :

* The “Perfect” photos: the car is the main object of the photo, not too much publicity or it is blurred, sharp image at least for the car, no crash,... (label: “ok”)
* The “Retouch” photos: presence of identifiable people or many people, photos where the car is blurred, presence of road signs or green posts, presence of a very readable advertising panel (label:“retouch”)
* The “Useless” photos: photos that are not related to the race, photos of concerts, animations, food stands, or photos that are too wide in which cars are not the main object, crash photos,... (label:“exclude”)

To evaluate your success we will pass your classifier on an evaluation dataset that you do not have access to to assign a performance rate on this benchmark dataset.

## Method

* Predict class for one image (Perfect,Retouch or Useless) based on accuracy
    * *img_path*     => Add the path of your image in png or jpg

```
predictClass(img_path)
```

* Classify the test photos 
    * *input_directory*     => Add the path of your test folder
```
evaluate_classifier(input_directory)
```