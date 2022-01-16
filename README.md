# Genetic Algorithm for Single Page Apps

Genetic Algorithm implementation to classify webpage's components using site's screenshot image.

![Trained DNA](https://github.com/jbagnato/genetic-spa-classifier/blob/main/sample.gif)

As a result you get a json file, a png image with component's area and a gif with the evolution.

## Getting Started

To use it:

0. Set your local paths on constants.py


1. Webscrap some sites using

    ```python
    genspa scrap
    ```

2. Train algorihm with

   ```python
   genspa train config/genspa.json drinkolipop.png
   ```
   
 
## Developer Environment Intallation

```
conda create -n genspa python=3.7 -y

conda activate genspa

pip install -r requirements.txt 
```

## module installation (for develop)

```
python setup.py develop
```

## create wheel (genspa package)

```
python setup.py bdist_wheel
```

## STEPS

* Run webscrapper to get the websites screenshots
* Run Algorithm agains a image
* Return a png image with the classification

## Run WebScraper 

Run on terminal:

```
genspa scrap config/genspa.json
```

## Run Genetic Algorithm

Run on terminal:

```
genspa train config/genspa.json wandure.png
```

## TODO:

* new ways of cross in 2 point
* try diverse mutation, ex. only size, only component
* generate valid chromosome problem over time
* diverse score on same block to tiebreak
* new generation using only 1 list of components and shuffle
* Then on crossover,choice two and swap, so it still valid

## DONE

* ~~fix some components overlap~~
* ~~add json to results with offset and score~~
* ~~detect certain icons to increase accuracy~~
* ~~improve detection time on "about" pattern~~
* ~~add "classism" and better roulette~~
* ~~create detection patterns~~
* ~~create genoma~~
* ~~create chromosoma~~
* ~~create components as python enum~~
