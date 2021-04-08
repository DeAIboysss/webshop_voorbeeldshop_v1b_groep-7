# Project Voorbeeldshop
In dit project wordt een recommendation engine opgezet door het team voor de website van de "Voorbeeldshop".
Deze recommendations worden aan de hand van een heuristiek opgesteld.

## Recommendations:
* Simple recommendation
* Sub sub category en prijsklasse
* Aanbiedingen / promo's
* Anderen bekeken ook
* Personal

### [Simpel](recom_functions/recom_simple_popular.py) recommendation heuristiek:
De vier best verkochte producten met uitzondering van producten die 0 euro kosten.

### [Similar](recom_functions/recom_price_range.py) recommendation:
Vier producten worden aanbevolen op basis van dezelfde prijsklasse als het huidige product en de huidige sub sub category.

### [Simpele Combination](recom_functions/recom_aanbiedingen_4_1.py) recommendation:
Aanbeveling op basis van producten die een promo hebben.

### [Complicated combination](recom_functions/recom_aanbiedingen_4_2.py) recommendation:
Aanbeveling in de shoppingcart dat wanneer je een product hebt toegevoegd die bij een aanbieidng hoort dat de andere producten in die aanbeiding ook aanbevolen krijgt
![De werking van Personal:](readme_images/flowchart_combination.png)

### [Personal deel 1](recom_functions/recom_personal.py) recommendation:
Het algoritme werkt op basis van previously recommended, viewed before en similars.
Er worden dus aanbevelingen gedaan op basis van iemands kijk gedrag.

![De werking van Personal:](readme_images/Recommendation_personal.png)

### [Personal deel 2](recom_functions/recom_behaviour.py) recommendation:
De aanbeveling werkt op basis van iemands persona. 
Er wordt hier gekeken naar segment in combinatie met previously recommended, viewed before en similars.
