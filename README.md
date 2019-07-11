# Quran Common Phrases

Download result from [Releases](https://github.com/Salamdev/Quran-CommonPhrases/releases) page.

Run Steps:
1. Import [quran-simple.sql](quran-simple.sql) (from [tanzil.net](http://tanzil.net) project) to a MySQL/MariaDB database with name 'quran'.
2. Run [removeBesmelah.sql](removeBesmelah.sql)
3. Edit database connection config in [findCommonPhrases.py](findCommonPhrases.py) if needed.
4. Run [findCommonPhrases.py](findCommonPhrases.py)

## License
#### Apache License v2
