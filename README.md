# Prokudin-Gorsky's photo processing

The program makes colored photo from S.M. Prokudin-Gorsky's negatives. 

## There is a [newer version](https://github.com/aedobrynin/gorsky) of this project written on Golang

![Algo result #1](https://github.com/hashlib/Prokudin-Gorsky/blob/master/results_for_readme/2018678905.png)

![Algo result #2](https://github.com/hashlib/Prokudin-Gorsky/blob/master/results_for_readme/2018679120.png)

![Algo result #3](https://github.com/hashlib/Prokudin-Gorsky/blob/master/results_for_readme/2018679802.png)

## How to run

Install requirements:
```
pip3 install -r requirements.txt
```

Run for *your_image.tif*:
```
python3 algo.py your_image.tif
```
The result will be saved in the *result* directory.

## Algorithm explanation
The algorithms finds the best shifts for image channels using [correlation coefficient](https://en.wikipedia.org/wiki/Correlation_coefficient). This process is sped up by [image pyramid](https://en.wikipedia.org/wiki/Pyramid_(image_processing)).

## Built With

* [scikit-skimage](https://scikit-image.org/) - A collection of algorithms for image processing

## Algorithm results
 You can find some in [results_for_readme](results_for_readme) and more [here](https://bit.ly/2EIYNYq).
 
 To get raw photos you should take number from picture's name, for example, ```2018678848```, and put it in this link: ```https://www.loc.gov/pictures/collection/prok/item/YOUR NUMBER GOES HERE/```.

