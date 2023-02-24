# Quran Common Phrases

By the python difflib.SequenceMatcher

Download result from [Releases](https://github.com/Salamdev/Quran-CommonPhrases/releases) page.

Steps:

1. Import [quran-simple.sql](quran-simple.sql) (from [tanzil.net](http://tanzil.net) project) to a MySQL/MariaDB database with name 'quran'.
2. Run [removeBesmelah.sql](removeBesmelah.sql)
3. Edit database connection config in [findCommonPhrases.py](findCommonPhrases.py) if needed.
4. Run [findCommonPhrases.py](findCommonPhrases.py)

Result help:

1. **id**: Row id.
2. **a_ayah**: First ayah number.
3. **a_surah**: First surah number.
4. **a_text**: First ayah text to compare.
5. **b_ayah**: Second ayah number.
6. **b_surah**: Second surah number.
7. **b_text**: Second ayah text to compare.
8. **issame**: Two ayahs are same or not (1=same,0=not same).
9. **matchingblock**: Common phrase of two ayahs.
10. **a_place**: Common phrase location in first ayah.
11. **b_place**: Common phrase location in second ayah.
12. **length**: Length of common phrase (by words)
13. **ratio**: Ratio of the phrase similarity (a number between 0 and 1. 1=same)

## License

#### Apache License v2
