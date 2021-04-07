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

### Sub sub category en prijsklasse recommendation:
Vier producten worden aanbevolen op basis van dezelfde prijsklasse als het huidige product en de huidige sub sub category.

### Aanbiedingen recommendation:
Aanbeveling op basis van producten die een promo hebben.

### Anderen bekeken ook recommendation:
Het algoritme werkt op basis van previously recommended, viewed before en similars.
Er worden dus aanbevelingen gedaan op basis van iemands gedrag.

### [personal](recom_functions/recom_personal.py) recommendation:
De aanbeveling werkt op basis van iemands persona. 
Er wordt hier gekeken naar segment in combinatie met previously recommended, viewed before en similars.
