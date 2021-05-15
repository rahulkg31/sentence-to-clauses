# Sentence-to-Clauses
A python implementation of extracting clauses from a sentence.

## Example
Example of sentences and their clauses.

Sentence  | Clauses
------------- | -------------
The dog went to the county fair. | ['The dog went to the county fair']
He plays cricket but does not play hockey. | ['He plays cricket', 'He does not play hockey']
Joe waited for the train, but the train was late. | ['Joe waited for the train', 'the train was late']
I can’t believe how fast the dog ran to the county fair. | ["I ca n't believe", 'the dog ran to the county fair']
Joe realized that the train was late while he waited at the train station. | ['Joe realized', 'the train was late', 'he waited at the train station']
Mary and Samantha arrived at the bus station early but waited until noon for the bus. | ['Mary and Samantha arrived at the bus station early', 'Mary and Samantha waited until noon for the bus']

## Dependencies
The project requires Python 3, Nltk and CoreNLP.

## Future
We can use other parser like Berkeley parser and compare the results. We can also add more patterns to handle complex sentences.

Note:- This is a little R&D, I was doing on my part, So it's not a full flegded project and works only for simple sentences and can not parse the complex sentence structures.

## License
The [MIT License][license] - Copyright (c) 2018 Rahul Kumar Gond

[license]: <https://github.com/iamrkg31/sentence-to-clauses/blob/master/LICENSE.md>
