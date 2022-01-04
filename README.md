# genetic-spa-classifier
Genetic Algorithm implementation to classify webpage's components using site's screenshot image

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

* detect certain icons to increase accuracy
* add json to results with offset and score
* improve detection time on "about" pattern
* add "classism" and better roulette