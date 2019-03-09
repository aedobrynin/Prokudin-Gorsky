
# Prokudin-Gorsky's photo processing

The program makes colored photo from S.M. Prokudin-Gorsky's negatives. 

![Algo result #1](https://github.com/hashlib/Prokudin-Gorsky/blob/master/results_for_readme/2018678905.png)

![Algo result #2](https://github.com/hashlib/Prokudin-Gorsky/blob/master/results_for_readme/2018679120.png)

![Algo result #3](https://github.com/hashlib/Prokudin-Gorsky/blob/master/results_for_readme/2018679802.png)

## Preparing for work

Before using algorithm you have to install Python requirements from *requirements.txt* using
```
pip3 install -r requirements.txt
```
You may also make new virtual environment before installing requirements.

## Algorithm usage
To make up colored photo you have to execute *algo.py* and provide path to photo in it.

    python3 algo.py data/photo.tif

Your results will be in *result* directory
## Algorithm explanation
My algorithm uses [image pyramid](https://en.wikipedia.org/wiki/Pyramid_(image_processing)) for fast finding the best shifts for image channels, it calculates [correlation coefficient](https://en.wikipedia.org/wiki/Correlation_coefficient) to choose them. I made it multithreaded to speed up. 

## Built With

* [scikit-skimage](https://scikit-image.org/) - A collection of algorithms for image processing

## License

It's free to use. But I'll be grateful, if you mention me ([hashlib](https://github.com/hashlib)) in your work.

## Contact me

If you want to contact me, you should write me an email.
You can find my email [here](https://github.com/hashlib).
**I'm waiting for any report from you, 'cause I know that my code isn't ideal!**

## Algorithm results
The files that I used as input data is too large and I decided to don't post output images on GitHub.
 So, you can find more in my [Dropbox shared folder](https://bit.ly/2EIYNYq)
 To get raw photos you should take number from picture's name, for example, ```2018678848```, and put it into this link: ```http://www.loc.gov/pictures/collection/prok/item/YOUR NUMBER GOES HERE/```.

